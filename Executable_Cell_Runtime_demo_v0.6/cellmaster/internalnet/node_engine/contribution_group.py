# cellmaster/internalnet/node_engine/contribution_group.py


# =========================================
# Default Contribution Categories
# =========================================

DEFAULT_CATEGORIES = [

    "activation",
    "suppression",
    "amplification",
    "resource",
    "damage",
    "stabilization",
    "destabilization"
]


# =========================================
# Group Contributions By Category
# =========================================

def group_contributions_by_category(
    contributions
):

    """
    organize transformed contributions
    into predefined semantic categories

    responsibilities:
        - preserve graph semantic grouping
        - isolate category aggregation
        - provide skeleton-ready structure

    DOES NOT:
        - aggregate values
        - apply node formulas
        - apply runtime gates
    """

    grouped = initialize_groups()

    for contribution in contributions:

        category = contribution.get(
            "category",
            "activation"
        )

        # ---------------------------------
        # unknown category
        # ---------------------------------

        if category not in grouped:

            grouped[category] = []

        grouped[category].append(
            contribution
        )

    return grouped


# =========================================
# Initialize Empty Groups
# =========================================

def initialize_groups():

    grouped = {}

    for category in DEFAULT_CATEGORIES:

        grouped[category] = []

    return grouped


# =========================================
# Extract Category Values
# =========================================

def extract_category_values(
    grouped_contributions,
    category
):

    contributions = grouped_contributions.get(
        category,
        []
    )

    return [

        contribution.get(
            "value",
            0.0
        )

        for contribution in contributions
    ]


# =========================================
# Count Category Contributions
# =========================================

def count_category_contributions(
    grouped_contributions,
    category
):

    contributions = grouped_contributions.get(
        category,
        []
    )

    return len(contributions)


# =========================================
# Get Participating Sources
# =========================================

def get_participating_sources(
    grouped_contributions,
    category
):

    contributions = grouped_contributions.get(
        category,
        []
    )

    return [

        contribution.get("source")

        for contribution in contributions
    ]
