# Provenance

**Status: STAGED, NOT PUBLISHED.** This repo is prepared, not published or
linked anywhere, and must not be opened publicly or referenced in
tempoxyz/mpp-specs#292 until a maintainer explicitly picks "direction 2"
(reference = content-addressed digest of a frozen field set, distinct from
method-specific settlement) — the condition stated in our own comment
4916496571 (2026-07-08). As of 2026-08-25, schwentker narrowed the open
question to a plain yes/no for maintainers (comment 5404120501); no
maintainer has answered yet.

## Exact source of every fixture value

`card_receipt_example_verbatim` in `artifacts/manifest.json` is copied
character-for-character from `tempoxyz/mpp-specs`,
`specs/methods/card/draft-card-charge-00.md`, section "Receipt Generation"
(lines 665–674 as of commit checked 2026-08-25). Author of record: Jacob
Brans (Visa), per the draft's front matter. Nothing in that object was
invented — `challengeId`, `method`, `status`, `reference`, `timestamp`,
`externalId` are the spec's own illustrative values.

`preimage.agent_id` (`did:example:agent-checkout-001`) is **synthetic** —
the spec's example receipt has no agent identifier field (card-charge is a
server/PSP-side receipt, not an agent-declared record), so there is no real
value to cite. Marked explicitly as `did:example:` per RFC 7942/common DID
convention for non-resolvable placeholder identifiers — never to be
represented as a real agent.

`preimage.action_type` (`mpp.card.charge`) is our own naming convention
(namespace `mpp.` + method + intent), not a value defined anywhere in
`draft-card-charge-00` or `draft-payment-intent-charge`. Chosen for
readability; any conformant value works since `action_type` is
free-text-with-convention by design in `action-ref-v1`.

`preimage.scope` composes three of the receipt's own fields
(`challengeId`, `reference`, `externalId`) verbatim as the pointer into the
card method's own settlement record — same two-layer pattern as
`cashu-melt-quote-action-ref-anchor` (quote id cited by reference, not
reinvented).

`preimage.timestamp` is the receipt's own `timestamp` field, copied
verbatim (already RFC 3339).

## What this is not

- Not an integration with schwentker, artiji.xyz, or any real running card
  rail — no real production fixture exists publicly for artiji.xyz (checked
  2026-08-25: no repo under the `schwentker` GitHub account matches
  artiji/card/charge/mpp).
- Not anchored on-chain. Anchoring is deliberately held until the
  conditional trigger is confirmed, to avoid an on-chain record for a
  vector set that may never be requested.
- Not a claim that Visa, tempoxyz, or any mpp-specs maintainer endorsed,
  reviewed, or participated in this derivation.

## Reproduce

```bash
python3 scripts/produce.py artifacts   # derives action_ref_v1
python3 verifier/verify.py             # independent recompute, confirms MATCH
```

`jcs.py` is vendored verbatim from `argentum-core` (no reimplementation).
