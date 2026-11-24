<!--kb
id: mlops-rocm-windows-consumer-gpu
labels: kind:practice-guide, area:machine-learning-ops, rocm, windows, gpu
triggers: running a PyTorch job on the local AMD GPU; is torch.cuda.is_available true on the RX 6700 XT; ROCm on Windows consumer card gfx1031; is fp16 safe for this encoder; how fast is XLM-R large on this machine; reusing an existing ROCm venv instead of installing torch; HF_HOME on an exFAT drive breaks symlinks; VRAM used by another process is invisible
verified: 2026-11-03
review_by: 2027-02-03
confidence: verified
evidence: measured on this machine (RX 6700 XT, ROCm preview); version-sensitive
-->

# PyTorch on an AMD consumer GPU under Windows (ROCm preview) — what works, measured

Author: maria (2026-11-03), with priya's VRAM caveat (her `HOW TO RUN JOBS.md` §4, measured 2026-08-07).
Machine: AMD Radeon RX 6700 XT (12.87 GB, RDNA2 gfx1031 — not on AMD's official ROCm support list), Windows 10,
`torch 2.9.1+rocm7.13.0a20260423` (a **preview** build; the exact wheel index is whatever built
`dev-science-ops/sd-interpretability/.venv` — reuse that venv rather than guessing a URL).

## What works (each measured, not assumed)

| claim | evidence |
|---|---|
| `torch.cuda.is_available()` is True; the ROCm build answers the CUDA API names | device name `AMD Radeon RX 6700 XT` |
| fp16 inference is numerically safe for an XLM-R-large bi-encoder | XL-LEXEME on 1,983 sentences: fp16 vs fp32 cosine per sentence min 0.999824, p01 0.999991 |
| throughput, XLM-R large (560M), batch 32, sentences ~30-60 tokens | fp16 163 sentences/s (1.17 GB peak allocated); fp32 114/s (2.30 GB) |
| model load from a USB external drive | ~35 s for a 2.2 GB `pytorch_model.bin` (load time, not compute) |
| Stable Diffusion 1.4, 50 steps, batch 1 | ~15-16 s/image (priya) |

## What does not (or is unverified)

- bitsandbytes, flash-attention, vLLM: no ROCm-Windows builds; quantised LLMs only via llama.cpp. Docker cannot see the GPU.
- **`torch.cuda.mem_get_info` sees only the calling process on this build** (priya, 2026-08-07): a monitor in a
  separate process reads an empty GPU while a job holds 6 GB. Report VRAM from *inside* the job
  (`torch.cuda.max_memory_allocated`) and use seconds-per-unit to tell GPU from CPU fallback.

## Reusing a working ROCm install without touching it: the `.pth` layer

Installing ROCm torch is the fragile part; the rest is small. To add packages without modifying someone else's venv:

```
<python 3.10 that built the other venv> -m venv .venv-gpu
echo "<abs path to other venv>/Lib/site-packages" > .venv-gpu/Lib/site-packages/zz_other_readonly.pth
.venv-gpu/Scripts/python.exe -m pip install --no-deps <the few extra packages>
```

The `.pth` puts the other site-packages *after* the new venv's own, so the extras installed with `--no-deps` win and
nothing is written into the other venv. Same Python minor version is required (compiled wheels). `--no-deps` is the
point: without it pip "fixes" torch by downloading a CUDA wheel into the new venv. Breaks if the owner upgrades their
venv — the `.pth` file is machine-local and must be gitignored.

## Hugging Face cache on Windows

Without Developer Mode, `huggingface_hub` cannot create symlinks and warns; the cache then stores real copies (more
disk, otherwise fine). Point `HF_HOME` at a registered asset location (`zoo-knowledge-base/tools/assets.py where`),
never at a hard-coded path. Set `HF_HUB_OFFLINE=1` in jobs after the first fetch, so a network blip cannot stall a run.

**Trap (measured 2026-11-03, exFAT external drive):** when two files of a repo have identical content (same blob hash,
e.g. `modules.json` and another small JSON), `snapshot_download` tries `os.symlink` even with symlinks unsupported and
dies with `OSError: [WinError 1]` at the END of the download - the big weights are there, the small config files are
not, and the script never reaches its success line. Symptom in sentence-transformers: `modules.json` missing from the
snapshot. Fix: fetch the missing files directly (`curl -L https://huggingface.co/<repo>/resolve/<rev>/<file>`) into
the snapshot folder; or keep the HF cache on NTFS.

**Same trap, NTFS variant (measured 2026-11-24, C: drive, no Developer Mode):** `snapshot_download` died with `OSError: [WinError 1314]`
(client lacks the symlink privilege) on the FIRST small file, `config.json`; the weights had been downloaded as real copies, `config.json` was
missing, and the job that loaded the model failed with "couldn't connect to huggingface.co" because `HF_HUB_OFFLINE=1` was set. If a pipeline
script pipes the loader through `grep`, the failure is invisible and the script can print its own "OK". Fix: `curl -L` the missing file into the
snapshot folder, and make loops abort when the success marker is absent.

## A newer `transformers` than the shared venv has, without touching it (measured 2026-11-24)

Qwen3 needs transformers >= 4.51; the shared ROCm venv had 4.44. `pip install --no-deps --target <asset dir>/pylibs transformers==4.51.3
tokenizers==0.21.1 huggingface_hub==0.30.2` and put that directory first on `sys.path` inside the job script. On this ROCm-Windows torch build
`import transformers.models.qwen3.modeling_qwen3` then fails with `No module named 'torch._C._distributed_c10d'` because `modeling_utils` does an
unconditional `import torch.distributed.tensor`; stub it before the import (`sys.modules["torch.distributed.tensor"] = types.ModuleType(...)`;
also set `torch.distributed.is_available = lambda: False`). Hidden states of a 4B fp16 decoder (`output_hidden_states=True`, batch 16) ran at
5 to 16 usages/s on the RX 6700 XT depending on text length; Qwen2.5-3B 5 to 9/s.

## llama.cpp (Vulkan build b12065) as a local LLM server on the same GPU: three measured traps (2026-11-24)

- **Throughput decays within about 30 minutes of service when the host is short of RAM** (16 GB with ~12 Electron/Claude processes open: free RAM 1.8 GB,
  pagefile 13 GB used). `llama-server` showed private bytes 10.6 GB and working set 17 MB; prefill fell from ~200-300 tokens/s to ~45. A fresh server was
  about 2x faster for ~15 minutes, then degraded again. A watch on the job's own counter (cache lines per minute) and a restart of the server when the rate drops
  below ~60% of its start rate recovered it; all jobs must be resumable for this.
- **`-fa off` (no flash attention) hung the server** (146 s for the first 143-token prompts, then no progress). Keep `-fa on`, even though the server logs
  "Flash Attention ... assigned to device CPU".
- **Parallel long prompts overrun the per-slot context.** `-c 8192 -np 4 --kv-unified` leaves ~2048 tokens per slot when all four are busy; four concurrent
  40-usage induction prompts (~3-4k tokens each, German and Swedish) returned HTTP 500 while the same prompts run one at a time worked, and a threaded client that
  swallowed the error produced empty inventories downstream. Use one request at a time for long prompts, or a larger `-c`.
