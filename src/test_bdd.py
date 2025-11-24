from bdd_encoding import build_bdd_structures
from bdd_reachability import compute_reachable_bdd, count_reachable_states, is_reachable_marking

# Petri net rất nhỏ:
# p0 --t0--> p1 --t1--> p2
places = ["p0", "p1", "p2"]

transitions = [
    {"name": "t0", "inputs": ["p0"], "outputs": ["p1"]},
    {"name": "t1", "inputs": ["p1"], "outputs": ["p2"]},
]

# initial: chỉ có token ở p0
initial_marking_list = ["p0"]

# === GỌI PHẦN 3A ĐỂ XÂY BDD STRUCTURES ===
bdd, var_current, var_next, B_init, T = build_bdd_structures(
    places, transitions, initial_marking_list
)

# === GỌI PHẦN 3B ĐỂ TÍNH REACHABLE SET ===
R = compute_reachable_bdd(bdd, var_current, var_next, B_init, T, places)

num = count_reachable_states(bdd, R, len(places))
print("Số reachable markings (kỳ vọng = 3):", num)

# test vài marking
M0 = {"p0": 1, "p1": 0, "p2": 0}
M1 = {"p0": 0, "p1": 1, "p2": 0}
M2 = {"p0": 0, "p1": 0, "p2": 1}
M3 = {"p0": 1, "p1": 1, "p2": 0}   # impossible

for name, M in [("M0", M0), ("M1", M1), ("M2", M2), ("M3", M3)]:
    print(
        name, M,
        "reachable?" ,
        is_reachable_marking(bdd, R, var_current, M)
    )
