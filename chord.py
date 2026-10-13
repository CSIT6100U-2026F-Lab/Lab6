"""In-process Chord ring. No sockets.

Each node only knows its successor. find_successor walks clockwise
until it finds the owner of a key id: the first node clockwise with
node.id >= key_id (wrapping around 0).
"""

import hashlib

MOD = 64


def key_id(key):
    """Map a key onto the ring [0, MOD)."""
    digest = hashlib.sha1(str(key).encode("utf-8")).hexdigest()
    return int(digest, 16) % MOD


def in_range(value, start, end, include_end=True):
    """True if value is in (start, end] on the ring."""
    value %= MOD
    start %= MOD
    end %= MOD
    if start == end:
        return True
    if start < end:
        return start < value <= end if include_end else start < value < end
    if include_end:
        return value > start or value <= end
    return value > start or value < end


class HonestNode(object):
    def __init__(self, node_id):
        self.id = node_id % MOD
        self.successor = self
        self.predecessor = self
        self.store = {}

    def find_successor(self, target_id, path=None):
        """Return the node responsible for target_id. path collects node ids."""
        if path is None:
            path = []
        path.append(self.id)
        if len(path) > MOD + 2:
            raise RuntimeError("find_successor looped")
        target_id %= MOD
        if self.successor is self or target_id == self.id:
            return self
        if in_range(target_id, self.id, self.successor.id, include_end=True):
            return self.successor
        return self.successor.find_successor(target_id, path)

    def put(self, key, value):
        owner = self.find_successor(key_id(key))
        owner.put_local(key, value)
        return owner

    def get(self, key):
        owner = self.find_successor(key_id(key))
        return owner.get_local(key)

    def put_local(self, key, value):
        self.store[key] = value

    def get_local(self, key):
        return self.store.get(key)

    def owns(self, key):
        return self.find_successor(key_id(key)) is self


class Network(object):
    """A set of nodes. Adding a node rewires successor/predecessor by id."""

    def __init__(self):
        self.nodes = []

    def add(self, node):
        if any(n.id == node.id for n in self.nodes):
            raise ValueError("duplicate node id {0}".format(node.id))
        self.nodes.append(node)
        self._relink()
        return node

    def _relink(self):
        ordered = sorted(self.nodes, key=lambda n: n.id)
        for i, node in enumerate(ordered):
            node.successor = ordered[(i + 1) % len(ordered)]
            node.predecessor = ordered[(i - 1) % len(ordered)]

    def who_has(self, key):
        """Nodes whose store actually contains this key."""
        return [n for n in self.nodes if key in n.store]
