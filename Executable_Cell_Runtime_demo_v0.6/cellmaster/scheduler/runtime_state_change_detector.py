# cellmaster/scheduler/runtime_state_change_detector.py


# =========================================
# runtime state change detector
# =========================================

def detect_runtime_state_changes(

    old_state,

    new_state
):

    signals = []

    signals.extend(

        detect_atp_changes(

            old_state,

            new_state
        )
    )

    signals.extend(

        detect_ros_changes(

            old_state,

            new_state
        )
    )

    signals.extend(

        detect_membrane_changes(

            old_state,

            new_state
        )
    )

    return signals


# =========================================
# ATP
# =========================================

def detect_atp_changes(

    old_state,

    new_state
):

    signals = []

    atp = new_state.get(

        "ATP",

        0.0
    )

    if atp < 10.0:

        signals.append({

            "input_type":
                "internal_state_change",

            "internal_signal":
                "ATP_low",

            "strength":
                10.0
        })

    return signals


# =========================================
# ROS
# =========================================

def detect_ros_changes(

    old_state,

    new_state
):

    signals = []

    ros = new_state.get(

        "ROS",

        0.0
    )

    if ros > 50.0:

        signals.append({

            "input_type":
                "internal_state_change",

            "internal_signal":
                "ROS_high",

            "strength":
                8.0
        })

    return signals


# =========================================
# membrane
# =========================================

def detect_membrane_changes(

    old_state,

    new_state
):

    signals = []

    membrane = new_state.get(

        "cell_membrane",

        100.0
    )

    if membrane < 30.0:

        signals.append({

            "input_type":
                "internal_state_change",

            "internal_signal":
                "membrane_damage",

            "strength":
                10.0
        })

    return signals
