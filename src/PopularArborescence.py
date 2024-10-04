from collections.abc import Callable
import copy


class UF:
    def __init__(self, n: int) -> None:
        self.parent: list[int] = list(range(n))
        self.rank: list[int] = [0] * n

    def find(self, x: int) -> int:
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]

    def unite(self, x: int, y: int) -> bool:
        root_x = self.find(x)
        root_y = self.find(y)
        if root_x != root_y:
            if self.rank[root_x] < self.rank[root_y]:
                self.parent[root_x] = root_y
            elif self.rank[root_x] > self.rank[root_y]:
                self.parent[root_y] = root_x
            else:
                self.parent[root_y] = root_x
                self.rank[root_x] += 1
            return True
        return False


class PopularArborescence:
    def __init__(self, n: int, edges: set[tuple[int, int]], comp: Callable[[tuple[int, int], tuple[int, int]], bool]) -> None:
        self.n: int = n
        self.edges: set[tuple[int, int]] = edges
        self.comp: Callable[[tuple[int, int], tuple[int, int]], bool] = comp
        self.C: list[set[tuple[int, int]]] = [edges]

    def rank(self, n: int, v: set[tuple[int, int]]) -> int:
        used = [False] * n
        uf = UF(n)
        res = 0
        for s, t in v:
            if uf.unite(s, t):
                used[t] = True
                res += 1

        return res

    def span(self, n: int, v: set[tuple[int, int]], E: set[tuple[int, int]]) -> set[tuple[int, int]]:
        used = [False] * n
        uf = UF(n)
        res = set()

        sz = self.rank(n, v)

        for s, t in E:
            if (s, t) in v:
                res.add((s, t))
                continue
            v.add((s, t))
            if self.rank(n, v) == sz:
                res.add((s, t))
            v.remove((s, t))

        return res

    def intersect(self, s: set[tuple[int, int]], t: set[tuple[int, int]]) -> set[tuple[int, int]]:
        return s & t

    def diff(self, s: set[tuple[int, int]], t: set[tuple[int, int]]) -> set[tuple[int, int]]:
        return s - t

    def Compute_E_C(self) -> set[tuple[int, int, int]]:
        n = self.n
        mx = [-1] * n
        mx1: list[set[tuple[int, int]]] = [set() for _ in range(n)]
        mx2: list[set[tuple[int, int]]] = [set() for _ in range(n)]

        for i, c in enumerate(self.C):
            c_diff = self.diff(c, self.C[i - 1]) if i > 0 else c
            for _, t in c_diff:
                mx[t] = i

        for i, c in enumerate(self.C):
            c_diff = self.diff(c, self.C[i - 1]) if i > 0 else c
            for s, t in c_diff:
                if mx[t] == i:
                    mx1[t].add((s, t))
                if mx[t] == i + 1:
                    mx2[t].add((s, t))

        E: set[tuple[int, int, int]] = set()
        for i in range(n):
            for e in mx1[i]:
                if all(not self.comp(e, e2) for e2 in mx1[i]):
                    E.add((mx[i], e[0], e[1]))

            for e in mx2[i]:
                if all(not self.comp(e, e2) for e2 in mx2[i]) and all(self.comp(f, e) for f in mx1[i]):
                    E.add((mx[i] - 1, e[0], e[1]))
        return E

    def Compute_I(self, E: set[tuple[int, int, int]]) -> set[tuple[int, int]]:
        I = set()
        used = [0] * self.n
        uf = UF(self.n)

        for _, s, t in E:
            if not used[t] and uf.unite(s, t):
                used[t] = 1
                I.add((s, t))

        return I

    def solve(self) -> list[int, tuple[set[tuple[int, int]], set[tuple[int, int, int]], set[tuple[int, int]], list[set[tuple[int, int]]]]]:
        res = []
        g: list[list[int]] = [[] for _ in range(self.n)]
        for s, t in self.edges:
            g[t].append(s)

        p = 1
        res.append((self.n, self.edges, {}, {}, copy.deepcopy(self.C)))

        while p < self.n:
            E = self.Compute_E_C()
            I = self.Compute_I(E)
            k = -1
            res.append((self.n, self.edges, E, I, copy.deepcopy(self.C)))
            for i, c in enumerate(self.C):
                if len(self.intersect(c, I)) < self.rank(self.n, c):
                    k = i
                    break
            if k == -1:
                return res

            self.C[k] = self.span(self.n, self.intersect(I, self.C[k]), self.edges)

            if k + 1 == p:
                p += 1
                self.C.append(self.edges)

        print("Not Found")
        return res
