# cellmaster/internalnet/behavior_engine/behavior_skeleton.py

"""
Behavior Skeleton Layer

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

    - compute raw behavior drive
    - apply abstract behavior formula
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
    aggregated_contributions
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
        aggregated_contributions.get(
            "activation",
            0.0
        )
    )

    suppression = (
        aggregated_contributions.get(
            "suppression",
            0.0
        )
    )

    amplification = (
        aggregated_contributions.get(
            "amplification",
            1.0
        )
    )

    resource = (
        aggregated_contributions.get(
            "resource",
            1.0
        )
    )

    damage = (
        aggregated_contributions.get(
            "damage",
            0.0
        )
    )

    stabilization = (
        aggregated_contributions.get(
            "stabilization",
            1.0
        )
    )

    destabilization = (
        aggregated_contributions.get(
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

        "aggregated_contributions":
            aggregated_contributions,

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

        drive = (
            (
                activation -
                suppression
            )

            * amplification
            * resource
        )

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
