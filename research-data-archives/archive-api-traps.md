<!--kb
id: research-archive-api-traps
labels: research-data, archives, reproducibility, osf, zenodo, figshare, dataverse, crossref, retraction, git-lfs, checksums, link-rot
triggers: download a dataset from OSF; does this OSF link have files; OSF node is empty; verify Zenodo checksum; Zenodo concept DOI; figshare file count zero; figshare embargo; Dataverse checksum mismatch; Dataverse csv tab; is this paper retracted; Crossref updated-by; Retraction Watch in Crossref; check correction to a paper; git lfs pointer 134 bytes; is this data link dead; 410 vs 404; file written as 0 bytes on Windows; colon in filename Windows
verified: 2026-10-14
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
| OSF | child components | a parent can be empty while its children hold everything | list `/children/`; the children are separate GUIDs |
| **figshare** | unversioned id floats | `/articles/<id>` and `m9.figshare.<id>` are the newest version | require `.v<N>`; fetch `/articles/<id>/versions/<N>` |
| figshare | zero files, three different reasons | `embargo_type: file` + `embargo_date` (one "Analysis code for:" deposit embargoed to 2027-10-13); `is_metadata_record: true` (no files by design); or unexplained. **7 of 40** public search hits on 2026-10-14 listed zero files | say which; none of them is "broken" |
| figshare | two md5s | `computed_md5` (figshare's, of what it holds) vs `supplied_md5` (uploader's) | check against `computed_md5`; if the two disagree, that is a claim about the deposit |
| figshare | `is_link_only` | the "file" is a link elsewhere; figshare holds no bytes | not fetched, not verified |
| figshare | file list size | the article endpoint embedded all 491 files of one deposit (matched `/files?page_size=1000`) | no truncation seen; not a guarantee |
| **GitHub LFS** | pointer served as content | `raw.githubusercontent.com` answers 200 with a ~134-byte pointer while `media.githubusercontent.com` answers 404 (a 335 MB object) | detect pointers by size (100-200 B) and first line, not only via `.gitattributes`: one repository had none |

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
