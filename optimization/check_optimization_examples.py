"""Finite checks for the adjacent packing, recombination and restart entries.

Run with Python 3; standard library only. Exhaustive finite checks are not proofs
of the general literature results. No project data or solver library is used.
"""

from fractions import Fraction as F
from itertools import combinations, product
from math import comb
from time import perf_counter
import json


def subsets(items):
    items = tuple(items)
    for size in range(len(items) + 1):
        yield from combinations(items, size)


def independent(vertices, edges):
    return all(not (a in vertices and b in vertices) for a, b in edges)


def covering(vertices, edges):
    return all(a in vertices or b in vertices for a, b in edges)


def matching_size(edges):
    return max(
        len(chosen)
        for chosen in subsets(edges)
        if len({v for edge in chosen for v in edge}) == 2 * len(chosen)
    )


def check_recombination():
    graph_cases = 0
    for left_n, right_n in product(range(4), repeat=2):
        n = left_n + right_n
        possible = tuple(product(range(left_n), range(left_n, n)))
        vertex_sets = [set(vs) for vs in subsets(range(n))]
        for edge_tuple in subsets(possible):
            edges = set(edge_tuple)
            nu = matching_size(edges)
            alpha = max(len(vs) for vs in vertex_sets if independent(vs, edges))
            covers = [vs for vs in vertex_sets if covering(vs, edges)]
            cover = min(covers, key=len)
            assert alpha == n - nu and len(cover) == nu
            assert independent(set(range(n)) - cover, edges)
            # An isolated common-parent vertex must remain in the optimum.
            assert max(
                len(vs) for vs in subsets(range(n + 1))
                if n in vs and independent(set(vs), edges)
            ) == alpha + 1
            graph_cases += 1

    weighted_cases = 0
    left, right = {0, 1}, {2, 3}
    vertex_sets = [set(vs) for vs in subsets(range(4))]
    for edge_tuple in subsets(product(left, right)):
        edges = set(edge_tuple)
        for weights in product(range(3), repeat=4):
            total = sum(weights)
            weight = lambda vs: sum(weights[v] for v in vs)
            alpha = max(weight(vs) for vs in vertex_sets if independent(vs, edges))
            cover_cost = min(weight(vs) for vs in vertex_sets if covering(vs, edges))
            # S contains s and the listed vertices, but excludes t.
            cut = lambda s: (
                weight(left - s) + weight(right & s)
                + (total + 1) * sum(a in s and b not in s for a, b in edges)
            )
            source_side = min(vertex_sets, key=cut)
            recovered_cover = (left - source_side) | (right & source_side)
            assert covering(recovered_cover, edges)
            assert cut(source_side) == cover_cost == weight(recovered_cover)
            assert alpha == total - cover_cost
            weighted_cases += 1

    triangle = {(0, 1), (0, 2), (1, 2)}
    assert matching_size(triangle) == 1
    assert max(len(vs) for vs in subsets(range(3))
               if independent(set(vs), triangle)) == 1
    for m in range(1, 4):
        assert matching_size(set(product(range(m), range(m, 2 * m)))) == m
        assert matching_size(set()) == 0
    return {"bipartite_graphs": graph_cases, "weighted_graphs": weighted_cases}


def descendants(word, s):
    return {tuple(word[i] for i in kept)
            for kept in combinations(range(len(word)), len(word) - s)}


def check_packing():
    deletion_cases = 0
    for q in (2, 3):
        for n in range(6):
            words = list(product(range(q), repeat=n))
            for s in range(n + 1):
                reverse_counts = {}
                for word in words:
                    for descendant in descendants(word, s):
                        reverse_counts[descendant] = reverse_counts.get(descendant, 0) + 1
                expected = sum(comb(n, j) * (q - 1) ** j for j in range(s + 1))
                assert len(reverse_counts) == q ** (n - s)
                assert set(reverse_counts.values()) == {expected}
                deletion_cases += 1
            if n:
                for word in words:
                    runs = 1 + sum(a != b for a, b in zip(word, word[1:]))
                    assert len(descendants(word, 1)) == runs
    assert len(descendants((0, 0, 0, 0, 1), 2)) != len(
        descendants((0, 0, 0, 1, 1), 2)
    )

    columns = ({0, 1}, {1, 2})
    coverage = lambda y: [sum(y[d] for d in column) for column in columns]

    def phi(y):
        c = coverage(y)
        return tuple(y[d] / min(c[w] for w in range(2) if d in columns[w])
                     for d in range(3))

    fixed = tuple(map(F, (1, 0, 1)))
    better = tuple(map(F, (0, 1, 0)))
    assert phi(fixed) == fixed and sum(fixed) == 2
    assert min(coverage(better)) == 1 and sum(better) == 1
    local_cases = 0
    for values in product((F(0), F(1, 2), F(1), F(2)), repeat=3):
        if min(coverage(values)) > 0:
            updated = phi(values)
            assert min(coverage(updated)) >= 1
            if min(coverage(values)) >= 1:
                assert all(a <= b for a, b in zip(updated, values))
            local_cases += 1

    half = (F(1, 2),) * 3
    assert all(half[i] + half[j] <= 1 for i, j in combinations(range(3), 2))
    assert sum(half) == F(3, 2) > 1
    k2_independent = [set(vs) for vs in subsets(range(2))
                      if independent(set(vs), {(0, 1)})]
    invariant = [vs for vs in k2_independent if vs == {1 - v for v in vs}]
    assert max(map(len, k2_independent)) == 1
    assert max(map(len, invariant)) == 0
    return {"deletion_parameters": deletion_cases, "local_map_inputs": local_cases}


def check_runtime():
    def restarted(distribution, cutoff, setup=F(0)):
        success = sum(p for t, p in distribution if t <= cutoff)
        consumed = sum(min(t, cutoff) * p for t, p in distribution)
        return (setup + consumed) / success

    distribution = ((1, F(1, 2)), (100, F(1, 2)))
    for h in (F(0), F(10), F(97, 2), F(100)):
        assert restarted(distribution, 1, h) == 2 + 2 * h
        assert restarted(distribution, 100, h) == F(101, 2) + h
    assert restarted(distribution, 1, F(97, 2)) == restarted(
        distribution, 100, F(97, 2)
    )
    # Geometric per-instance laws are memoryless at every tested cutoff.
    ps = (F(1, 2), F(1, 8))
    for p, cutoff in product(ps, (1, 3, 8)):
        consumed = sum((1 - p) ** t for t in range(cutoff))
        success = 1 - (1 - p) ** cutoff
        assert consumed / success == 1 / p
    same_instance_mean = sum(1 / p for p in ps) / 2
    redraw_instance_cost = 1 / (sum(ps) / 2)
    assert same_instance_mean == 5 and redraw_instance_cost == F(16, 5)
    # Three independent replicas of the two-point distribution.
    survival = sum(F(1, 8) for times in product((1, 100), repeat=3) if min(times) > 1)
    assert survival == F(1, 2) ** 3
    return {"overhead_cases": 4, "geometric_instance_cutoffs": 6,
            "mixture_cost_fixed_instance": str(same_instance_mean),
            "mixture_cost_redrawing_instance": str(redraw_instance_cost)}


if __name__ == "__main__":
    if not __debug__:
        raise SystemExit("Run without -O: these finite checks require assertions.")
    started = perf_counter()
    results = {"packing": check_packing(), "recombination": check_recombination(),
               "runtime": check_runtime()}
    results["elapsed_seconds"] = round(perf_counter() - started, 6)
    print(json.dumps(results, indent=2))
