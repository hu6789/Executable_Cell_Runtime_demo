# cellinstance/factory/stochastic_initializer.py

import random


# =========================================
# Stochastic Initializer
# =========================================

class StochasticInitializer:

    """
    stochastic runtime initializer

    responsibilities:
        - sample biological initial states
        - construct runtime node values
        - apply stochastic variability
        - normalize runtime initialization

    DOES NOT:
        - execute runtime logic
        - modify world state
        - evaluate physiology
    """

    def __init__(self):

        pass

    # =====================================
    # initialize runtime state
    # =====================================

    def initialize_runtime_state(
        self,
        init_schema
    ):

        runtime_state = {}

        for node_name, node_schema in (

            init_schema.items()
        ):

            runtime_state[
                node_name
            ] = self.sample_node_value(
                node_schema
            )

        return runtime_state

    # =====================================
    # sample node value
    # =====================================

    def sample_node_value(
        self,
        node_schema
    ):
        # -----------------------------
        # fixed scalar
        # -----------------------------

        if isinstance(
            node_schema,
            (int, float)
        ):
            return float(
                node_schema
            )
            
        distribution = node_schema.get(
            "distribution",
            "fixed"
        )

        # =================================
        # fixed value
        # =================================

        if distribution == "fixed":

            return node_schema.get(
                "value",
                0.0
            )

        # =================================
        # normal distribution
        # =================================

        if distribution == "normal":

            mean = node_schema.get(
                "mean",
                0.0
            )

            std = node_schema.get(
                "std",
                1.0
            )

            return random.gauss(
                mean,
                std
            )

        # =================================
        # uniform distribution
        # =================================

        if distribution == "uniform":

            low = node_schema.get(
                "min",
                0.0
            )

            high = node_schema.get(
                "max",
                1.0
            )

            return random.uniform(
                low,
                high
            )

        # =================================
        # fallback
        # =================================

        return 0.0
