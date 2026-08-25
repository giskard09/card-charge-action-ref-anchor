# card-charge-action-ref-anchor

A worked example that derives an **`action_ref`** — a deterministic,
content-addressed identifier for an agent action
([`action-ref-v1`](https://github.com/giskard09/argentum-core/blob/master/docs/spec/action-ref.md)) —
for a card-network charge, per
[`draft-card-charge-00`](https://github.com/tempoxyz/mpp-specs/blob/main/specs/methods/card/draft-card-charge-00.md)
(tempoxyz/mpp-specs, author J. Brans/Visa).

Not answering the authorization-vs-settlement timing question open in
[tempoxyz/mpp-specs#292](https://github.com/tempoxyz/mpp-specs/issues/292) —
that's a spec decision, not something a reference mechanism should
presuppose. This shows what "reference as content-addressed digest"
(direction 2, from our comment
[4916496571](https://github.com/tempoxyz/mpp-specs/issues/292#issuecomment-4916496571))
looks like concretely for the card method: the mechanism identifies the
action regardless of which timing rule the spec lands on, so the two
questions can be resolved independently.

> **Provenance, up front (read `PROVENANCE.md` for the full statement).**
> The receipt object is copied verbatim from `draft-card-charge-00`'s own
> "Receipt Generation" example. `agent_id` is a synthetic placeholder
> (`did:example:...`) — the spec's example receipt has no agent
> identifier field. No live artiji.xyz integration, no claim of
> endorsement by Visa, tempoxyz, or any mpp-specs maintainer.

## What's here

| Path | What it is |
|------|-----------|
| `scripts/produce.py` | Derives `action_ref_v1` per action-ref-v1 (JCS RFC 8785 + SHA-256) from the card-charge receipt example. |
| `scripts/jcs.py` | `argentum-core`'s own JCS helper, vendored verbatim. |
| `verifier/verify.py` | Independent (stdlib-only) recompute + match check. |
| `artifacts/manifest.json` | The canonical instance: preimage + digest. |
| `PROVENANCE.md` | Exact source of every fixture value. Read it. |

## Reproduce

```bash
python3 scripts/produce.py artifacts
python3 verifier/verify.py
```

Disclosure: we maintain the referenced `action-ref-v1` spec and corpus.
