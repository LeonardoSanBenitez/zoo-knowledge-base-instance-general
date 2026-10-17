<!--kb
id: research-archive-api-traps
labels: research-data, archives, reproducibility, osf, zenodo, figshare, dataverse, crossref, retraction, git-lfs, checksums, link-rot
triggers: published results on a non-default git branch; which version of the Zenodo record did the paper use; the record now has a newer version; Hugging Face dataset linked with no revision; find the commit that existed when the paper was published; Hugging Face DOI; huggingface 401 private or deleted; download a dataset from OSF; does this OSF link have files; OSF node is empty; verify Zenodo checksum; Zenodo concept DOI; figshare file count zero; figshare embargo; Dataverse checksum mismatch; Dataverse csv tab; is this paper retracted; Crossref updated-by; Retraction Watch in Crossref; check correction to a paper; git lfs pointer 134 bytes; is this data link dead; 410 vs 404; file written as 0 bytes on Windows; colon in filename Windows
verified: 2026-10-16
-->

# Research archives: the ways a fetch reports success without having succeeded

Status: active. Author: maria. Measured 2026-08-25 to 2026-10-14 while building
`dev-science-ops/paper-retrospective-reproducibility/tools/acquire.py` (Dataverse, Zenodo, OSF,
figshare backends) and `tools/gate.py` (V1 identifiers, V20 corrections). Every trap below was met on
a live deposit, and each has an offline test in that project's `tools/test_acquire.py` or
`tools/test_gate.py`. **These are API behaviours on the dates given; re-check before relying on
one.**

---

## The one rule underneath all of them

Every archive answers the *easy* question ("does the identifier resolve?") with HTTP 200 whether or
not it holds the bytes you need. **Ask the archive's API what it holds, fetch it, hash what is on
your disk, and run the same check against a case whose answer you already know.** A zero that has
never been shown to be capable of being non-zero is not evidence.

## Per archive

| archive | trap | what it looks like | what to do |
|---|---|---|---|
| **Dataverse** | serves an *ingested derivative* of tabular files by default | every `.csv`/`.dta` mismatches its published md5; looks like a corrupt deposit. Cost 8 false defect claims on one flawless deposit | `/api/access/datafile/<id>?format=original` |
| Dataverse | `directoryLabel` is separate from `filename` | same-named files in different folders overwrite each other on disk; relative paths in the authors' scripts break. One deposit: 56 of 59 files foldered, 4 `README.md` | local path = `directoryLabel/filename` |
| **Zenodo** | concept DOI | `10.5281/zenodo.<n>` may be the *concept*, which always resolves to the newest version | pin a version record; refuse a record whose `conceptrecid == id` |
| Zenodo | checksum is `md5:<hex>` | comparing to a bare hexdigest never matches | strip the algorithm prefix; refuse an algorithm you cannot compute |
| Zenodo | restricted/embargoed | HTTP 200, title, licence, empty file list | zero files is a failure, not an empty success |
| **OSF** | `osf.io/<guid>` is an SPA shell | live, deleted and invented GUIDs return **byte-identical** HTTP 200 pages | ask `api.osf.io/v2/guids/<g>/`: 410 = deposited and deleted, 404 = never minted |
| OSF | `/nodes/<g>/files/` lists **storage providers** | every node appears to have >= 1 "file" | walk providers -> folders -> files |
| OSF | an add-on provider whose external storage is gone | the add-on's listing answers **404** (osf.io/3bzu8: GitHub add-on configured for a deleted repository) | record it by name; it is not "empty" |
| OSF | pages are bounded (default 10) | silent truncation | follow `links.next` |
| OSF | only `osfstorage` publishes hashes | add-on files (GitHub, Dropbox...) have none | record as unverified, never verified |
| OSF | files are versioned | the hash you read is for `current_version`; a new version between list and download is a false mismatch | download `...?version=<current_version>` |
| OSF | `?view_only=<key>` in the cited URL | the node answers **401** and looks private. In a 60-paper PLOS scout (2026-10-14), 10 papers had a DAS GUID answering 401; 7 of the 10 printed a key in the same URL and all 7 opened with it. 14 of 49 DAS naming OSF use such a link | the key is part of the identifier: carry it on every request, including pagination, children and the download |
| OSF | a second method for "is it private?" | `osf.io/api/v1/project/<g>/` (legacy) answers **200 for private nodes too**: another shell | use WaterButler, `files.osf.io/v1/resources/<g>/providers/osfstorage/`: 200 public, 403 private, 404 invented (controls agreed 2026-10-14) |
| OSF | child components | a parent can be empty while its children hold everything | list `/children/`; the children are separate GUIDs |
| **figshare** | unversioned id floats | `/articles/<id>` and `m9.figshare.<id>` are the newest version | require `.v<N>`; fetch `/articles/<id>/versions/<N>` |
| figshare | zero files, three different reasons | `embargo_type: file` + `embargo_date` (one "Analysis code for:" deposit embargoed to 2027-10-13); `is_metadata_record: true` (no files by design); or unexplained. **7 of 40** public search hits on 2026-10-14 listed zero files | say which; none of them is "broken" |
| figshare | two md5s | `computed_md5` (figshare's, of what it holds) vs `supplied_md5` (uploader's) | check against `computed_md5`; if the two disagree, that is a claim about the deposit |
| figshare | `is_link_only` | the "file" is a link elsewhere; figshare holds no bytes | not fetched, not verified |
| figshare | file list size | the article endpoint embedded all 491 files of one deposit (matched `/files?page_size=1000`) | no truncation seen; not a guarantee |
| **Hugging Face** | the HF DOI floats | `10.57967/hf/2481`: DataCite stores `version: caa7a91` (a commit), but its `url` -- where doi.org sends you -- is the repo page, i.e. today's `main` (checked by maria and mark, 2026-10-14/16). HF docs: a DOI is minted "for the current revision" | read the commit from DataCite (`api.datacite.org/dois/<doi>` -> `attributes.version`) and fetch `.../resolve/<sha>/...`; same family as a Zenodo concept DOI |
| Hugging Face | a dataset linked with no revision | the link means `main` *today*. NeurIPS 2024 D&B (mark, 2026-10-14): 94 papers linked their own HF data, 89 cited `main`, 0 cited a revision; **19 of 94 (20%)** had own data files change after camera-ready, 12 of them modifying or deleting files | find the commit at the paper's date from the repo's commit list (`/api/datasets/<id>/commits/main`); `.../commit/<sha>.diff` lists paths per commit anonymously (LFS shows as pointer diffs, small). Numbers: mark's `report_2026-10-14.txt` |
| Hugging Face | **401** anonymously | answered for private **and** deleted repos alike (`cerebras/SlimPajama-627B`: 401 on API and page). Gated repos answer **200** with a `gated` field | 401 is not "gated" and not "private": it is "cannot tell" |
| Hugging Face | renamed repo | old id answers **307** to the new one (`rethinlab -> rethinklab/Bench2Drive`) | follow, and record the rename: the printed id is no longer the identity |
| **GitHub LFS** | pointer served as content | `raw.githubusercontent.com` answers 200 with a ~134-byte pointer while `media.githubusercontent.com` answers 404 (a 335 MB object) | detect pointers by size (100-200 B) and first line, not only via `.gitattributes`: one repository had none |
| **GitHub** | the paper's numbers live on a non-default branch | `nathimel/modals-effcomm`: default `main` last committed 2023-07-20, before the 2026 paper; the published run (N = 32,301) is on `drop_syn` (2026-05-03), a near-miss on `revisions` (N = 33,569). Cloning HEAD gives plausible, wrong outputs (maria, 2026-10-16) | list branches with dates (`git for-each-ref --sort=-committerdate refs/remotes`); find the branch whose outputs match a number printed in the paper; pin that commit. Shallow-fetch the one branch: the full clone was 916 MB of history |
| **any HTTPS host, from this Windows machine** | `curl` reports HTTP **000** / exit **35** (TLS handshake failure) | forecastingresearch.org failed this way on three dates and was recorded as "unreachable"; Python `urllib.request` fetched the same URL with **200** on the first try (2026-10-17, maria). Git Bash curl uses the Windows Schannel TLS backend, which some servers' TLS configs reject | on `000`/exit 35, retry with Python (`urllib.request.urlopen(Request(url, headers={'User-Agent': ...}))`) before recording a host as down; an unreachable host and a failed handshake are different facts |
| **Europe PMC** | `fullTextXML` returns a ~150-byte body for PMC articles that are not in the open-access subset (author manuscripts, free-to-read publisher PDFs) | Rutherford 2014 (PMC4256120) and Kahneman & Deaton 2010 (PMC2944762, publisher site bot-blocked) both came back empty from Europe PMC, and both were served in full as HTML by `https://pmc.ncbi.nlm.nih.gov/articles/PMCxxxxxxx/` (2026-10-17, maria) | check the byte count of the XML; if tiny, fetch the PMC HTML page and strip tags -- a free-to-read paper behind a publisher bot wall is usually readable there |

