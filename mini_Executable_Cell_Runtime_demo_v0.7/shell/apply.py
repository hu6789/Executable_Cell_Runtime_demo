from internalnet.hir.schema import HIROutput
from shell.world import World
from internalnet.runtime.state import NodeState

def apply_hir_output(
    world: World,
    cell_id: str,
    output: HIROutput,
) -> None:
    """
    Apply one cell's HIROutput to World.

    id is used only to locate the target cell and is never modified.

    Applied outputs:
    - BehaviorRuntimeState -> node/gene states
    - labels -> current-tick labels
    - external SHH effects -> SHH field

    Type update is intentionally deferred.
    """

    cell = world.get_cell(cell_id)

    # ---------------------------------------------------------
    # 0. Final InternalNet Runtime -> World state
    #
    # Runtime contains the final states after:
    # Node -> Passive -> Gene.
    # ---------------------------------------------------------
    if output.runtime is not None:
        for node_name, node_state in output.runtime.node_states.items():
            cell.nodes[node_name] = node_state

        for gene_name, gene_state in output.runtime.gene_states.items():
            cell.genes[gene_name] = gene_state

    # ---------------------------------------------------------
    # 1. BehaviorRuntimeState -> World state
    # ---------------------------------------------------------
    for runtime_state in output.behaviors.values():
        internal_output = runtime_state.internal_outputs

        if not internal_output:
            continue

        # -----------------------------------------------------
        # Normalize single-output and multi-output forms.
        #
        # Single output:
        # {
        #     "target": "SHH",
        #     "state": "total",
        # }
        #
        # Multiple outputs:
        # [
        #     {
        #         "target": "GLI3",
        #         "state": "free",
        #         "mode": "consume",
        #     },
        #     {
        #         "target": "GLI3",
        #         "state": "repressor",
        #         "mode": "produce",
        #     },
        # ]
        # -----------------------------------------------------
        if isinstance(internal_output, list):
            internal_outputs = internal_output
        else:
            internal_outputs = [internal_output]

        for item in internal_outputs:
            target = item.get("target")
            state = item.get("state")
            mode = item.get("mode")

            if target not in cell.nodes:
                raise KeyError(
                    "Node target not found in cell: {}".format(target)
                )

            current_node = cell.nodes[target]

            # -------------------------------------------------
            # Legacy/default behavior:
            # overwrite the target state with runtime value.
            # -------------------------------------------------
            if mode is None:
                if state == "total":
                    cell.nodes[target] = NodeState(
                        name=current_node.name,
                        total=runtime_state.value,
                        states=dict(current_node.states),
                    )

                elif state == "free":
                    states = dict(current_node.states)
                    states["free"] = runtime_state.value

                    cell.nodes[target] = NodeState(
                        name=current_node.name,
                        total=current_node.total,
                        states=states,
                    )

            # -------------------------------------------------
            # Explicit consume / produce behavior.
            # -------------------------------------------------
            elif mode == "consume":
                states = dict(current_node.states)

                current_value = states.get(state, 0.0)
                states[state] = max(
                    current_value - runtime_state.value,
                    0.0,
                )

                cell.nodes[target] = NodeState(
                    name=current_node.name,
                    total=current_node.total,
                    states=states,
                )

            elif mode == "produce":
                states = dict(current_node.states)

                current_value = states.get(state, 0.0)
                states[state] = (
                    current_value + runtime_state.value
                )

                cell.nodes[target] = NodeState(
                    name=current_node.name,
                    total=current_node.total,
                    states=states,
                )

            else:
                raise ValueError(
                    "Unsupported internal output mode: {}".format(
                        mode
                    )
                )
            
    # ---------------------------------------------------------
    # 2. Labels -> current-tick labels
    #
    # Labels are tick-based:
    # overwrite instead of accumulating.
    # ---------------------------------------------------------
    cell.labels = set(output.labels)

    # ---------------------------------------------------------
    # 3. External effects -> World
    #
    # HIR describes the external effect.
    # Shell applies it to World.
    # ---------------------------------------------------------
    for effect in output.external_effects.values():
        if effect.effect_type != "extracellular":
            continue

        if effect.target != "SHH":
            continue

        source = world.state.shh_field.sources.get(cell_id)

        if source is None:
            raise KeyError(
                "SHH source position not found for cell: {}".format(
                    cell_id
                )
            )

        position, _ = source

        world.state.shh_field.set_source(
            cell_id=cell_id,
            position=position,
            amount=effect.value,
        )
        
        print(
            "  [WORLD UPDATE] Cell {}: SHH source <- {:.4f}".format(
                cell_id,
                effect.value,
            )
        )

    # ---------------------------------------------------------
    # 4. Type update
    #
    # HIR provides the current primary type.
    # Shell persists it to World.
    # ---------------------------------------------------------
    if output.type_name is not None:
        cell.type = output.type_name
