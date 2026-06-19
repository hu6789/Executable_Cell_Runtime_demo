# cellinstance/runtime/runtime_state.py


# =========================================
# Runtime State
# =========================================

class RuntimeState:

    """
    runtime node state container

    responsibilities:
        - hold internal node values
        - apply runtime delta
        - provide snapshot
        - support node read/write

    DOES NOT:
        - calculate physiology
        - execute graph logic
        - write world
    """

    def __init__(

        self,
        initial_state=None
    ):

        self.node_state = dict(

            initial_state or {}
        )

    # =====================================
    # get node
    # =====================================

    def get(

        self,
        node_name,
        default=0.0
    ):

        return self.node_state.get(

            node_name,
            default
        )

    # =====================================
    # set node
    # =====================================

    def set(

        self,
        node_name,
        value
    ):

        self.node_state[node_name] = value

    # =====================================
    # apply delta
    # =====================================

    def apply_delta(

        self,
        delta_dict
    ):

        for node_name, delta in delta_dict.items():

            old_value = self.node_state.get(

                node_name,
                0.0
            )

            self.node_state[node_name] = (

                old_value + delta
            )

    # =====================================
    # export snapshot
    # =====================================

    def snapshot(self):

        return dict(

            self.node_state
        )

    def raw(self):
        return self.node_state


    def snapshot(self):
        return dict(self.node_state)

    def __getitem__(self, k):
        return self.node_state[k]

    def __setitem__(self, k, v):
        self.node_state[k] = v

    def get(self, k, default=None):
        return self.node_state.get(k, default)

    def items(self):
        return self.node_state.items()

    def __iter__(self):
        return iter(self.node_state)

    def __len__(self):
        return len(self.node_state)
