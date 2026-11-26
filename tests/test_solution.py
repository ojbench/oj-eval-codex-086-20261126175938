"""Compare the executable against a recursive, depth-parity reference."""
import random
import subprocess
import sys

sys.setrecursionlimit(10000)
executable = sys.argv[1] if len(sys.argv) > 1 else './build/code'


def check(children, queries):
    n = len(children) - 1
    data = [str(n)]
    data.extend(f'{left} {right}' for left, right in children[1:])
    data.append(str(len(queries)))
    data.extend(map(str, queries))
    result = subprocess.run([executable], input='\n'.join(data) + '\n',
                            text=True, capture_output=True, check=True)
    expected = []
    flipped = [False] * (n + 1)

    def traverse(node, depth, order):
        if node == -1:
            return
        left, right = children[node]
        if flipped[depth]:
            left, right = right, left
        traverse(left, depth + 1, order)
        order.append(node)
        traverse(right, depth + 1, order)

    for k in queries:
        for depth in range(k, n + 1, k):
            flipped[depth] = not flipped[depth]
        order = []
        traverse(1, 1, order)
        expected.append(order)
    actual = [list(map(int, line.split())) for line in result.stdout.splitlines()]
    assert actual == expected, (data, actual, expected)


check([None, [2, 3], [-1, -1], [-1, -1]], [1, 1])
check([None, [-1, -1]], [1] * 100)
check([None] + [[i + 1, -1] for i in range(1, 1024)] + [[-1, -1]],
      [1, 2, 1024, 1023, 1] * 20)
rng = random.Random(2049)
for _ in range(300):
    n = rng.randint(2, 150)
    children = [None] + [[-1, -1] for _ in range(n)]
    slots = [(1, 0), (1, 1)]
    labels = list(range(2, n + 1))
    rng.shuffle(labels)
    for node in labels:
        index = rng.randrange(len(slots))
        parent, side = slots.pop(index)
        children[parent][side] = node
        slots.extend([(node, 0), (node, 1)])
    check(children, [rng.randint(1, n) for _ in range(100)])
print('Passed sample, singleton, maximum-depth chain, and 300 random trees.')
