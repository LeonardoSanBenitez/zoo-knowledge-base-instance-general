<!--kb
id: reading-stats-package-files-without-the-package
labels: research-data, reproducibility, r, rds, spss, sav, stata, dta, python, pandas, missing-values
triggers: read an R rds file in python; pyreadr invalid file or unsupported features; rdata package NA values; R NA becomes -2147483648; my reanalysis found a huge defect in a deposit; read an SPSS sav file in python; means look one point too high; value labels in pyreadstat; read a Stata dta file in python; string column too long for the reader; no R installed reanalyse an R deposit
verified: 2026-10-23
-->

# Reading a deposit written by R, SPSS or Stata, without R, SPSS or Stata

Status: active. Author: maria. Three traps, each met while reanalysing a published deposit in Python
on a host with no R. Each one produced a plausible wrong number before it produced an error. Records:
`vandam2025-meditation-adverse-effects-representative`, `cebolla2017-unwanted-effects-meditation`,
`gamma2021-mpe92m` (instance-papers).

## The rule that covers all three

**Before believing anything surprising, tabulate the raw values of the column involved.** All three
traps show up at once in a frequency table, and none of them shows up in a summary statistic.

## R `.rds`

| trap | what it looks like | what to do |
|---|---|---|
| `pyreadr` refuses some files | `LibrdataError: Invalid file, or file has unsupported features` (an `.rds` data.frame with matrix-valued columns, e.g. from `scale()`) | use the `rdata` package: `rdata.parser.parse_file` + `rdata.conversion.SimpleConverter` with your own `data.frame` constructor |
| **R's `NA_integer_` arrives as -2147483648** | no error. Every comparison like `x <= 3` counts each NA as true. On one deposit it made a correct imputation look as if it had overwritten 69% of the observed values (62,825 of 91,258 "observed" cells). The real figure was 0 of 27,548. | mask `a == np.iinfo(np.int32).min` to NaN for every integer column before use. (Double columns were not checked; tabulate them too.) |
| the constructor receives a dict | a hand-written constructor that iterates `obj` gets the column NAMES as values, and builds an empty frame | iterate `obj.items()` |
| `(n, 1)` matrix columns | `ValueError: Data must be 1-dimensional` | flatten `a[:, 0]`; split wider matrices into `name.1, name.2, ...` |
| `POSIXct` | warning "Missing constructor for R class POSIXct"; a raw R object comes back | take `.value`, or ignore the timestamp columns |

A working loader is `instance-papers/papers/vandam2025-meditation-adverse-effects-representative/reanalysis/load_rds.py`.

## SPSS `.sav` (`pyreadstat.read_sav`)

Values arrive as **codes**. Labels are in `meta.variable_value_labels`. A 0-10 scale stored as codes
1-11 has every mean one point too high. This is not hypothetical: one published table did exactly
this (cebolla2017, Table 4: "% at minimum" right, means +1 on every item). Print the value labels next to
any mean before comparing it with a printed table.

## Stata `.dta` (`pandas.read_stata`)

- `convert_categoricals=False` gives codes, which are what the analysis works on. The default converts to labels (pandas
  documents that it raises on non-unique value labels; gamma2021's record does not say which reason applied).
- A deposit may ship several Stata versions of one file. In gamma2021 the plain Stata-14 file had a
  string column too long for some readers. The `_R` variant read cleanly. Use the variant the authors
  prepared for other software if there is one.

## Why this belongs in a knowledge base

Every one of these produces a number, not a crash. The `.rds` NA trap came within one step of
being written into a paper record as a defect of the authors' imputation. What stopped it was the rule
above: the change pairs, tabulated, all came from one impossible value. A reanalysis is only as honest
as its reader.
