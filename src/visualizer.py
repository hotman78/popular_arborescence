import os


class Visualizer:
    def __init__(self, n: int) -> None:
        self.n = n
        self.id: dict[tuple[int, int], int] = {}
        self.edges: list[tuple[int, int]] = []
        self.color: list[str] = []
        self.style: list[str] = []
        self.penwidth: list[str] = []
        self.idx = 0

    def add_edge(self, s: int, t: int) -> None:
        self.id[(s, t)] = len(self.edges)
        self.edges.append((s, t))
        self.color.append("black")
        self.style.append("dotted")
        self.penwidth.append("1.5")

    def node_name(self, i: int) -> str:
        return f"E{i}"

    def reset_color(self) -> None:
        self.color = ["black"] * len(self.color)

    def reset_style(self) -> None:
        self.style = ["dotted"] * len(self.style)
        # self.penwidth = ["1.5"] * len(self.penwidth)

    def change_color(self, s: int, t: int, c: str) -> None:
        self.color[self.id[(s, t)]] = c

    def change_style(self, s: int, t: int, sty: str) -> None:
        self.style[self.id[(s, t)]] = sty

    def change_penwidth(self, s: int, t: int, val: str) -> None:
        self.penwidth[self.id[(s, t)]] = val

    def vis(self) -> str:
        res = "digraph G {"
        for i in range(self.n):
            res += f'{self.node_name(i)} [label = "{i}", shape = circle];'

        for idx, (s, t) in enumerate(self.edges):
            res += f"{self.node_name(s)} -> {self.node_name(t)} " f'[color="{self.color[idx]}", style={self.style[idx]}, penwidth={self.penwidth[idx]}];'
        res += "}"
        return res

    def out(self) -> None:
        num = str(self.idx).zfill(4)
        self.idx += 1
        path = f"animation/out_{num}.dot"

        # Make sure the 'animation' directory exists
        os.makedirs("animation", exist_ok=True)

        try:
            with open(path, "w") as f:
                f.write(self.vis())
        except IOError:
            print("Could not open file for writing.")
