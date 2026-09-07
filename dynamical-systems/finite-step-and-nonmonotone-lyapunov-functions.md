<!--kb
id: finite-step-and-nonmonotone-lyapunov
labels: dynamical-systems, lyapunov, discrete-time, stability, LMI, ISS, switching
triggers: a candidate Lyapunov function is allowed to increase temporarily; can the candidate rise for a few steps; does a weighted average imply a particular iterate decreases; does a strict drop in every window force convergence; can an M-step certificate be made one-step; what changes with disturbances or switching; how should an LMI derived from a window inequality be audited; a finite-horizon inequality is not yet a stability theorem
verified: 2026-08-14
-->

# Finite-step and non-monotone Lyapunov certificates in discrete time

**Author:** cidral  
**Checked/updated:** 2026-08-14

This is a retrieval-oriented map of the distinctions that matter when a
candidate Lyapunov function is allowed to increase temporarily. It is not a
general introduction to Lyapunov theory. The central warning is:

> A finite-horizon inequality is not yet a stability theorem. First identify
> what the inequality actually selects (a fixed terminal time, some time in a
> window, or a path through several functions); then add the hypotheses that
> control all unselected times.

## Route by the question you have

| Question | Go to |
|---|---|
| Can the candidate rise for a few steps? | [Fixed terminal-step decrease](#1-fixed-terminal-step-decrease) |
| Does a weighted average imply a particular iterate decreases? | [Weighted averages](#3-weighted-average-descent-is-a-selection-lemma) |
| Does “some strict drop in every window” force convergence? | [Strict is not uniform](#4-strict-is-not-uniform-a-minimal-counterexample) |
| Can an $M$-step certificate be made one-step? | [Finite-sum bridge](#2-the-finite-sum-bridge-to-one-step-descent) |
| Where do stability between descent times and exponential rates come from? | [Inter-sample control](#5-the-selected-subsequence-is-not-the-whole-trajectory) |
| What changes with disturbances or switching? | [ISS and graph certificates](#6-disturbances-switching-and-multiple-functions) |
| How should an LMI derived from a window inequality be audited? | [Algebraic audit](#7-audit-an-lmi-from-the-scalar-semantics-outward) |

Throughout, $x^+=F(x)$ is an autonomous discrete-time system with equilibrium
$F(0)=0$, $F^j$ is the $j$-fold iterate, and $V\colon X\to\mathbb R_{\geq0}$
is compared with distance to the equilibrium by class-$\mathcal K_\infty$
functions when a global result is intended.

## 1. Fixed terminal-step decrease

The clean finite-step condition has a **fixed** $M\geq1$:

$$
V(F^M x)-V(x)\leq-\alpha(V(x)),
$$

where $\alpha$ is a continuous positive-definite comparison function (a linear-rate version is
$V(F^M x)\leq qV(x)$ with $q<1$). This controls each residue-class subsequence
$V(F^{r+kM}x)$ once the same condition can be applied at every state.

What is still needed depends on the conclusion:

- **Attractivity at sampled times:** comparison bounds for $V$ and a uniform
  positive decrease away from zero.
- **Lyapunov stability and convergence of every iterate:** control of the
  finitely many maps $F^r$, $0\leq r<M$. A standard weak hypothesis is
  $\mathcal K$-boundedness, e.g. $|F(x)|\leq\kappa(|x|)$; continuity at the
  equilibrium is a familiar stronger condition.
- **Global conclusions:** proper/radially unbounded comparison bounds, or an
  equivalent mechanism preventing escape between sampled times.
- **Exponential conclusions:** quantitative comparison bounds and a linear
  contraction, not merely pointwise strictness.

Geiselhart, Gielen, Lazar and Wirth prove finite-step decrease sufficient for
global asymptotic stability under $\mathcal K$-bounded dynamics, without global
continuity, and give a constructive converse theorem. Their paper is the most
useful terminology anchor: [Systems & Control Letters 70 (2014), 49–59](https://doi.org/10.1016/j.sysconle.2014.05.007).

## 2. The finite-sum bridge to one-step descent

The algebraic core is exceptionally simple. Given a fixed $M$, define

$$
W(x):=\sum_{j=0}^{M-1}V(F^j x).
$$

Then the middle terms telescope:

$$
W(Fx)-W(x)=V(F^M x)-V(x).
$$

Thus a terminal $M$-step decrease for $V$ becomes a one-step decrease for
$W$. This identity is unconditional; calling $W$ a classical Lyapunov
function is not. Positivity is inherited from the $j=0$ summand, but
continuity, properness, and upper comparison bounds require corresponding
properties of $V$ and the finite iterates of $F$. This is the finite-sum
construction in the 2014 converse theorem above.

Two frequent overclaims are worth blocking explicitly:

1. A **variable** selected time $\ell(x)\in\{1,\dots,M\}$ does not fit this
   telescoping identity without augmenting the state or defining a new closed
   loop.
2. An inequality involving a weighted sum of future $V$-values does not imply
   that the terminal value $V(F^M x)$ decreases.

## 3. Weighted-average descent is a selection lemma

Suppose $\sigma_i\geq0$, $\sum_{i=1}^M\sigma_i\geq1$, and

$$
\sum_{i=1}^M\sigma_i V(x_i)\leq(1-\alpha)V(x_0),
\qquad 0<\alpha<1.
$$

Then there exists at least one $\ell\in\{1,\dots,M\}$ such that

$$
V(x_\ell)\leq(1-\alpha)V(x_0).
$$

Indeed, if every future value were larger than the right-hand threshold, their
weighted sum would be larger than that threshold times
$\sum_i\sigma_i\geq1$. This conclusion is existential: it identifies a
descent time, not necessarily $M$.

To make this into a controller or a dynamical theorem, one must define the
selection rule (for example, implement the predicted controls through the
first or best admissible $\ell$) and prove that the resulting variable-step
process is recursively feasible. This is exactly the role played by the
flexible-step selection in Fürnsinn, Ebenbauer and Gharesifard's
[generalized-Lyapunov MPC](https://arxiv.org/abs/2211.02780), published in
*Automatica* in 2025.

The weights have another, separate role. If every $\sigma_i>0$, then

$$
V(x_i)\leq\frac{1-\alpha}{\sigma_i}V(x_0).
$$

This supplies a finite-window overshoot bound. If zero weights are permitted,
the corresponding stages are completely unconstrained by the average. If the
weights vary with state, a lower-control condition on
$\min_i\sigma_i(x)$ is needed for uniform trajectory bounds. Kolsi,
Ebenbauer, Gharesifard and Suttner make this explicit in their 2026
state-dependent-weight framework: besides average contraction they impose a
comparison bound involving $\min_i\sigma_i(x)$ and a further growth condition
for exponential stability ([Definition 2 and Theorem 1](https://arxiv.org/html/2605.03726)).

Hence keep three statements separate:

$$
\text{average inequality}
\Rightarrow\text{existence of a descent index}
\xRightarrow[\text{policy}]{\text{implement }\ell}
\text{contracting sampled closed loop}
\xRightarrow[\text{in-window bounds}]{}
\text{full-trajectory stability}.
$$

## 4. Strict is not uniform: a minimal counterexample

“There is a strict drop” is weaker than “there is enough drop to force the
limit to zero.” The numerical sequence $v_n=1+1/(n+1)$ decreases strictly at
every step but converges to $1$.

This is realizable as a discrete dynamical counterexample if continuity is
omitted. Let

$$
X=\{0,1\}\cup\{1+1/(n+1):n\in\mathbb N\}\subset\mathbb R,
$$

set $F(0)=0$, $F(1)=0$, and
$F(1+1/(n+1))=1+1/(n+2)$, and take $V(x)=|x|$. Then
$V(Fx)<V(x)$ for every $x\neq0$, but the trajectory beginning at $2$ converges
to $1$, not to the equilibrium. The failure is concentrated at the
discontinuity of $F$ at the accumulation point $1$.

This example diagnoses why standard theorems ask for a quantitative positive
definite decrement, or derive one from continuity plus compact annuli. On a
compact annulus, a continuous strictly positive decrement has a positive
minimum. Without compactness/continuity/uniform comparison, pointwise
strictness can decay to zero away from the target.

The same warning applies to “at least one strict drop in every $M$-window.” It
creates a decreasing selected subsequence, but only uniform descent or a
comparison-function argument forces its limit to be zero.

## 5. The selected subsequence is not the whole trajectory

Let sampling times satisfy $t_{k+1}-t_k\leq M$ and
$V(x_{t_{k+1}})\leq qV(x_{t_k})$, $q<1$. Then sampled values decay
geometrically. To transfer this to all $t$, seek a uniform finite-window bound

$$
V(x_{t_k+j})\leq C\,V(x_{t_k}),\qquad 0\leq j\leq M.
$$

It immediately yields

$$
V(x_t)\leq Cq^{\lfloor t/M\rfloor}V(x_0).
$$

This elementary decomposition is often the shortest way to audit a claimed
exponential theorem: locate the sampled contraction and locate the overshoot
constant. If either is only statewise rather than uniform, the advertised
global rate does not follow.

For uncontrolled systems, $\mathcal K$-boundedness of $F$ propagates bounds
across the finite window. For controlled systems, a small-control property,
bounded feasible controls, or a direct predicted-state bound serves the same
logical purpose. Recent flexible-step work replaces or reshapes these
hypotheses, but does not eliminate this obligation.

## 6. Disturbances, switching, and multiple functions

### Finite-step ISS

With input $u$, a dissipative finite-step ISS inequality has the form

$$
V(x_M)-V(x_0)\leq-\alpha(V(x_0))+\gamma(\|u\|_\infty).
$$

Under $\mathcal K$-bounded dynamics this is not merely sufficient: finite-step
ISS Lyapunov functions characterize ISS in the framework of Geiselhart and
Wirth ([arXiv:1406.3224](https://arxiv.org/abs/1406.3224)). For nonlinear
switched systems, max-, implication-, and dissipative-form finite-step
certificates are equivalent to uniform ISS with respect to a measurement
function under a uniform $\mathcal K$-boundedness assumption
([Noroozi et al., IFAC 2020, Theorem 1](https://ifatwww.et.uni-magdeburg.de/ifac2020/media/pdfs/3745.pdf)).

The disturbance term changes the target conclusion: outside the input-sized
region there is descent; inside it, the gain determines the ultimate bound.
Dropping $\gamma$ when translating an ISS certificate back to an autonomous
claim is safe only after setting the input identically to zero.

### Path-complete and graph Lyapunov functions

For switching, non-monotonicity may be distributed across several functions.
A labeled graph encodes inequalities such as
$V_a(x)\geq\gamma V_b(A_i x)$; path-completeness guarantees that every
switching word is covered. This is neither a weighted-window certificate nor a
single fixed-$M$ terminal certificate, although graph paths can induce
multi-step inequalities. The original framework is Ahmadi, Jungers, Parrilo
and Roozbehani's [path-complete graph method](https://doi.org/10.1137/110855272).

A recent structural result studies when graph certificates dominate one
another through composition lifts, refutes a natural conjecture about that
ordering, and uses the counterexample to motivate refined graph constructions: Jongeneel and Jungers
([arXiv:2503.18189](https://arxiv.org/abs/2503.18189)). The reusable lesson is
that “more graph edges/functions” is not by itself a proof of a stronger
certificate; domination needs an explicit lift or implication.

## 7. Audit an LMI from the scalar semantics outward

When a quadratic candidate $V(x)=x^\top Px$ turns a window condition into an
LMI, audit in this order:

1. **Write the scalar inequality first.** Mark which terms are current,
   intermediate, and terminal, and which are multiplied by weights.
2. **Move every term to one side before lifting.** A future term moved across
   the inequality changes sign. Most block-matrix sign errors are already
   visible here.
3. **Substitute the dynamics explicitly.** For a linear trajectory,
   $x_i=\Phi_i x_0$ gives $V(x_i)=x_0^\top\Phi_i^\top P\Phi_i x_0$.
4. **Only then use a Schur complement or auxiliary variables.** State which
   block is assumed positive/negative definite; the equivalence fails if that
   block is singular or has the wrong sign.
5. **Stress-test degenerate weights.** Put all weight on one stage, let a
   permitted weight be zero, and reduce to $M=1$. The LMI must reduce to the
   intended scalar condition in each case.
6. **Test a scalar system.** For $x^+=ax$ and $V(x)=px^2$, every claimed matrix
   implication collapses to a one-line inequality in $a,p$ and the weights.
   This catches sign reversals more reliably than a random high-dimensional
   numerical test.

A positive-semidefinite block matrix is a certificate only for the precise
quadratic form it represents. It cannot repair a mismatch between a weighted
average, a selected intermediate iterate, and a terminal-step claim.

## 8. Literature map and what is actually new

| Source | Mechanism | Reusable contribution |
|---|---|---|
| [Ahmadi–Parrilo, CDC 2008](https://doi.org/10.1109/CDC.2008.4739402) | non-monotone/average decrease | Early systematic sufficient conditions and construction of a monotone certificate from a non-monotone one. |
| [Geiselhart et al., SCL 2014](https://doi.org/10.1016/j.sysconle.2014.05.007) | fixed finite-step decrease | Constructive converse theorem and finite-sum bridge under weak $\mathcal K$-boundedness. |
| [Geiselhart–Wirth, 2015/2016](https://arxiv.org/abs/1406.3224) | finite-step ISS | Necessity and sufficiency for ISS; relaxed small-gain conditions. |
| [Noroozi et al., 2019](https://arxiv.org/abs/1908.09660) | finite-step control LF | Contractive multi-step MPC with and without reoptimization. |
| [Fürnsinn et al., 2024 preprint / 2025 journal](https://arxiv.org/abs/2211.02780) | constant-weight average descent | Flexible-step MPC: average descent selects the number of controls actually implemented. |
| [Fürnsinn et al., v2 2025](https://arxiv.org/abs/2404.07870) | switched linear/LMI construction | Applies generalized CLFs to switched linear systems that lack a quadratic common Lyapunov function. |
| [Pietschner et al., 2025](https://arxiv.org/abs/2510.00961) | unknown LTI systems | Couples flexible-step descent with online learning/exploration; convergence does not require an initial full identification phase. |
| [Jongeneel–Jungers, v2 2025](https://arxiv.org/abs/2503.18189) | path-complete graph certificates | Studies comparison by composition lifts, refutes a conjecture about that ordering, and derives graph refinements from the failure. |
| [Kolsi et al., 2026](https://arxiv.org/abs/2605.03726) | state-dependent weighted descent | Adds state-dependent weights and explicit comparison/growth conditions for global generalized exponential stability. |

The post-2024 development is therefore not a new proof that “average descent
alone implies stability.” It is a sequence of increasingly explicit closed-loop
constructions: how the descent index is selected, how feasibility persists,
how intermediate growth is bounded, and how rates survive state-dependent
weights or online model learning.

## 9. Compact proof-audit checklist

Before accepting a relaxed Lyapunov theorem, answer all nine:

1. Is the horizon fixed, bounded, or state-dependent?
2. Does the hypothesis control the terminal value, a maximum, a sum/average,
   or merely one existentially selected value?
3. If a descent index is existential, what policy selects and implements it?
4. Is the decrease quantitative and uniform away from the target, or merely
   strict pointwise?
5. What bounds every intermediate state/value between descent times?
6. Are the comparison bounds local/global and proper/radially unbounded where
   required?
7. Are continuity, compactness, invariance, or $\mathcal K$-boundedness used at
   the exact step where uniformity is inferred?
8. For ISS, where is the input gain and what norm of the input appears?
9. For an LMI, does the scalar $1\times1$ specialization say the same thing as
   the prose theorem?
