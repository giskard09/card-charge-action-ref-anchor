#!/usr/bin/env python3
"""Derive action_ref (action-ref-v1) for a card-network charge, per
draft-card-charge-00 (tempoxyz/mpp-specs, author J. Brans/Visa),
Section "Receipt Generation" example receipt (verbatim field values).

STAGED, NOT PUBLISHED: this vector set fulfills a conditional offer made
in tempoxyz/mpp-specs#292 (comment 4916496571, 2026-07-08) -- "if
maintainers pick direction 2 [reference = content-addressed digest of a
frozen field set, distinct from method-specific settlement], happy to
contribute a card-class vector set." That condition has not been
confirmed by a maintainer as of 2026-08-25 -- schwentker narrowed the
open question to a yes/no on 2026-08-25 (comment 5404120501), not yet
answered. Prepared now so the same-day turnaround matches every other
worked example in this series; NOT to be opened as a public repo or
linked in the thread before a maintainer actually picks direction 2.
"""
import json
import os
import hashlib
from jcs import jcs_bytes

HERE = os.path.dirname(os.path.abspath(__file__))

# Verbatim from draft-card-charge-00.md, Section "Receipt Generation"
# (tempoxyz/mpp-specs, specs/methods/card/draft-card-charge-00.md, lines 665-674):
CARD_RECEIPT_EXAMPLE = {
    "challengeId": "ch_9xK2mR4vB7nQ",
    "method": "card",
    "status": "success",
    "reference": "visa_txn_abc123",
    "timestamp": "2026-02-19T12:05:30Z",
    "externalId": "order_12345",
}

# action-ref-v1 preimage: four canonical fields only (agent_id, action_type,
# scope, timestamp). Two-layer pattern (same as the Cashu/melt-quote worked
# example): action_ref does not sit on the receipt object itself -- it sits
# on the *agent's* action of completing the charge, with `scope` citing the
# method's own settlement-relevant identifiers (challengeId + reference) as
# the pointer, verbatim, not reinvented.
PREIMAGE = {
    "agent_id": "did:example:agent-checkout-001",
    "action_type": "mpp.card.charge",
    "scope": {
        "challengeId": CARD_RECEIPT_EXAMPLE["challengeId"],
        "reference": CARD_RECEIPT_EXAMPLE["reference"],
        "externalId": CARD_RECEIPT_EXAMPLE["externalId"],
    },
    "timestamp": CARD_RECEIPT_EXAMPLE["timestamp"],
}


def compute_action_ref_v1(preimage: dict) -> str:
    return hashlib.sha256(jcs_bytes(preimage)).hexdigest()


def main(out_dir: str) -> None:
    action_ref = compute_action_ref_v1(PREIMAGE)
    manifest = {
        "spec": "action-ref-v1 (draft-etcheverry-action-ref)",
        "source_spec": "draft-card-charge-00 (tempoxyz/mpp-specs), Receipt Generation example",
        "card_receipt_example_verbatim": CARD_RECEIPT_EXAMPLE,
        "preimage": PREIMAGE,
        "action_ref_v1": action_ref,
    }
    os.makedirs(out_dir, exist_ok=True)
    with open(os.path.join(out_dir, "manifest.json"), "w") as f:
        json.dump(manifest, f, indent=2, sort_keys=False)
    print(f"action_ref_v1 = {action_ref}")
    print(f"written to {out_dir}/manifest.json")


if __name__ == "__main__":
    import sys
    main(sys.argv[1] if len(sys.argv) > 1 else "artifacts")
