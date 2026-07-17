# inputbuilder/asi_plugin.py


# =========================================
# Adaptive Specificity Interpreter (ASI)
# =========================================

class AdaptiveSpecificityInterpreter:

    """
    antigen specificity / recognition plugin

    responsibilities:
        - antigen matching
        - specificity amplification
        - recognition probability
        - receptor compatibility bias

    does NOT:
        - create intents
        - directly modify world
        - override HIR
    """

    def __init__(self):

        # ---------------------------------
        # receptor specificity database
        # ---------------------------------

        self.receptor_profiles = {

            "TCR": {

                "preferred_antigens": [
                    "viral_peptide",
                    "tumor_peptide"
                ],

                "base_match_prob": 0.7
            },

            "BCR": {

                "preferred_antigens": [
                    "surface_antigen",
                    "viral_capsid"
                ],

                "base_match_prob": 0.6
            }
        }

    # =====================================
    # apply ASI
    # =====================================

    def apply(
        self,
        node_inputs
    ):

        """
        apply specificity interpretation
        to standardized node inputs
        """

        enhanced = []

        for node_input in node_inputs:

            enhanced_input = self.process_single_input(
                node_input
            )

            enhanced.append(
                enhanced_input
            )

        return enhanced

    # =====================================
    # process single input
    # =====================================

    def process_single_input(
        self,
        node_input
    ):

        payload = node_input.get(
            "payload",
            {}
        )

        receptor = payload.get(
            "receptor"
        )

        antigen = payload.get(
            "antigen"
        )

        # ---------------------------------
        # no specificity context
        # ---------------------------------

        if receptor is None or antigen is None:

            payload["match_probability"] = 0.0

            payload["recognition_bias"] = 1.0

            node_input["payload"] = payload

            return node_input

        # ---------------------------------
        # receptor profile
        # ---------------------------------

        profile = self.receptor_profiles.get(
            receptor,
            {}
        )

        preferred = profile.get(
            "preferred_antigens",
            []
        )

        base_prob = profile.get(
            "base_match_prob",
            0.1
        )

        # ---------------------------------
        # matching logic
        # ---------------------------------

        if antigen in preferred:

            match_prob = base_prob

            recognition_bias = 1.5

        else:

            match_prob = 0.05

            recognition_bias = 0.5

        # ---------------------------------
        # inject semantic interpretation
        # ---------------------------------

        payload["match_probability"] = (
            match_prob
        )

        payload["recognition_bias"] = (
            recognition_bias
        )

        payload["recognized"] = (
            match_prob >= 0.5
        )

        node_input["payload"] = payload

        return node_input
