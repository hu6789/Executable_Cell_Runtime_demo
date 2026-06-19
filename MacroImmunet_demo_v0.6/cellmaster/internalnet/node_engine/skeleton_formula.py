# cellmaster/internalnet/node_engine/skeleton_formula.py


# =========================================
# Apply Node Skeleton Formula
# =========================================

def apply_node_skeleton_formula(
    node_definition,
    aggregated_contributions
):

    """
    execute abstract node skeleton

    node skeleton defines:
        - how categories combine
        - final runtime structure
        - abstract physiological logic

    graph edges define:
        - contribution sources

    supported skeletons:
        - drive_balance
        - activation_only
        - suppression_balance
        - resource_limited
        - damage_integrated
        - custom_formula
    """

    skeleton = node_definition.get(
        "skeleton_formula",
        "drive_balance"
    )

    # =====================================
    # built-in skeletons
    # =====================================

    if skeleton == "drive_balance":

        raw_value = evaluate_drive_balance(
            aggregated_contributions
        )

    elif skeleton == "activation_only":

        raw_value = evaluate_activation_only(
            aggregated_contributions
        )

    elif skeleton == "suppression_balance":

        raw_value = evaluate_suppression_balance(
            aggregated_contributions
        )

    elif skeleton == "resource_limited":

        raw_value = evaluate_resource_limited(
            aggregated_contributions
        )

    elif skeleton == "damage_integrated":

        raw_value = evaluate_damage_integrated(
            aggregated_contributions
        )

    # =====================================
    # custom formula
    # =====================================

    elif skeleton == "custom_formula":

        raw_value = evaluate_custom_formula(

            node_definition,
            aggregated_contributions
        )

    # =====================================
    # fallback
    # =====================================

    else:

        raw_value = 0.0

    # =====================================
    # unified runtime package
    # =====================================

    return {

        "skeleton_formula":
            skeleton,

        "raw_value":
            raw_value,

        "active":
            True,
        
        "metadata":
            {}
    }
# =========================================
# Drive Balance
# =========================================

def evaluate_drive_balance(
    aggregated
):

    activation = get_category_value(
        aggregated,
        "activation"
    )

    suppression = get_category_value(
        aggregated,
        "suppression"
    )

    amplification = get_category_value(
        aggregated,
        "amplification",
        default=1.0
    )

    resource = get_category_value(
        aggregated,
        "resource",
        default=1.0
    )

    destabilization = get_category_value(
        aggregated,
        "destabilization"
    )

    stabilization = get_category_value(
        aggregated,
        "stabilization"
    )

    drive = (
        activation
        - suppression
    )

    drive *= amplification

    drive *= resource

    drive += stabilization

    drive -= destabilization

    return drive
# =========================================
# Activation Only
# =========================================

def evaluate_activation_only(
    aggregated
):

    return get_category_value(
        aggregated,
        "activation"
    )


# =========================================
# Suppression Balance
# =========================================

def evaluate_suppression_balance(
    aggregated
):

    activation = get_category_value(
        aggregated,
        "activation"
    )

    suppression = get_category_value(
        aggregated,
        "suppression"
    )

    return (
        activation - suppression
    )


# =========================================
# Resource Limited
# =========================================

def evaluate_resource_limited(
    aggregated
):

    activation = get_category_value(
        aggregated,
        "activation"
    )

    resource = get_category_value(
        aggregated,
        "resource",
        default=1.0
    )

    damage = get_category_value(
        aggregated,
        "damage"
    )

    return (
        activation
        * resource
        - damage
    )


# =========================================
# Damage Integrated
# =========================================

def evaluate_damage_integrated(
    aggregated
):

    activation = get_category_value(
        aggregated,
        "activation"
    )

    damage = get_category_value(
        aggregated,
        "damage"
    )

    destabilization = get_category_value(
        aggregated,
        "destabilization"
    )

    return (
        activation
        - damage
        - destabilization
    )


# =========================================
# Custom Formula
# =========================================

def evaluate_custom_formula(
    node_definition,
    aggregated
):

    """
    placeholder for future
    programmable skeletons
    """

    formula = node_definition.get(
        "custom_formula"
    )

    if formula is None:

        return 0.0

    # future:
    # safe formula parser

    return 0.0


# =========================================
# Get Category Value
# =========================================

def get_category_value(
    aggregated,
    category,
    default=0.0
):

    category_data = aggregated.get(
        category
    )

    if category_data is None:

        return default

    if not category_data.get(
        "active",
        False
    ):

        return default

    return category_data.get(
        "value",
        default
    )
