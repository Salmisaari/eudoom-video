"""Ink separation LUT: sRGB colour -> coverage of the four inks (black, blue, yellow, orange).

Print model: result = paper * prod_k (1 - a_k * (1 - T_k)), T_k = ink_k / paper (per channel, linear light).
Each LUT cell holds the coverages that reproduce the cell's colour best, preferring less ink
(black is cheap so neutrals go to black, colours are dearer). Output: app/public/data/inklut.bin,
N^3 cells (r fastest), 4 uint8 per cell, plus inklut.json with the inks and N.
"""
import json, sys
import numpy as np

INKS = {  # sRGB hex of each ink printed solid on the paper
    "black": "#1d1b20",
    "blue": "#2b3f9e",
    "yellow": "#ffd21f",
    "orange": "#f2602b",
}
PAPER = "#f3eee3"
COST = np.array([0.004, 0.012, 0.012, 0.012])  # per unit coverage (in loss units)
N = 33

def lin(h):
    v = np.array([int(h[i:i + 2], 16) for i in (1, 3, 5)]) / 255.0
    return np.where(v <= 0.04045, v / 12.92, ((v + 0.055) / 1.055) ** 2.4)

P = lin(PAPER)
T = np.stack([np.minimum(lin(h) / P, 1.0) for h in INKS.values()])  # 4 x 3

def render(a):  # a: (..., 4) -> (..., 3) linear
    f = 1.0 - a[..., :, None] * (1.0 - T[None, :, :])  # (...,4,3)
    return P * np.prod(f, axis=-2)

def to_srgb(x):
    x = np.clip(x, 0, 1)
    return np.where(x <= 0.0031308, x * 12.92, 1.055 * x ** (1 / 2.4) - 0.055)

g = np.linspace(0, 1, N)
tgt = np.stack(np.meshgrid(g, g, g, indexing="ij"), -1)[..., ::-1].reshape(-1, 3)  # r fastest
tgt = tgt[:, ::-1] if False else tgt
# rebuild explicitly so index = r + g*N + b*N*N
b_, g_, r_ = np.meshgrid(g, g, g, indexing="ij")
tgt = np.stack([r_.ravel(), g_.ravel(), b_.ravel()], -1)  # sRGB targets

# coarse grid search
q = np.linspace(0, 1, 9)
grid = np.stack(np.meshgrid(q, q, q, q, indexing="ij"), -1).reshape(-1, 4)
gs = to_srgb(render(grid))  # compare in sRGB (closer to perceptual)
best = np.empty((tgt.shape[0], 4))
for i in range(0, tgt.shape[0], 1500):
    t = tgt[i:i + 1500]
    d = ((t[:, None, :] - gs[None, :, :]) ** 2).sum(-1) + (grid @ COST)[None, :]
    best[i:i + 1500] = grid[d.argmin(1)]

# refine: projected gradient descent (numerical gradient) on all cells at once
a = best.copy()
def loss(a):
    return ((to_srgb(render(a)) - tgt) ** 2).sum(-1) + a @ COST
lr = 0.2
for it in range(400):
    L0 = loss(a)
    grad = np.zeros_like(a)
    for k in range(4):
        e = np.zeros(4); e[k] = 1e-3
        grad[:, k] = (loss(np.clip(a + e, 0, 1)) - L0) / 1e-3
    na = np.clip(a - lr * grad, 0, 1)
    better = loss(na) < L0
    a[better] = na[better]
    if it % 100 == 99:
        lr *= 0.5
err = np.sqrt(((to_srgb(render(a)) - tgt) ** 2).sum(-1))
print("max err (sRGB 0..1):", err.max().round(3), "median:", np.median(err).round(4))
for name, h in [("paper", PAPER)] + list(INKS.items()):
    v = np.array([int(h[i:i + 2], 16) for i in (1, 3, 5)]) / 255.0
    idx = np.round(v * (N - 1)).astype(int)
    print(name, a[idx[0] + idx[1] * N + idx[2] * N * N].round(2))
out = sys.argv[1] if len(sys.argv) > 1 else "../app/public/data/inklut.bin"
(np.round(a * 255).astype(np.uint8)).tofile(out)
json.dump({"N": N, "paper": PAPER, "inks": INKS, "order": list(INKS)}, open(out.replace(".bin", ".json"), "w"), indent=1)
print("wrote", out)
