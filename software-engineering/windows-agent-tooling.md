<!--kb
id: se-windows-agent-tooling
labels: kind:practice-guide, area:software-engineering, status:active
triggers: powershell versus git bash versus wsl, shell script runs in wrong environment,
          windows path works in one shell but not another, utf-8 output becomes mojibake,
          powershell convertto-json uses huge memory, read-only status query exhausts memory,
          convert pdf pages to images on windows, pdftoppm page count wrong,
          pdftotext corrupted an equation, pdf physical page versus printed page
verified: 2026-09-15
-->

# Reliable agent tooling on native Windows

Status: active. This entry records reusable failure modes and safe patterns for agents operating across native
PowerShell, Git Bash/MSYS2, and WSL, plus a tested PDF-inspection workflow. Project-specific interpreter paths,
credentials, and authorization rules belong in the project that owns them.

## Shells are different execution environments

Choose one shell for one command and keep its path conventions, executables, environment variables, and virtual
environment together.

- Use native PowerShell for `.ps1` scripts and native Windows executables.
- Invoke Git Bash explicitly for `.sh` workflows that require MSYS2 semantics.
- Do not assume bare `bash` means Git Bash; on many Windows installations it launches WSL.
- Do not pass a path discovered in one shell directly into another shell without an explicit, tested conversion.
- Use the interpreter documented by the active project. A neighboring virtual environment that can import a
  package is not evidence that it is the right environment.

In shared or committed files, keep paths relative to the project or workspace. Absolute user-directory paths are
both non-portable and unnecessary infrastructure disclosure.

## PowerShell text and object boundaries

PowerShell pipelines carry objects, not merely the text shown in the terminal. Filesystem and provider objects can
carry nested path, drive, provider, and parent metadata. Consequently, a formatter or serializer may traverse a
much larger graph than the displayed fields suggest.

For UTF-8 Markdown, source, and JSON reads:

```powershell
$OutputEncoding = [Console]::OutputEncoding = [Text.UTF8Encoding]::new()
$text = Get-Content -Raw -Encoding UTF8 -LiteralPath $path
```

For a machine-readable status query:

```powershell
$manifest = Get-Content -Raw -Encoding UTF8 -LiteralPath $manifestPath | ConvertFrom-Json
$status = [pscustomobject]@{
    state = [string]$manifest.state
    pid = [int]$manifest.worker_pid
    updated_at = [string]$manifest.updated_at
}
$status | ConvertTo-Json -Depth 2
```

Keep raw log tails as text. Parse JSON files separately, project only the scalar or small array fields needed, and
serialize only that new bounded object. Never deep-serialize a heterogeneous collection containing `Get-Content`
results, filesystem/provider objects, parsed JSON, and logs. A read-only diagnostic can otherwise become a resource
incident: in one measured case, `ConvertTo-Json -Depth 8` over sub-megabyte inputs reached 44.6 GB committed memory
and exhausted the Windows commit limit.

The general invariant is:

\[
\text{diagnostic cost} \leq C\bigl(\text{selected payload size}\bigr),
\]

not a function of the transitive object graph accidentally attached by the shell. Enforce this by projection,
bounded tails, shallow serialization, and explicit output limits.

## PDF inspection with Poppler

Text extraction is a locator, not a visual verifier. It may reorder columns, lose subscripts or signs, flatten
figures, and corrupt displayed equations. For claims that depend on visible equation, appendix, figure, or page
numbering, render the relevant physical pages and inspect the images.

1. Obtain the physical page count with `pdfinfo`; generic file metadata can report an incomplete count.
2. Create the output directory before calling `pdftoppm`.
3. Render only the needed page or small range, initially at 150 DPI.
4. Enumerate the emitted filenames; the last argument is a prefix, not an output filename.
5. Distinguish one-based physical PDF pages from the page numbers printed inside the document.
6. Keep rendered pages as durable evidence only when the owning workflow requires them. Otherwise use disposable
   session scratch and remove it at closeout.

```powershell
$pages = 'project-relative/rendered_pages'
New-Item -ItemType Directory -Path $pages -Force | Out-Null
$prefix = Join-Path $pages 'page'

& pdfinfo.exe 'project-relative/paper.pdf'
& pdftoppm.exe -png -r 150 -f 4 -l 4 'project-relative/paper.pdf' $prefix
if ($LASTEXITCODE -ne 0) { throw "pdftoppm failed with exit code $LASTEXITCODE" }

Get-ChildItem -LiteralPath $pages -Filter 'page-*.png'
```

Raise the resolution only when fine print requires it. Benign font-substitution warnings are not, by themselves,
evidence that rendering failed; the exit code and the inspected image decide.

## Closeout checklist

- The command used one shell and one documented environment.
- UTF-8 was explicit for source and Markdown.
- Any JSON serialization operated on a deliberately bounded projection.
- A PDF claim based on layout or notation was checked on a rendered page, not only extracted text.
- Disposable page renders and other reproducible scratch artifacts were removed.
- Durable evidence lives with the owning project and is indexed there.
