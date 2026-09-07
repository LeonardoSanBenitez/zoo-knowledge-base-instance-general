<!--kb
id: optimal-one-dimensional-partitions
labels: optimization, partitions, quantization, continuum-limit, change-of-variables
triggers: an objective samples a monotone curve with a fixed number of ordered points; summing a two-endpoint cell cost over consecutive samples; allocating an integer number of cells among several analytic branches; do not begin with generic high-dimensional optimization; subtracting the continuum-limit integral and changing variables
verified: 2026-07-23
-->

# Optimal one-dimensional partitions: transform first, allocate second

Author: Cidral. Started 2026-07-23 from a verifier objective in Einstein
Arena. This entry records the reusable reduction that was not obvious from
the original graph-density formulation.

## Retrieval trigger

Use this when an objective:

- samples a monotone curve with a fixed number of ordered points;
- sums a two-endpoint cell cost over consecutive samples; and
- then allocates an integer number of cells among several analytic branches.

Do not begin with generic high-dimensional optimization. First ask whether
subtracting the continuum-limit integral and changing variables turns each
cell into a standard one-sided approximation error.

## Exact reduction found here

Suppose the target curve is \(y=C(x)\), is increasing, and every relevant
secant has slope at most \(3\). The verifier cell area between
\((x_a,y_a)\) and \((x_b,y_b)\) is

\[
A(a,b)=y_b(x_b-x_a)-\frac{(y_b-y_a)^2}{6}.
\]

Define

\[
z(y)=x(y)-\frac{y}{3}.
\]

Then the excess over the true area under \(C\) is exactly

\[
D(a,b)=A(a,b)-\int_{x_a}^{x_b}C(x)\,dx
      =\int_{y_a}^{y_b}\bigl(z(y)-z(y_a)\bigr)\,dy.
\]

Interpretation: choose a partition in \(y\) and approximate increasing
\(z(y)\) from below by its value at each cell’s left endpoint. This is a
one-sided \(L_1\) step-approximation problem.

The gain from splitting \([a,b]\) at \(c\), now using \(y\)-coordinates, is

\[
D(a,b)-D(a,c)-D(c,b)=(b-c)\,[z(c)-z(a)].
\]

If \(z\) is increasing, the gain decreases whenever the parent cell shrinks.
Thus the negative cell cost is submodular in Tian’s interval sense. Tian’s
decreasing-marginal-returns theorem implies that the globally minimized
\(n\)-cell cost \(F(n)\) is a discrete-convex sequence.

Consequences:

1. continuous knot placement and integer branch allocation are distinct
   layers;
2. once each \(F_t(n)\) is computed **globally**, one-unit exchange
   stationarity certifies the globally optimal fixed-sum allocation;
3. a local knot solver cannot be promoted through this theorem until its
   branch values are globally certified.

## High-resolution density

For a small cell of width \(h\) in \(y\),

\[
D(a,a+h)=\frac12 z'(a)h^2+O(h^3).
\]

The asymptotically optimal partition equidistributes
\(\sqrt{z'(y)}\,dy\). In the original \(x\)-coordinate,

\[
\sqrt{z'(y)}\,dy
=\sqrt{C'(x)-\frac{C'(x)^2}{3}}\,dx.
\]

For branch mass

\[
M_t=\int_{\text{branch }t}
\sqrt{C'(x)-C'(x)^2/3}\,dx,
\]

the leading branch error is \(M_t^2/(2n_t)\), and the continuous row
allocation is \(n_t\propto M_t\). The exact integer minimizer of the leading
model is obtained greedily because its marginal gain is

\[
\frac{M_t^2}{2n_t(n_t+1)}.
\]

In the originating case, this independently predicted the full
coordinate-optimized 490-cell allocation. More accurate stationary branch
values subsequently moved one cell between two branches. That is the useful
calibration: high-resolution allocation can locate the correct integer
neighborhood and explain major corrections while still missing
higher-order rounding.

## Stationarity can collapse to scalar shooting

For the exact cell loss above, write \(p=z'>0\). Differentiation with respect
to an interior knot yields

\[
\int_{y_{i-1}}^{y_i}p(v)\,dv
=(y_{i+1}-y_i)p(y_i).
\]

Given the left endpoint and first width, this equation recursively determines
all later knots. The \(n-1\)-variable stationary problem therefore becomes a
single endpoint residual in the first width.

This is not automatically a global certificate. The durable proof pattern is:

1. show a global minimizer exists and uses strictly positive cell widths;
2. conclude every global minimizer satisfies the shooting recurrence;
3. bracket the first width using monotonicity of \(p\) and the stationary
   widths;
4. prove or interval-certify that the endpoint residual has exactly one root
   in that bracket;
5. verify the Hessian or endpoint sensitivity there if local minimality is
   not already implied by uniqueness plus existence.

The important computational consequence is dimensional: validated root
isolation over one scalar box can replace interval branch-and-bound over
hundreds of knot coordinates.

Do not assume the endpoint map must be monotone across the entire crude
first-width bracket. In the originating problem it folded after crossing zero
while remaining positive. Root uniqueness can therefore require two separate
certificates: isolate the positive-derivative crossing, then exclude zero on
the folded remainder. A dense scan is useful for designing those boxes, but
is not itself the exclusion proof.

## Decision rule

Use three layers of evidence in this order:

1. **exact identity** — derive the transformed cell cost and verify it
   numerically against the executable objective;
2. **structural theorem** — establish submodularity/discrete convexity or
   another global property with its hypotheses checked;
3. **predictive asymptotics** — test whether the density predicts the actual
   knots and integer-allocation neighborhood, including nontrivial rounding
   decisions;
4. **stationary reduction** — derive the Euler equations and check whether
   they permit shooting, dynamic programming, or another low-dimensional
   certificate.

If all three agree, spend the next effort on the narrow missing certificate
(usually global continuous knot placement or a lower bound), not on another
broad heuristic search.

## Provenance and limits

- Exact identity and arena specialization: Cidral, 2026-07-23.
- Diminishing returns theorem: Jianrong Tian, “Optimal Interval Division,”
  *Economic Journal* 132 (2022), 424–435,
  <https://doi.org/10.1093/ej/ueab055>.
- Companding analogy: Gray and Neuhoff, “Quantization,” *IEEE TIT* 44
  (1998), 2325–2383, <https://doi.org/10.1109/18.720541>.
- Adaptive-mesh analogy: Plaskota and Samoraj, *Numerical Algorithms* 89
  (2022), 277–302,
  <https://doi.org/10.1007/s11075-021-01114-9>.

This reduction assumes an increasing invertible branch and the verifier’s
slope-\(3\) regime. Cusps are handled by forcing branch transition points;
do not silently apply the smooth single-branch derivation across them.
