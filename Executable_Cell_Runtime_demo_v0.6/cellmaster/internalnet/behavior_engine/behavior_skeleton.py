# cellmaster/internalnet/behavior_engine/behavior_skeleton.py

"""
Behavior Skeleton Layer
combine normalized categories
position:
    contribution processing stage

pipeline:

    contribution
        ->
    transform
        ->
    group
        ->
    aggregate
        ->
    skeleton
        ->
    behavior gate

responsibilities:

    compute behavior drive

Input:

    normalized behavior signals

Output:

    raw behavior drive
    - separate behavior philosophy from graph wiring

design principle:

    graph edge:
        defines signal origin

    skeleton:
        defines behavior computation structure

examples:

    secretion:
        activation × resource

    proliferation:
        activation × resource × stabilization

    migration:
        activation × mobility_resource

DOES NOT:

    - evaluate final behavior gate
    - execute behavior
    - generate intent
"""
# =========================================
# Behavior Skeleton Runtime
# =========================================

def apply_behavior_skeleton(
    behavior_def,
    normalized_contributions
):

    """
    compute raw behavior drive
    using abstract behavior skeleton

    responsibilities:
        - combine aggregated categories
        - apply abstract runtime structure
        - generate raw behavior drive

    DOES NOT:
        - evaluate final behavior gate
        - apply runtime scaling
        - execute behaviors
    """

    skeleton = behavior_def.get(
        "behavior_skeleton",
        {}
    )

    formula = skeleton.get(
        "formula",
        "default"
    )

    # =====================================
    # category values
    # =====================================

    activation = (
        normalized_contributions.get(
            "activation",
            0.0
        )
    )

    suppression = (
        normalized_contributions.get(
            "suppression",
            0.0
        )
    )

    amplification = max(
        0.0,
        normalized_contributions.get(
            "amplification",
            100.0
        )
    )

    resource = max(
        0.0,
        normalized_contributions.get(
            "resource",
            100.0
        )
    )

    stabilization = (
        normalized_contributions.get(
            "stabilization",
            100.0
        )
    )

    damage = (
        normalized_contributions.get(
            "damage",
            0.0
        )
    )

    destabilization = (
        normalized_contributions.get(
            "destabilization",
            0.0
        )
    )

    # =====================================
    # compute skeleton formula
    # =====================================
    """
    Behavior Skeleton Formula

    important:

        behavior json does NOT
        define graph wiring

        graph wiring comes from
        behavior edges

        skeleton only defines
        abstract computation structure

    therefore:

        different cell types
        may reuse same skeleton
        while using different node wiring
    """
    raw_drive = compute_formula(

        formula,

        activation,
        suppression,
        amplification,
        resource,
        damage,
        stabilization,
        destabilization
    )

    return {

        "raw_drive":
            raw_drive,

        "normalized_contributions":
            normalized_contributions,

        "formula":
            formula
    }


# =========================================
# Skeleton Formula Dispatcher
# =========================================

def compute_formula(
    formula,
    activation,
    suppression,
    amplification,
    resource,
    damage,
    stabilization,
    destabilization
):

    # =====================================
    # default skeleton
    # drive =
    # (activation - suppression)
    # × amplification
    # × resource
    # =====================================

    if formula == "default":

        activation /= 100.0
        suppression /= 100.0
        amplification /= 100.0
        resource /= 100.0
        damage /= 100.0
        stabilization /= 100.0
        destabilization /= 100.0

        drive = (
            max(
                activation - suppression,
                0.0
            )
            * amplification
            * resource
        )

        drive *= stabilization
        drive *= (
            1.0 -
            destabilization
        )

        drive -= damage

        drive = max(
            drive,
            0.0
        )

        return drive * 100.0

        drive *= (
            stabilization
        )

        drive *= (
            1.0 -
            destabilization
        )

        drive -= damage

        return max(
            0.0,
            drive
        )

    # =====================================
    # aggressive skeleton
    # =====================================

    if formula == "aggressive":

        drive = (

            activation
            * amplification
            * amplification
        )

        drive *= (
            1.0 -
            suppression
        )

        drive *= resource

        drive -= (
            damage * 0.5
        )

        return max(
            0.0,
            drive
        )

    # =====================================
    # conservative skeleton
    # =====================================

    if formula == "conservative":

        drive = (
            activation -
            suppression -
            damage
        )

        drive *= (
            resource
            * stabilization
        )

        return max(
            0.0,
            drive
        )

    # =====================================
    # fallback
    # =====================================

    return max(
        0.0,
        activation - suppression
    )
