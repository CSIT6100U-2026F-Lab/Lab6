#!/usr/bin/env python3
"""Two tests, one key each. Run: python3 test_chord.py

Each key is owned by the freeloader. After put:
  - later get still returns the value
  - the freeloader did not store it, and some other node did
"""

import unittest

from chord import HonestNode, Network
from freeloader import FreeloaderNode


def first_key_owned_by(node, start=0):
    i = start
    while i < 20000:
        key = "k{0}".format(i)
        if node.owns(key):
            return key, i + 1
        i += 1
    raise RuntimeError("no key hashes onto node {0}".format(node.id))


def nodes_with_value(net, value):
    return [n for n in net.nodes if value in n.store.values()]


def make_ring():
    net = Network()
    a = net.add(HonestNode(8))
    f = net.add(FreeloaderNode(20))
    b = net.add(HonestNode(36))
    return net, a, b, f


def owned_keys():
    net, a, b, f = make_ring()
    key1, nxt = first_key_owned_by(f, 0)
    key2, _ = first_key_owned_by(f, nxt)
    return key1, key2


def check_put_get_dump(key, value):
    net, a, b, f = make_ring()
    assert f.owns(key)

    a.put(key, value)

    assert b.get(key) == value
    assert f.get(key) == value

    assert key not in f.store
    assert value not in f.store.values()
    others = [n for n in nodes_with_value(net, value) if n is not f]
    assert len(others) >= 1


class TestFreeloader(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.key1, cls.key2 = owned_keys()

    def test_key1(self):
        check_put_get_dump(self.key1, "alpha")

    def test_key2(self):
        check_put_get_dump(self.key2, "beta")


if __name__ == "__main__":
    unittest.main(verbosity=2)
