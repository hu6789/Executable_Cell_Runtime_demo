# cellmaster/internalnet/hir/state_label.py


# =========================================
# State Label Evaluation
# =========================================

def evaluate_state_labels(
    adjusted_context,
    fate_progression,
    runtime_entity
):

    """
    evaluate runtime state labels

    responsibilities:
        - evaluate stable/activated states
        - evaluate stress states
        - evaluate infection states
        - evaluate death progression states
        - generate public exposure labels

    DOES NOT:
        - directly modify runtime state
        - directly write world
        - directly execute fate
    """

    interpretation_labels = adjusted_context.get(
        "interpretation_labels",
        []
    )

    runtime_state = adjusted_context.get(
        "runtime_state",
        {}
    )

    progression_context = fate_progression.get(
        "progression_context",
        {}
    )

    completion_context = fate_progression.get(
        "completion_context",
        {}
    )

    state_labels = []

    # =====================================
    # baseline state
    # =====================================

    state_labels.extend(

        evaluate_baseline_labels(
            runtime_state
        )
    )

    # =====================================
    # stress labels
    # =====================================

    state_labels.extend(

        evaluate_stress_labels(
            interpretation_labels
        )
    )

    # =====================================
    # infection labels
    # =====================================

    state_labels.extend(

        evaluate_infection_labels(
            runtime_state,
            interpretation_labels
        )
    )

    # =====================================
    # fate labels
    # =====================================

    state_labels.extend(

        evaluate_fate_labels(
            progression_context,
            completion_context
        )
    )

    # =====================================
    # deduplicate
    # =====================================

    state_labels = list(
        set(state_labels)
    )

    return {

        "state_labels":
            state_labels,

        "public_labels":
            filter_public_labels(
                state_labels,
                runtime_entity
            )
    }


# =========================================
# Baseline Labels
# =========================================

def evaluate_baseline_labels(
    runtime_state
):

    labels = []

    activation = runtime_state.get(
        "activation_level",
        0.0
    )

    if activation > 0.5:

        labels.append(
            "activated"
        )

    else:

        labels.append(
            "stable"
        )

    return labels


# =========================================
# Stress Labels
# =========================================

def evaluate_stress_labels(
    interpretation_labels
):

    labels = []

    if "metabolic_stress" in interpretation_labels:

        labels.append(
            "metabolic_stress"
        )

    if "oxidative_stress" in interpretation_labels:

        labels.append(
            "oxidative_stress"
        )

    if "integrity_collapse" in interpretation_labels:

        labels.append(
            "critical_damage"
        )

    return labels


# =========================================
# Infection Labels
# =========================================

def evaluate_infection_labels(
    runtime_state,
    interpretation_labels
):

    labels = []

    infection_burden = runtime_state.get(
        "infection_burden",
        0.0
    )

    if infection_burden > 0.2:

        labels.append(
            "infected"
        )

    if infection_burden > 0.7:

        labels.append(
            "highly_infected"
        )

    return labels


# =========================================
# Fate Labels
# =========================================

def evaluate_fate_labels(
    progression_context,
    completion_context
):

    labels = []

    fate = progression_context.get(
        "fate",
        "stable"
    )

    progressing = progression_context.get(
        "progressing",
        False
    )

    completed = completion_context.get(
        "completed",
        False
    )

    # =====================================
    # apoptosis
    # =====================================

    if fate == "apoptosis":

        if progressing:

            labels.append(
                "death_initiated"
            )

        if completed:

            labels.append(
                "death_confirmed"
            )

    # =====================================
    # necrosis
    # =====================================

    if fate == "necrosis":

        if progressing:

            labels.append(
                "necrotic_progression"
            )

        if completed:

            labels.append(
                "necrotic_collapse"
            )

    return labels


# =========================================
# Public Label Filter
# =========================================

def filter_public_labels(
    state_labels,
    runtime_entity
):

    exposure_profile = getattr(
        runtime_entity,
        "exposure_profile",
        {}
    )

    public_rules = exposure_profile.get(
        "public_labels",
        []
    )

    # no restriction
    if not public_rules:

        return state_labels

    public_labels = []

    for label in state_labels:

        if label in public_rules:

            public_labels.append(
                label
            )

    return public_labels
