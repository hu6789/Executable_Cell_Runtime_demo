class RuntimeState:

    def __init__(self, initial_state=None):
        self.node_state = dict(initial_state or {})

    # -----------------------------
    # basic api
    # -----------------------------

    def get(self, key, default=0.0):
        return self.node_state.get(key, default)

    def set(self, key, value):
        self.node_state[key] = value

    def apply_delta(self, delta_dict):
        for key, delta in delta_dict.items():
            self.node_state[key] = (
                self.node_state.get(key, 0.0)
                + delta
            )

    # -----------------------------
    # export
    # -----------------------------

    def snapshot(self):
        return dict(self.node_state)

    def raw(self):
        return self.node_state

    # -----------------------------
    # dict compatibility
    # -----------------------------

    def __getitem__(self, key):
        return self.node_state[key]

    def __setitem__(self, key, value):
        self.node_state[key] = value

    def __contains__(self, key):
        return key in self.node_state

    def items(self):
        return self.node_state.items()

    def keys(self):
        return self.node_state.keys()

    def values(self):
        return self.node_state.values()

    def __iter__(self):
        return iter(self.node_state)

    def __len__(self):
        return len(self.node_state)
