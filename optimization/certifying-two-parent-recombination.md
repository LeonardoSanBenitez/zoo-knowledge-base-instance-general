<!--kb
id: certifying-two-parent-recombination
labels: optimization, independent-set, set-packing, recombination, certificates
triggers: can two feasible solutions be merged optimally without global search; independently verify an optimal crossover or matching certificate; parents are very different but recombination makes no improvement; does bipartite repair still work with three parents
verified: 2026-09-23
-->

# Two-parent recombination: an exact local optimum with a small certificate

Author: Cidral. Primary-source synthesis with explicit certificate boundaries;
checked 2026-09-23.

- **Known result and applicable model.** Optimal recombination preserves coordinates
  where both binary parents agree and chooses between their values elsewhere.
  Maximum-weight independent set has a polynomial-time recombination algorithm;
  unit-capacity set packing inherits the result through its conflict graph.
  [Eremeev (2008), Proposition 1 and Corollary 1](https://ofim.oscsbras.ru/~eremeev/PAPERS.MAT/Eremeev_EC_web.pdf),
  DOI [10.1162/EVCO.2008.16.1.127](https://doi.org/10.1162/EVCO.2008.16.1.127).
  Pairwise conflicts must completely characterize feasibility; capacities greater
  than one or other global constraints need a separate argument.

- **Reduction in set notation.** Let \(P,Q\) be independent sets in a simple graph,
  \(U=P\cup Q\), \(C=P\cap Q\), \(L=P\setminus Q\), and \(R=Q\setminus P\).
  Vertices of \(C\) have no neighbors in \(U\), and all remaining edges cross \(L,R\).
  For the resulting bipartite graph \(H\),

  \[
  \max\{|S|:C\subseteq S\subseteq U,\ S\text{ independent}\}
  =|U|-\nu(H),
  \]

  where \(\nu\) is maximum matching size. Each matching edge forces one omission;
  a vertex cover of matching size supplies exactly enough omissions. Isolated
  common vertices remain selected. The equality is a two-parent restriction,
  not a bound on the full graph's independence number.

- **A certificate can be easier to check than to generate.** Reconstruct \(U\) and all
  its conflicts from the original feasibility relation; verify both parents. Check
  that a supplied matching \(M\) has real edges and disjoint endpoints, that a supplied
  \(K\subseteq L\cup R\) covers every edge, and that \(|M|=|K|\). Then \(U\setminus K\)
  is an optimal child. Omitting a conflict from both the solver and its checker can
  invalidate an otherwise internally consistent certificate.

- **Weights require a different certificate.** For nonnegative weights, use a network
  with arcs \(s\to l\) of capacity \(w_l\), \(r\to t\) of capacity \(w_r\), and
  \(l\to r\) of capacity \(W+1\) for conflicts, where \(W=\sum_{v\in L\cup R}w_v\).
  A minimum cut never severs a conflict arc because a cut of capacity at most \(W\)
  exists. If \(S\) is its source side, the cover is
  \((L\setminus S)\cup(R\cap S)\). A feasible flow and cut of equal value certify
  minimum omitted weight; cardinality matching alone does not. Add the unchanged
  common-parent weight to the complementary independent set's weight.

- **Set distance is not complementarity.** Two disjoint parents of size \(m\) have
  symmetric difference \(2m\), whether \(H\) is empty or \(K_{m,m}\). The best children
  have sizes \(2m\) and \(m\), respectively. Cross-conflict structure determines the
  gain. Failure to improve one union leaves other parents and outside candidates open.

- **Two nearby methods have different domains.** Lamm–Sanders–Schulz mix parental vertex
  covers across a two-way graph partition, then repair uncovered boundary edges by
  bipartite matching; later local search can leave the parental union. That restricted
  repair is not the same optimization domain as the full-union formula above.
  [Graph Partitioning for Independent Sets, §3.3](https://arxiv.org/html/1502.01687).
  Three-parent unions need not be bipartite: three singleton parents on a triangle
  have union independence number 1, while \(|U|-\nu=2\).

- **Verification.** [Finite checks](check_optimization_examples.py) independently
  enumerate small graphs, independent sets, matchings, covers and weighted cuts.
  These tests check the displayed constructions and counterexamples, not arbitrary
  solver implementations or a formal proof of the general result. For the distinction
  between integer graph equivalence and LP strength, see
  [deletion packing and duality](deletion-packing-duality-and-local-bounds.md).
