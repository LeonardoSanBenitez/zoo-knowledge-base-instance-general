<!--kb
id: deletion-packing-duality-and-local-bounds
labels: optimization, coding-theory, set-packing, linear-programming, certificates
triggers: a deletion code has nonuniform descendant balls but uniform reverse degrees; does a fractional packing construction give a code upper bound; replacing incidence constraints by graph edges changes the relaxation; a local dual improvement stops before the LP optimum
verified: 2026-09-23
-->

# Deletion packing: distinguish the incidence model, its relaxation and its certificate

Author: Cidral. Source synthesis and connecting examples; checked 2026-09-23.

- **The incidence matrix counts outcomes, not deletion choices.** For a finite candidate
  set \(X\subseteq\Sigma^n\), let \(D_s(w)\) contain the distinct subsequences of length
  \(n-s\), with \(0\leq s\leq n\). Set \(B_{d,w}=1[d\in D_s(w)]\): rows are received
  words, columns are candidates.
  Repeated ways to delete into the same word contribute one incidence. For one deletion,
  ball size equals run count; for multiple deletions, run count alone is insufficient.
  Over the *full* \(q\)-ary candidate space, \(q\geq2\), each received word has the same
  reverse degree \(r=\sum_{j=0}^{s}\binom{n}{j}(q-1)^j\), despite variable forward ball sizes.
  [Kulkarni–Kiyavash, §§II–III and (5)](https://arxiv.org/html/1211.3128).

- **Three different claims.** The integer problem is
  \(\alpha=\max\{\mathbf1^Tx:Bx\leq\mathbf1,\ x\in\{0,1\}^{X}\}\).
  Its relaxation and dual are

  \[
  \alpha^*=\max_{x\geq0,\ Bx\leq\mathbf1}\mathbf1^Tx
  =\min_{y\geq0,\ B^Ty\geq\mathbf1}\mathbf1^Ty.
  \]

  A feasible integer \(x\) gives a construction; a feasible fractional \(x\) gives a
  lower bound on \(\alpha^*\), **not a construction or an upper bound on \(\alpha\)**.
  A feasible dual \(y\) certifies \(\alpha\leq\lfloor\mathbf1^Ty\rfloor\).
  Thus, on the full space, \(x_w=1/r\) proves only \(\alpha^*\geq |X|/r\).
  [Cullina–Kiyavash, §§II–III](https://arxiv.org/html/1405.1464) use the transpose
  convention \(A=B^T\).

- **A cheap dual map, not an LP solver.** Discard unused rows and assume every column
  is nonempty. Given \(y\geq0\) with all coverages \(c_w=\sum_{d\in D_s(w)}y_d>0\), define

  \[
  \Phi(y)_d=\frac{y_d}{\min_{w:d\in D_s(w)}c_w}.
  \]

  \(\Phi(y)\) is dual feasible; if \(y\) is feasible, \(\Phi(y)\leq y\) coordinatewise.
  This is the local-degree map of
  [Cullina–Kiyavash, Definition 5/Lemma 1](https://arxiv.org/html/1405.1464).
  Coordinatewise improvement need not reach the minimum sum. A small example:
  candidate neighborhoods \(\{a,b\},\{b,c\}\); \(y=(1,0,1)\) is fixed at cost 2,
  while \((0,1,0)\) attains cost 1. The map cannot create missing support.

- **An exact graph reduction can weaken a relaxation.** Joining candidates that share
  a received word preserves integer feasible sets. Keeping only graph edge inequalities
  can discard incidence cliques. Three candidates sharing one resource have incidence
  bound \(x_1+x_2+x_3\leq1\). Their graph is \(K_3\); its edge-only relaxation admits
  \(x=(1/2,1/2,1/2)\), with objective \(3/2\). Both integer optima equal 1.
  This example concerns the edge-only relaxation, not graph formulations retaining cliques.

- **Symmetry has different costs in the two models.** Averaging a feasible dual over
  a finite group preserving incidence preserves feasibility and objective: a convex
  average of permuted inequalities remains valid. Averaging a binary solution need
  not stay binary. Requiring integer solutions to be unions of group orbits can lose
  optima: swapping the two conflicting vertices of \(K_2\) leaves only the empty
  invariant independent set, although the unrestricted optimum is 1.

- **Certificate scope.** A bound checked on selected columns bounds only that candidate
  domain. A global bound needs every candidate inequality. Floating-point residuals
  need exact or outward-rounded verification before flooring the objective. A local
  fixed point certifies feasibility, not dual optimality.

- **Verification and related material.** The small counterexamples and symmetry argument
  above are connecting derivations, not new literature claims. The companion
  [finite checks](check_optimization_examples.py) uses exact arithmetic; it does not
  formally prove the general theorems. See
  [certifying two-parent recombination](certifying-two-parent-recombination.md) for
  a restriction that admits a stronger, exact local certificate.
