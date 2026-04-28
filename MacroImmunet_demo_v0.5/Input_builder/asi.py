class ASI:

    def apply(self, node_input, perception):

        # example: boost TCR if strong contact
        if node_input.get("TCR_signal", 0) > 0.5:
            node_input["TCR_signal"] *= 1.2

        return node_input
