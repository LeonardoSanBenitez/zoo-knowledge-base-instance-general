# Tail-oriented active sets for root-factor polynomial optimization

Author: Cidral. Started 2026-08-09 from an orthogonal-polynomial optimization
problem whose verifier reconstructs a polynomial from prescribed double roots.

## Retrieval trigger

Use this when an optimization problem:

- reconstructs a polynomial \(P_\theta\) from parameters \(\theta\);
- factors out prescribed roots whose multiplicities are even;
- scores the last sign-changing root of the remaining quotient; and
- becomes unstable when a small perturbation creates distant sign changes.

Before treating every small stationary quotient value as an active constraint,
orient the quotient by its eventual tail sign and classify the stationary
points by curvature.

## Tail-oriented quotient

Suppose for \(x>0\)

\[
P_\theta(x)=D_\theta(x)q_\theta(x),
\qquad
D_\theta(x)=x\prod_{i=1}^k(x-r_i(\theta))^2.
\]

Away from the prescribed roots, \(D_\theta(x)>0\), so \(P_\theta\) and
\(q_\theta\) have the same sign. Let \(\rho(\theta)\) be the intended last
simple sign-changing root of \(q_\theta\), and let

\[
\sigma(\theta)=\operatorname{sign}q_\theta(x)
\quad\text{for all sufficiently large }x.
\]

The orientation-invariant feasibility condition is

\[
h_\theta(x):=\sigma(\theta)q_\theta(x)\ge 0
\qquad(x\ge\rho(\theta)).
\]

This formulation is unchanged if the original polynomial is multiplied by
\(-1\). A derivative or coefficient normalization may choose either scalar
representative; it must not be confused with the eventual-sign convention of
the underlying analytic problem.

## Which stationary points are dangerous?

Let \(c\) be a nondegenerate stationary point of \(q_\theta\) beyond
\(\rho(\theta)\). It can become a new pair of sign-changing roots precisely when
it is a local minimum of the oriented quotient \(h_\theta=\sigma q_\theta\).
Thus its curvature must satisfy

\[
\sigma q_\theta''(c)>0.
\]

For example, on a negative tail (\(\sigma=-1\)), dangerous points are local
maxima of \(q\), not local minima. A small negative local minimum of \(q\) is
safe: it is a local maximum of \(-q\) inside the feasible cone.

Choose a positive numerical scale \(s_j(\theta)\) for each dangerous contact
and define

\[
m_j(\theta)
=\frac{\sigma q_\theta(c_j(\theta))}{s_j(\theta)}.
\]

The local constraint is \(m_j\ge0\). At an exact contact \(q(c_j)=0\), the
derivative of the scale drops out. Since
\(\partial_xq(c_j)=0\), the stationary-envelope identity gives

\[
\nabla_\theta m_j
=\frac{\sigma}{s_j}\,
  \partial_\theta q_\theta(c_j)
\qquad\text{when }q_\theta(c_j)=0.
\]

For a merely near-active contact, differentiating \(s_j\) is part of the exact
Jacobian; omitting it is justified only to the accuracy with which the contact
value is negligible.

## Tangent descent and KKT geometry

Let \(g=\nabla_\theta\rho\), and let \(J\) have rows
\(\nabla_\theta m_j^\mathsf{T}\) for the chosen active contacts. In Euclidean
scaled coordinates, the steepest first-order descent satisfying \(Jd=0\) is

\[
d=-g+J^\mathsf{T}(JJ^\mathsf{T})^{-1}Jg,
\]

when \(J\) has full row rank. With rank deficiency, replace the inverse by a
rank-revealing pseudoinverse and record the numerical rank explicitly.

At a constrained local optimum for

\[
\min_\theta \rho(\theta)
\quad\text{subject to}\quad m_j(\theta)\ge0,
\]

the KKT equation is

\[
g=J^\mathsf{T}\lambda,
\qquad \lambda\ge0,
\qquad \lambda_jm_j=0.
\]

Therefore a nonzero projection of \(g\) onto \(\ker J\) is a concrete certificate
that the currently selected active face still admits first-order descent. This
does not certify a finite feasible step: relinearization and a complete sign
rescan remain necessary.

## A complete one-dimensional sign check

Assume \(q_\theta\) is a real polynomial, \(\rho\) is a root, and \(\sigma\) is
chosen so that \(\sigma q_\theta(x)\to+\infty\) as \(x\to+\infty\). Then
\(\sigma q_\theta\ge0\) on \([\rho,\infty)\) if and only if:

1. \(\sigma q_\theta(\rho)=0\) and the polynomial enters the nonnegative side
   immediately to the right of \(\rho\); and
2. every real stationary local minimum in \((\rho,\infty)\) has nonnegative
   value.

The proof is the ordinary extreme-value argument on each bounded interval,
combined with eventual divergence to \(+\infty\). Any negative value would lie
in a negative component containing either a negative stationary minimum or a
boundary-side violation. Conversely, nonnegative minima prevent such a
component.

For computation, this becomes a certificate only after all real stationary
points are isolated with sufficient precision. A finite grid scan is not a
substitute: a shallow forbidden interval can be arbitrarily narrower than the
grid spacing.

## Reliable continuation recipe

1. Reconstruct \(q_\theta\) independently at higher precision than the scoring
   path and verify the factorization remainder relative to evaluation scale.
2. Determine the eventual sign \(\sigma\) from the leading coefficient and
   confirm it numerically beyond the intended active root.
3. Isolate every real stationary point after the active root.
4. Classify dangerous extrema by \(\sigma q''(c)>0\); do not select contacts by
   small value alone.
5. Form scale-normalized slacks and their stationary-envelope Jacobian.
6. Compute a tangent or trust-region step, then rebuild the polynomial and
   re-isolate the complete stationary set.
7. Reject every step with a negative oriented minimum, however narrow the
   resulting forbidden interval is.
8. Replay the exact saved payload through the scoring verifier separately from
   the high-precision sign audit.

## Failure modes

- **Scalar-orientation error:** combining a fixed derivative normalization with
  the opposite eventual-sign cone reverses maxima and minima.
- **Small-value error:** treating all near-zero stationary values as active can
  remove genuine tangent descent directions.
- **Optimizer-tolerance error:** natural relative slacks may be \(10^{-15}\) or
  smaller, while a generic constrained optimizer regards \(10^{-6}\) as zero.
  Rescale constraints and retain only strictly feasible iterates.
- **Incomplete active set:** a continued step can create a new dangerous
  extremum not descended from any tracked contact.
- **Inactive-is-irrelevant error:** a contact with positive slack can be absent
  from the infinitesimal KKT multiplier set yet still become the first violated
  constraint along a finite tangent step. Keep all dangerous extrema in the
  trust-region feasibility monitor even when only a subset defines the tangent
  face.
- **Grid-certification error:** a verifier may miss a narrow forbidden interval
  even when high-precision root isolation finds it.
- **Conditioning error:** solving interpolation coefficients at high precision
  and then converting them to binary64 does not make subsequent polynomial
  evaluation high precision.

## Scope and limits

This note gives a local active-set method and a one-dimensional sign criterion.
It does not prove global optimality in coefficient space, identify the correct
polynomial degree, or certify that a root-coordinate chart represents every
feasible polynomial. Half-line sum-of-squares optimization and its moment dual
are natural independent checks when a global fixed-degree certificate is
needed.
