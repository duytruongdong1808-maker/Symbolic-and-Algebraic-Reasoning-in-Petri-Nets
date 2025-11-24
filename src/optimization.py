from bdd_encoding import build_bdd_structures
from bdd_reachability import compute_reachable_bdd
from collections import deque
import random

places = ["p0", "p1"]
transitions = [
    {"name": "t0", "inputs": ["p0"], "outputs": ["p0", "p0"]},  # produces 2 tokens, consumes 1 → p0 grows
]
initial_marking_list = ["p0"]

OMEGA = float("inf")   # use inf to represent ω

def fire_transition(marking, trans, place_index):
    """Return new marking after firing transition (or None if not enabled)."""
    new_m = list(marking)

    # consume tokens
    for p in trans["inputs"]:
        i = place_index[p]
        if new_m[i] == OMEGA:
            continue
        if new_m[i] == 0:
            return None     # not enabled
        new_m[i] -= 1

    # produce tokens
    for p in trans["outputs"]:
        i = place_index[p]
        if new_m[i] != OMEGA:
            new_m[i] += 1

    return tuple(new_m)


def km_leq(m1, m2):
    """m1 <= m2 componentwise (ω compares as bigger)."""
    for a, b in zip(m1, m2):
        if a != OMEGA and b != OMEGA and a > b:
            return False
        if a == OMEGA and b != OMEGA:
            return False
    return True


def km_increase_to_omega(marking, ancestor):
    """Return marking where increased components are set to ω."""
    m = list(marking)
    for i in range(len(marking)):
        if marking[i] > ancestor[i]:   # strictly increased
            m[i] = OMEGA
    return tuple(m)


def karp_miller_tree(places, transitions, initial_marking_list):
    place_index = {p: i for i, p in enumerate(places)}
    n = len(places)

    # Initial marking vector
    M0 = tuple(1 if p in initial_marking_list else 0 for p in places)

    root = M0
    tree = {root: []}
    queue = deque([(root, [root])])  # (node, ancestors_path)

    unbounded = False

    while queue:
        marking, ancestors = queue.popleft()

        for t in transitions:
            child = fire_transition(marking, t, place_index)
            if child is None:
                continue

            # acceleration check: compare with ancestors
            accelerated = False
            for anc in ancestors:
                if km_leq(anc, child) and child != anc:
                    child = km_increase_to_omega(child, anc)
                    accelerated = True
                    break

            if any(x == OMEGA for x in child):
                unbounded = True

            if child not in tree:
                tree[child] = []
                tree[marking].append(child)
                queue.append((child, ancestors + [child]))

    return tree, unbounded

def optimize(places, transitions, initial_markiplaces_weightng_list):
    #check if petri net is bounded
    tree, unbounded = karp_miller_tree(places, transitions, initial_marking_list)

    #assign weights for places
    places_weight = {}
    for p in places:
        rand_int = random.randint(1, 10)
        places_weight[p] = rand_int
        print(f"Place {p} assigned weight {rand_int}")

    #Build reverse index for markings
    place_index = {p: i for i, p in enumerate(places)}

    #Check all nodes
    for marking in tree.keys():
        for p in places:
            idx = place_index[p]
            if marking[idx] == OMEGA and places_weight[p] > 0:
                return "Objective unbounded above"

    best_value = -float("inf")
    best_marking = None

    for marking in tree.keys():
        value = 0
        for p in places:
            idx = place_index[p]
            if marking[idx] != OMEGA:
                value += marking[idx] * places_weight[p]

        marking_str = ", ".join(f"{places[i]}={marking[i]}" for i in range(len(places)))
        print(f"Marking: ({marking_str}) -> Value: {value}")

        if value > best_value:
            best_value = value
            best_marking = marking

    return best_marking, best_value

if __name__ == "__main__":
    result = optimize(places, transitions, initial_marking_list)
    #print result

    if isinstance(result, str):
        # This happens if the objective is unbounded
        print("Result:", result)
    else:
        best_marking, best_value = result

        # Print best marking nicely
        print("\nOptimal marking and value:")
        for i, p in enumerate(places):
            val = best_marking[i]
            if val == OMEGA:
                val_str = "ω"
            else:
                val_str = str(val)
            print(f"{p}: {val_str}")
        print("Optimal value:", best_value)