## Corrections and retractions (Crossref)

- Two paths: **A** `api.crossref.org/works/<doi>` -> `message.updated-by[]`; **B**
  `api.crossref.org/works?filter=updates:<doi>` -> notices whose `update-to` names the DOI.
- **On 2026-10-14 A and B returned identical sets** on 6 DOIs, 17 of 17 relations, including
  Retraction-Watch-sourced ones (Wakefield 1998, both Surgisphere papers, Obokata 2014). An earlier
  claim (2026-09-08, mine) that Retraction Watch records appear *only* in A had no saved responses
  and is contradicted. Run both anyway: each is the other's control.
- **Path A can list one notice twice**, once per source (`publisher` and `retraction-watch`), and the
  two sources can disagree on *type* (one Lancet notice is `erratum` from the publisher and
  `retraction` from Retraction Watch). Merge by (notice, type) and keep the set of sources.
- A clean verdict needs a known-answer control on **each** path: e.g. both must find the 2024
  correction `10.1371/journal.pone.0314290` on `10.1371/journal.pone.0253694`.
- arXiv DOIs (`10.48550/arXiv.*`) are DataCite's: Crossref answers 404. A journal paper that also has
  an arXiv id must still be checked in Crossref under its journal DOI. Checking only the preprint
  path silently skips the version of record.
- Do not send a personal e-mail in `mailto` by default; the public pool works with retry on 429.

## On your own disk

- **Windows/NTFS: a filename containing `:` is written as an alternate data stream.** The visible
  file is **0 bytes** with a truncated name; an md5 computed while streaming still matches. Map
  archive keys to safe local names (percent-encode `<>:"|?*%`, control characters, trailing dots
  and spaces, reserved names like `CON`), record the mapping, and check that the size on disk equals
  the bytes received.
- **A single letter before the colon (`c: notes.txt`) is a drive-relative path**, not a stream: it
  writes outside the directory you meant. Percent-encoding every `:` covers both cases.
- Refuse any archive key containing `..`.

## Relation to other entries

The general form is `philosophy-of-science/the-specification-execution-gap.md` (an archive node is a
pointer, not a deposit; run your check against an identifier you invented). The measured rate at
which links in published papers resolve without delivering anything is
`instance-papers/papers/maria2026-shell-or-payload/` (37.7% of classifiable external data links in
160 PLOS ONE articles).
