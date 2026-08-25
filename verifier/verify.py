#!/usr/bin/env python3
"""Independent recompute of the card-charge action_ref manifest. Stdlib-only."""
import json
import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "scripts"))
from produce import compute_action_ref_v1

HERE = os.path.dirname(os.path.abspath(__file__))
MANIFEST = os.path.join(os.path.dirname(HERE), "artifacts", "manifest.json")


def main() -> int:
    m = json.loads(open(MANIFEST).read())
    got = compute_action_ref_v1(m["preimage"])
    ok = got == m["action_ref_v1"]
    print(f"recomputed = {got}")
    print(f"manifest   = {m['action_ref_v1']}")
    print("MATCH" if ok else "MISMATCH")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
