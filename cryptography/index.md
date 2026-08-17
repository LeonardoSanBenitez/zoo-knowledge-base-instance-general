# cryptography — index

Applied cryptography and TLS *libraries* — their APIs, versioning, defaults and community
practice. Not the mathematics of the primitives (that belongs with formal-methods /
optimization if it ever arrives), and not protocol specifications for their own sake.

Format per line: `[status] path — one-line summary — why it matters / to whom`

---

## openssl/

- `active` `openssl/INDEX.md` — index and retrieval contract for the OpenSSL entries:
  header format, the fact that `labels` reuse OpenSSL's own GitHub labels, and lookup via
  `tools/kb_lookup.py --repo openssl/openssl`. Read before adding an OpenSSL entry.

- `active` `openssl/openssl-2026-snapshot.md` — what a remembered (3.0–3.2-era) OpenSSL
  answer gets wrong in 2026: computed support/EOL table (3.1/3.2/3.3 are EOL; 3.0's LTS
  ends 2026-09-07; 3.5 is the current LTS), the 4.0 removal list (engines, SSLv3,
  `c_rehash`, opaque `ASN1_STRING`, no `atexit()` cleanup), 3.5's changed TLS defaults
  (hybrid PQC keyshares) and 3.6's C99 requirement, the four community surfaces, and the
  project's AI-contribution policy — relevant to anyone answering an OpenSSL question or
  reading a TLS interop regression, and to anyone looking for a well-drafted precedent on
  AI disclosure in a security-critical project.
