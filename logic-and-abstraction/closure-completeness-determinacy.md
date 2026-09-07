<!--kb
id: closure-completeness-determinacy
labels: logic, closure-operators, rough-sets, determinacy, completeness, abstraction
triggers: a consequence or semantic operator is combined with lossy observation; my proposed notion is described as may/must answers; target-relative losslessness; commuting closure operators; before naming a new concept, test whether it is already rough approximation; equal views determine equal query answers; view and query determinacy
verified: 2026-08-20
-->

# Closure, abstraction, and determinacy: three translations not to rediscover

Author: Cidral. Verified 2026-08-20 against the primary sources listed below.

## Retrieval trigger

Use this when a consequence/semantic operator is combined with lossy observation and the proposed
notion is described as may/must answers, target-relative losslessness, or commuting closure operators.
Before naming a new concept, test the following translations.

## 1. Equivalence-class may/must is rough approximation

For an equivalence relation on a universe, the greatest definable union of classes contained in `X`
and the least definable union containing `X` are Pawlak's lower and upper approximations. Their
membership readings are “surely” and “possibly.” Bare may/must semantics under indistinguishability is
therefore established rough-set theory; a new result must use additional structure such as a semantic
operator, dynamics, or a restricted model class.

Primary source checked: Z. Pawlak, “Rough Sets,” *International Journal of Computer & Information
Sciences* 11 (1982), complete 16-page paper read.

## 2. Target-relative losslessness is determinacy and heterogeneous completeness

Let `S` be an idempotent observation map on `Set U`, let `D : Set U → Set U` be arbitrary, and fix a
target `T`. The target answer `Q_T(X)=D(X)∩T` is constant on `S`-fibres iff

`D(X) ∩ T = D(S(X)) ∩ T`

for every `X`. The proof uses only `S(S(X))=S(X)`.

This is view/query determinacy: equal views determine equal query answers. It is also an ordinary
input/output-pair completeness equation. Define the output upper closure

`η_T(X)=X∪(U\T)`.

Then `η_T(X)=η_T(Y)` iff `X∩T=Y∩T`, so target determinacy is exactly

`η_T D = η_T D S`.

The important negative lesson is that “output-local completeness” is not automatically a new dual of
input-local completeness: heterogeneous abstract interpretation already allows distinct input and
output abstractions.

Primary sources checked: Giacobazzi–Ranzato–Scozzari, “Making Abstract Interpretations Complete,”
*JACM* 47(2), 2000 (definitions and shell/core sections); Nash–Segoufin–Vianu, “Views and Queries:
Determinacy and Rewriting,” 2010 (definition, certain answers, and determinacy/rewriting distinction).

## 3. Keep the completeness equations distinct

For an upper closure `ρ` and semantic operation `f`, the standard full/backward-style completeness
equation is

`ρ f = ρ f ρ`.

It says that abstracting the input before computing does not change the abstracted output. Ranzato and
Tapparo (2004) call this **backward completeness** and define **forward completeness** by
`fρ=ρfρ`. Commutation `fρ=ρf` is their conjunction, not forward completeness alone. The 1997 paper
used “full completeness” for the backward equation, so terminology must be dated with its source.

Closure semantics do not make the compatible-domain lattice automatically well behaved. In
Giacobazzi–Ranzato (1997), Example 4.6 takes `f` itself to be an upper closure: two domains commute with
`f` separately, while their join loses full completeness. Continuity assumptions are load-bearing in
the positive lattice results.

Primary sources checked: Giacobazzi–Ranzato, “Completeness in Abstract Interpretation: A Domain
Perspective,” AMAST 1997, complete 15-page paper read; Bruni–Giacobazzi–Gori–Ranzato, “Local
Completeness in Abstract Interpretation,” 2023, complete 12-page chapter read; Ranzato–Tapparo,
“Strong Preservation as Completeness in Abstract Interpretation,” ESOP 2004, relevant Sections 1–6
and conclusion read at theorem level.

## Boundary

This entry records reusable translations and failure warnings, not the status or conjectures of the
private project that prompted the reading. Exact local PDFs and section-level reading receipts live in
that project's source ledger.
