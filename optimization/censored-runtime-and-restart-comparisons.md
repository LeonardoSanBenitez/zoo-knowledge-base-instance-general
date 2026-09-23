<!--kb
id: censored-runtime-and-restart-comparisons
labels: optimization, randomized-algorithms, benchmarking, censoring, restarts
triggers: compare randomized search when some runs time out; estimate time to target rather than the average successful runtime; choose restart budgets when initialization is expensive; pooling easy and hard instances appears to favor restarts; compare GPU batching with independent search replicas
verified: 2026-09-23
-->

# Timeouts, restarts and the runtime quantity actually being estimated

Author: Cidral. Cross-source synthesis and cost-model derivations; checked 2026-09-23.

- **A timeout is partial information.** For first verified target-hitting time \(T\)
  and cutoff \(\tau\), record \(Y=\min(T,\tau)\) and success indicator
  \(\delta=1[T\leq\tau]\). On failure, \(Y=\tau\) is a lower bound, not a completed
  runtime. Dropping failures and treating caps as completed runtimes answer different,
  generally biased questions about \(T\). Hutter–Hoos–Leyton-Brown explicitly model
  right-censored observations when configuring algorithms; adaptive censoring requires
  retaining the censoring information.
  [Bayesian Optimization With Censored Response Data, §§1–3](https://ada.liacs.nl/papers/HutEtAl13b.pdf).

- **Separate two experimental questions.** A fixed budget measures attained quality;
  a fixed target measures time until attainment. COCO's average runtime statistic is
  \(\sum_iY_i/\sum_i\delta_i\): failed attempts consume budget and successful attempts
  terminate at the target. Its interpretation is cost under simulated restarts,
  not the mean of the original uninterrupted runtime distribution. With no successes,
  the sample ratio is undefined; the experiment has not proved infinite expected time.
  COCO measures function evaluations; translating the statistic to wall time requires
  specifying initialization, verification and scheduling costs.
  [COCO: Performance Assessment, §§2.2, 3.2, 4](https://arxiv.org/html/1605.03560).

- **Restart overhead can reverse the preferred policy.** Assume independent identically
  distributed attempts on a fixed instance and target, fixed cutoff \(\tau\), success
  probability \(p=\Pr(T\leq\tau)>0\), and deterministic setup cost \(h\) paid before
  *every* attempt, including the first. The renewal equation is
  \(E=h+\mathbb E[\min(T,\tau)]+(1-p)E\), hence

  \[
  E=\frac{h+\mathbb E[\min(T,\tau)]}{p}.
  \]

  If overhead is paid only after failures, replace \(h\) in the numerator by
  \((1-p)h\). Example: \(T=1\) or \(100\), each with probability \(1/2\).
  Restarting at 1 costs \(2+2h\); running to completion costs \(50.5+h\).
  The restart advantage disappears at \(h=48.5\). This is a direct cost-model
  derivation, not a measured speedup or a recommendation for a particular cutoff.

- **Universal restarts have a specific theorem behind them.** Luby–Sinclair–Zuckerman
  give the schedule \(1,1,2,1,1,2,4,\ldots\), competitive within a logarithmic factor
  with optimal expected restart time under their unknown-distribution Las Vegas model.
  Independent fresh randomness and a fixed runtime law matter. The result does not
  automatically cover an evolving parent pool, warm-state transfer or expensive GPU
  setup. [Optimal Speedup of Las Vegas Algorithms, Lemma 1 and Theorems 3/5](https://www.cs.utexas.edu/~diz/pubs/speedup.pdf).

- **Pooling can invent a restart benefit.** Hoos–Stützle show that aggregating different
  instances can produce a runtime curve suggesting beneficial cutoffs even when each
  instance has an exponential, memoryless runtime law. Restarting the same difficult
  instance does not redraw an easier instance. Condition comparisons on instance,
  target and initialization policy before deciding what a pooled curve means.
  [Evaluating Las Vegas Algorithms—Pitfalls and Remedies, §4/Figure 4](https://ada.liacs.nl/papers/HooStu13.pdf).

- **Parallel order statistics assume unchanged replicas.** For \(r\) independent
  full-speed replicas with common runtime CDF \(F\),
  \(\Pr(T_{\min}>t)=(1-F(t))^r\). Packing more replicas onto one GPU can change each
  replica's throughput and therefore \(F\); substituting a serial runtime curve into
  this formula need not predict wall-clock performance. Reporting search work and
  elapsed time distinguishes algorithmic progress from execution throughput.

- **The experimental unit survives the implementation.** A thousand checkpoints
  from one run are not a thousand independent runs. Shared parents or adaptive
  selection can also invalidate an IID restart interpretation. State the sampling
  unit and the policy being evaluated; related reasoning is in
  [independence as a hidden premise](../philosophy-of-science/independence-the-hidden-premise-of-agreement.md).
  Choosing a cutoff on pilot data and evaluating it on fresh runs separates policy
  selection from performance estimation. Unequal caps must remain visible; the simple
  ratio above estimates a common restart policy only when attempts follow that policy.

- **Verification.** The setup-cost arithmetic and an exact finite mixture example are
  checked in [the companion](check_optimization_examples.py). The entry does not supply
  a general survival estimator, confidence intervals or a GPU performance model.
