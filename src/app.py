import streamlit as st
from solve import solve
from make_random import make_random

# left_column, right_column = st.columns(2)

if "input" not in st.session_state:
    st.session_state["input"] = ""
is_sample01 = st.button("Sample01", type="primary")
is_sample02 = st.button("Sample02", type="primary")
is_random = st.button("Random", type="primary")


if is_sample01:
    st.session_state["input"] = open("sample/sample01.txt", "r").read()
if is_sample02:
    st.session_state["input"] = open("sample/sample02.txt", "r").read()
if is_random:
    st.session_state["input"] = make_random()

show_dot_text = st.checkbox("show dot text")
input = st.text_area("Input", key="input", height=200)


if input == "":
    st.text("Please enter input")
    st.stop()

is_found, graphlist, weight = solve(input)
id = st.number_input("ID", value=0, min_value=0, max_value=len(graphlist) - 1)


# Helper functions for color computation
def hex_func(x: int) -> str:
    s = x // 16
    t = x % 16
    s1 = chr(s - 10 + ord("a")) if s >= 10 else chr(s + ord("0"))
    t1 = chr(t - 10 + ord("a")) if t >= 10 else chr(t + ord("0"))
    return s1 + t1


def c(x: int) -> str:
    return f"#{hex_func(255//10*(10-x))}00{hex_func(255//10*(x-1))}"


def make_dot() -> str:
    n, edges, E, I, C = graphlist[id]
    E_ = set((s, t) for _, s, t in E)
    res = "digraph G {\n"
    res += "rankdir=LR;\n"
    # print(len(C))
    for i in range(n):
        res += f'{i} [label="{i}"];\n'
    for s, t in edges:
        for idx, c in enumerate(C):
            if (s, t) in c:
                if (s, t) in I:
                    res += f'{s} -> {t} [color=red, label="{weight[(s, t)], idx}"];\n'
                elif (s, t) in E_:
                    res += f'{s} -> {t} [color=blue, label="{weight[(s, t)], idx}"];\n'
                else:
                    res += f'{s} -> {t} [label="{weight[(s, t)], idx}"];\n'
                break
    res += "}\n"
    return res


dot = make_dot()
if is_found:
    st.text("Popular arborescence founded.")
else:
    st.text("No popular arborescence.")
st.text("red: I, blue: E")
with st.container():
    st.graphviz_chart(dot)
if show_dot_text:
    st.text(dot)
st.text("Done.")
