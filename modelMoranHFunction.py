import argparse
import json

argParser = argparse.ArgumentParser()
argParser.add_argument("-C", "--cycles",
                       help="population structure in cycle notation",
                       default='[[1, 3, 0], [2]]')
argParser.add_argument("-K", "--k", help="h function k parameter",
                       type=int, default=0)

args = argParser.parse_args()


def h(cycles, k):
    p = cycles_to_permutations(cycles)

    if p[k] < k:
        s, s_reversed = create_s_permutations(k)
        swap = [i for i in range(N)]
        swap[p[k]], swap[-1] = swap[-1], swap[p[k]]
        return permutations_composition([swap, s_reversed, p, s])
    elif p[k] > k:
        s, s_reversed = create_s_permutations(p[k])
        swap = [i for i in range(N)]
        swap[k], swap[-1] = swap[-1], swap[k]
        return permutations_composition([s_reversed, p, s, swap])
    else:
        s, s_reversed = create_s_permutations(k)
        return permutations_composition([s_reversed, p, s])



def create_s_permutations(r):
    s = [i for i in range(N)]
    s_reversed = [i for i in range(N)]

    for i in range(r, N-1):
        s[i] = s[i]+1
    s[-1] = r

    for i in range(N):
        s_reversed[s[i]] = i

    return s, s_reversed


def permutations_composition(permutations):
    # composition is done from right to left
    permutations.reverse()

    output_permutation = [i for i in range(N)]
    for i in range(N):
        for p in permutations:
            output_permutation[i] = p[output_permutation[i]]

    return output_permutation


def cycles_to_permutations(cycles):
    output_permutation = [-1 for _ in range(N)]
    for c in cycles:
        c.reverse()
        for i in range(len(c)):
            output_permutation[c[i % len(c)]] = c[(i+1) % len(c)]

    return output_permutation


def permutation_to_cycles(permutation):
    cycles = []
    unused_ids = [i for i in range(N)]

    while unused_ids:
        i = unused_ids[0]
        c = []

        while i not in c:
            c.append(i)
            unused_ids.remove(i)
            i = permutation[i]

        c.reverse()
        cycles.append(c)

    return cycles


def prettier_cycles(cycles):
    return '('+')('.join([''.join([str(i) for i in c])
                          for c in cycles])+')'


if __name__ == '__main__':
    Cycles = json.loads(args.cycles)
    flatten_cycles = [int(i) for c in Cycles for i in c]
    N = max(flatten_cycles) + 1
    k = args.k

    assert len(flatten_cycles) == N, \
        f"Provided permutation is missing an element: " \
        f"max id: {N-1}, number of elements: {len(flatten_cycles)}"
    for i in range(N):
        assert i in flatten_cycles, \
            f"Missing id {i} in received permutation"

    print(f"Input population = {prettier_cycles(Cycles)}")
    print(f"For k = {k},     h = "
          f"{prettier_cycles(permutation_to_cycles(h(Cycles, k)))}")
