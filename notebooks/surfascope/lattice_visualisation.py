import numpy as np

import plotly.graph_objects as go


def points(V, size=4, color="darkblue", **kwargs):
    return go.Scatter3d(
        x=[v[0] for v in V],
        y=[v[1] for v in V],
        z=[v[2] for v in V],
        marker=dict(size=size, color=color),
        mode="markers",
        **kwargs
    )


def line(v1, v2, color="darkblue", width=2, mode="lines", **kwargs):
    return go.Scatter3d(
        mode=mode,
        x=[v1[0], v2[0]],
        y=[v1[1], v2[1]],
        z=[v1[2], v2[2]],
        line=dict(color=color, width=width),
        **kwargs
    )


def lines(V, name=None, color="darkblue", width=2, **kwargs):
    gen = ((v1, v2) for (v1, v2) in V)
    v1, v2 = next(gen)
    out = [
        line(v1, v2, width=width, color=color, name=name, legendgroup=name, **kwargs)
    ]
    out.extend(
        line(
            v1,
            v2,
            width=width,
            color=color,
            showlegend=False,
            legendgroup=name,
            **kwargs
        )
        for (v1, v2) in gen
    )
    return out


def vectors(lattice, name=None, color="darkblue", width=4, **kwargs):
    gen = zip(lattice, ["a", "b", "c"])
    v, label = next(gen)

    out = [
        line(
            [0, 0, 0],
            v,
            text=["", label],
            width=width,
            color=color,
            name=name,
            legendgroup=name,
            mode="lines+text",
            **kwargs
        )
    ]
    out.extend(
        line(
            [0, 0, 0],
            v,
            text=["", label],
            width=width,
            color=color,
            showlegend=False,
            legendgroup=name,
            mode="lines+text",
            **kwargs
        )
        for (v, label) in gen
    )
    return out


def get_vectors(lattice, name=None, color="darkblue", width=2, **kwargs):
    return lines([[[0, 0, 0], v] for v in lattice], **kwargs)


def get_box(lattice, **kwargs):
    a, b, c = lattice
    segments = [
        [[0, 0, 0], a],
        [[0, 0, 0], b],
        [[0, 0, 0], c],
        [a, a + b],
        [a, a + c],
        [b, b + a],
        [b, b + c],
        [c, c + a],
        [c, c + b],
        [a + b, a + b + c],
        [a + c, a + b + c],
        [b + c, a + b + c],
    ]
    return lines(segments, **kwargs)


def plot_fcc_conv():

    fcc_conv = np.array([[1, 0, 0], [0, 1, 0], [0, 0, 1]])
    fcc_vectors = vectors(
        fcc_conv, name="conv lattice vectors", color="darkblue", width=6
    )
    fcc_box = get_box(fcc_conv, name="conv lattice")

    atoms = points(
        [[0, 0, 0], [0.5, 0.5, 0], [0.5, 0, 0.5], [0, 0.5, 0.5]],
        size=10,
        color="orange",
        name="atoms",
        legendgroup="atoms",
    )

    fig = go.Figure(data=[*fcc_box, *fcc_vectors, atoms])
    return fig


def plot_fcc_prim():
    fcc_prim = np.array([[0.5, 0.5, 0], [0, 0.5, 0.5], [0.5, 0, 0.5]])

    fcc_prim_vectors = vectors(
        fcc_prim, name="prim lattice vectors", color="green", width=6
    )
    fcc_prim_box = get_box(fcc_prim, name="prim lattice", color="green")

    atoms = points(
        [[0, 0, 0], [0.5, 0.5, 0], [0.5, 0, 0.5], [0, 0.5, 0.5]],
        size=10,
        color="orange",
        name="atoms",
        legendgroup="atoms",
    )

    fcc_conv = np.array([[1, 0, 0], [0, 1, 0], [0, 0, 1]])
    fcc_conv_box = get_box(fcc_conv, name="conv lattice")


    fig = go.Figure(data=[*fcc_prim_box, *fcc_prim_vectors, *fcc_conv_box, atoms])

    return fig


def plot_fcc_100():

    # fcc_100_cell = np.array([[0, 0.5, -0.5], [0, 0.5, 0.5], [1.0, 0.0, 0]])
    fcc_100_cell = np.array([[0.5, -0.5, 0], [0.5, 0.5, 0], [0.0, 0, 1.0]])

    fcc_100_vectors = vectors(
        fcc_100_cell, name="100 lattice vectors", color="red", width=6
    )
    fcc_100_box = get_box(fcc_100_cell, name="100 lattice", color="red")

    fig = plot_fcc_conv()
    fig.add_traces([*fcc_100_box, *fcc_100_vectors])

    return fig


def plot_fcc_110():
    fcc_110_cell = np.array([[0, 0.0, 1.0], [0.5, -0.5, 0], [0.5, 0.5, 0.0]])

    fcc_110_vectors = vectors(
        fcc_110_cell, name="reduced lattice vectors", color="red", width=6
    )
    fcc_110_box = get_box(fcc_110_cell, name="reduced lattice", color="red")

    fig = plot_fcc_conv()
    fig.add_traces([*fcc_110_box, *fcc_110_vectors])
    return fig


def plot_fcc_111():
    fcc_111_cell = np.array([[0.5, 0, -0.5], [0, 0.5, -0.5], [1, 1, 1]])

    fcc_111_vectors = vectors(
        fcc_111_cell, name="reduced lattice vectors", color="red", width=6
    )
    fcc_111_box = get_box(fcc_111_cell, name="reduced lattice", color="red")

    fig = plot_fcc_conv()
    fig.add_traces([*fcc_111_box, *fcc_111_vectors])
    return fig