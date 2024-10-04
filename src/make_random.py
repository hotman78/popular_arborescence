import random


def make_random() -> str:
    n = random.randint(4, 8)
    m = random.randint(1, n * (n - 1) // 2)
    edges = []
    for i in range(1, n):
        j = random.randint(0, i - 1)
        edges.append((j, i, random.randint(1, 5)))
    for _ in range(m):
        s = random.randint(0, n - 1)
        t = random.randint(0, n - 1)
        while s == t:
            s = random.randint(0, n - 1)
            t = random.randint(0, n - 1)
        edges.append((s, t, random.randint(1, 5)))
    res = f"{n} {len(edges)}\n"
    for s, t, w in edges:
        res += f"{s} {t} {w}\n"
    return res
