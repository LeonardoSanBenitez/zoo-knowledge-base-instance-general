---
id: mlops-rocm-windows-consumer-gpu
kind: practice-guide
area: machine-learning-ops
status: active
triggers: ["rocm", "windows", "RX 6700 XT", "gfx1031", "torch.cuda.is_available", "fp16", "venv", "HF_HOME", "symlinks"]
---

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
