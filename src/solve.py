import streamlit as st
from visualizer import Visualizer
from PopularArborescence import PopularArborescence


@st.cache_data
def solve(
    input: str,
) -> tuple[
    bool, list[tuple[int, set[tuple[int, int]], set[tuple[int, int, int]], set[tuple[int, int]], list[set[tuple[int, int]]]]], dict[tuple[int, int], int]
]:
    input = input.splitlines()
    n, m = map(int, input[0].split())
    edges = set()
    weight = {}

    # Assuming you have a Visualizer class defined somewhere.
    # vis = Visualizer(n)

    for i in range(m):
        s, t, w = map(int, input[i + 1].split())

        # Ignore edges that go to the root
        if t == 0:
            continue

        edges.add((s, t))
        weight[(s, t)] = w
        # vis.add_edge(s, t)

        # vis.change_color(s, t, c(w))

    # Comparison function
    def comp(a: tuple[int, int], b: tuple[int, int]) -> bool:
        return weight[a] > weight[b]

    # comp = lambda a, b: weight[a] > weight[b]

    # Call to popular_arborescence function
    res = PopularArborescence(n, edges, comp).solve()

    return (res[0], res[1], weight)


# if __name__ == "__main__":
#     solve()
