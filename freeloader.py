"""Freeloader node — fill in put_local / get_local.

You are still the Chord owner of some keys (lookup is honest).
When a put would store on you, dump the value under a *different* unique
key that you do NOT own, using the honest put path. Keep a map so get
can fetch it back.

After a successful cheat, self.store must not contain user values.
"""

from chord import HonestNode


class FreeloaderNode(HonestNode):
    def __init__(self, node_id):
        HonestNode.__init__(self, node_id)
        # TODO: You can add necessary data structure here

    def put_local(self, key, value):
        # TODO: As a freeloader, you don't want to put the value in your own store (`self.store`)
        # Instead, you try to let other nodes store the value.
        raise NotImplementedError("put_local")

    def get_local(self, key):
        # TODO: You should still returns the correct result to the get request.
        raise NotImplementedError("get_local")