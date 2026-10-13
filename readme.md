# Lab 6 — Chord freeloader

A tiny **in-process** Chord ring (no network). Honest nodes walk the successor chain to find who owns a key, then store/load there. One node is a **freeloader**: lookup stays honest, but it must dump every value onto someone else and still answer `get`.

## Setup

```bash
python3 test_chord.py
```

## TODO

Fill in the TODOs in `freeloader.py`.
+ constructor
+ `put_local`
    - On put: do **not** write the user value into `self.store`. Store it under a unique dump key that **you do not own** (any other node is fine, not only your successor), using the honest path (`HonestNode.put`).
+ `get_local`
    - On get: Pass when later `get` still returns the value, the freeloader's `store` does not keep it, and at least one other node does.

## How the ring works

`find_successor(id)` starts at some node and walks `successor` clockwise until `id` is in `(n, n.successor]`. That successor is the owner. There is no central array.

`test_chord.py` runs two tests (`test_key1` / `test_key2`); both keys are owned by the freeloader.

# Submission

The single file `freeloader.py`.
