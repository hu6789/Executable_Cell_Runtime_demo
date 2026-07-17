# cellmaster/internalnet/internalnet.py

from cellmaster.internalnet.runtime_snapshot import (
    build_runtime_snapshot
)
from cellmaster.internalnet.node_engine.node_engine import (
    NodeEngine
)

from cellmaster.internalnet.passive_engine.passive_engine import (
    PassiveEngine
)

from cellmaster.internalnet.runtime_modulation.modulation_engine import (
    RuntimeModulationEngine
)

from cellmaster.internalnet.hir.hir_engine import (
    HIREngine
)

from cellmaster.internalnet.behavior_engine.behavior_engine import (
    BehaviorEngine
)

from cellmaster.internalnet.passive_engine.passive_loader import (
    PassiveLoader
)

DEBUG = False


def debug_print(*args, **kwargs):
    if DEBUG:
        print(*args, **kwargs)
        
# =========================================
# Internal Runtime Network
# =========================================

class InternalNet:

    """
    Cell Internal Runtime Network

    responsibilities:

        - execute node runtime
        - execute passive runtime
        - execute runtime modulation
        - execute HIR
        - execute behavior evaluation

    DOES NOT:

        - write world
        - generate intents
        - execute requests

    outputs:

        runtime_output
    """

    def __init__(

        self,

        node_engine=None,
        passive_engine=None,

        modulation_engine=None,

        hir_engine=None,
        behavior_engine=None
    ):
        self.node_engine = (
            node_engine
            or NodeEngine()
        )
        
        self.passive_loader = PassiveLoader()
        
        self.passive_engine = (
            passive_engine
            or PassiveEngine()
        )

        self.modulation_engine = (
            modulation_engine
            or RuntimeModulationEngine(
                registry=None
            )
        )

        self.hir_engine = (
            hir_engine
            or HIREngine()
        )

        self.behavior_engine = (
            behavior_engine
            or BehaviorEngine()
        )

    # =====================================
    # runtime execution
    # =====================================

    def run(

        self,

        runtime_entity,

        graph_context,

        node_inputs,

        runtime_context,

        tick=None
    ):

        debug_print(
            f"[InternalNet] tick={tick}"
        )
        
        # =================================
        # node runtime
        # =================================
        
        debug_print()
        debug_print()
        debug_print("GRAPH NODES")
        debug_print(
            graph_context.get_runtime_nodes()
        )

        debug_print()
        debug_print("GRAPH EDGES")
        debug_print(
            graph_context.get_runtime_edges()
        )

        node_runtime_results = (

            self.node_engine.evaluate_nodes(

                node_definitions = graph_context.get_runtime_nodes(),

                runtime_context=
                    runtime_context,

                graph_context=
                    graph_context
            )
        )
        
        debug_print()
        debug_print("NODE RUNTIME RESULTS")
        debug_print(node_runtime_results)

        # =================================
        # build node runtime state
        # =================================

        node_runtime_state = runtime_entity.runtime_state.snapshot()

        for result in node_runtime_results:

            node_id = result.get("node_id")

            if node_id is None:
                continue

            node_runtime_state[node_id] += (
                result.get("runtime_value", 0.0)
            )
            
        # =================================
        # passive runtime
        # =================================

        passive_definitions = (
            self.passive_loader.load_all_passives()
        )

        passive_runtime_results = (
            self.passive_engine.process_all_passives(
                runtime_entity=runtime_entity,
                runtime_context={
                    "runtime_state":
                        node_runtime_state,
                    "tick":
                        tick
                },
                passive_definitions=
                    passive_definitions
            )
        )

        passive_runtime_state = (
            self.passive_engine.apply_passive_state(
                node_runtime_state.copy(),
                passive_runtime_results
            )
        )
        
        debug_print()
        debug_print("=" * 60)
        debug_print("PASSIVE RESULTS")
        debug_print("=" * 60)
        debug_print(passive_runtime_results)

        debug_print()
        debug_print("=" * 60)
        debug_print("PASSIVE STATE")
        debug_print("=" * 60)
        debug_print(passive_runtime_state)

        # =================================
        # modulation runtime
        # =================================

        modulation_output = (

            self.modulation_engine.process(

                runtime_entity=
                    runtime_entity,
                    
                runtime_state=
                    passive_runtime_state,

                node_runtime_results=
                    node_runtime_results,

                passive_runtime_results=
                    passive_runtime_results,

                runtime_graph=
                    graph_context,

                node_inputs=
                    node_inputs,

                tick=tick
            )
        )

        modulation_runtime_state = (
            modulation_output.get(
                "modulation_runtime_state",
                {}
            )
        )

        modulated_runtime_state = (
            passive_runtime_state.copy()
            if isinstance(passive_runtime_state, dict)
            else passive_runtime_state
        )
        
        node_mods = (
            modulation_runtime_state.get(
                "node_modulations",
                {}
            )
        )
        
        for node_id, mod in node_mods.items():

            if mod.get("blocked"):

                modulated_runtime_state[
                    node_id
                ] = 0.0

                continue

            override = mod.get(
                "override"
            )

            if override is not None:

                modulated_runtime_state[
                    node_id
                ] = override

                continue

            value = modulated_runtime_state.get(
                node_id,
                0.0
            )

            value *= mod.get(
                "multiply",
                1.0
            )

            value += mod.get(
                "add",
                0.0
            )

            modulated_runtime_state[
                node_id
            ] = value
            
            
        debug_print()
        debug_print("MODULATION OUTPUT")
        debug_print(modulation_output)

        # =================================
        # HIR
        # =================================
        
        hir_output = (

            self.hir_engine.process(

                runtime_entity=
                    runtime_entity,

                runtime_state=
                    modulated_runtime_state,

                behavior_defs=
                    graph_context.get_runtime_behaviors(),

                modulation_runtime_state=
                    modulation_runtime_state,

                tick=tick
            )
        )

        # =================================
        # behavior runtime
        # =================================

        behavior_output = (

            self.behavior_engine.run_behaviors(

                runtime_entity=
                    runtime_entity,

                node_runtime_state=
                    modulated_runtime_state,

                modulation_runtime_state=
                    modulation_runtime_state,

                graph_context=
                    graph_context,

                hir_output=
                    hir_output,

                tick=tick
            )
        )
        
        trace = behavior_output.get(
            "behavior_trace",
            []
        )

        if trace:

            print()
            print(
                f"[Behavior] "
                f"{runtime_entity.id} "
                f"({runtime_entity.template_id})"
            )

            for item in trace:

                print(
                    f"    "
                    f"{item['behavior']:<28}"
                    f"strength={item['strength']:.6f}"
                )
        
        debug_print()
        debug_print("HIR OUTPUT")
        debug_print(hir_output)

        debug_print()
        debug_print("BEHAVIOR OUTPUT")
        debug_print(behavior_output)
        # =================================
        # runtime output
        # =================================

        runtime_output = {

            "cell_id":
                runtime_entity.id,

            "tick":
                tick,

            # -----------------------------
            # original state
            # -----------------------------

            "base_runtime_state":
                runtime_entity.runtime_state,

            # -----------------------------
            # node layer
            # -----------------------------

            "node_runtime_results":
                node_runtime_results,

            "node_runtime_state":
                node_runtime_state,

            # -----------------------------
            # passive layer
            # -----------------------------
       
            "passive_runtime_results":
                passive_runtime_results,
                
            "passive_runtime_state":
                passive_runtime_state,
                
            # -----------------------------
            # modulation layer
            # -----------------------------

            "modulation_output":
                modulation_output,
                
            "modulated_runtime_state":
                modulated_runtime_state,
                
            # -----------------------------
            # hir layer
            # -----------------------------

            "hir_output":
                hir_output,

            # -----------------------------
            # behavior layer
            # -----------------------------

            "behavior_output":
                behavior_output
        }


        # =================================
        # debug snapshot
        # =================================

        runtime_output[
            "runtime_snapshot"
        ] = build_runtime_snapshot(

            node_runtime_results=
                node_runtime_results,

            passive_runtime_results=
                passive_runtime_results,

            modulation_output=
                modulation_output,

            hir_output=
                hir_output,

            behavior_output=
                behavior_output,

            tick=
                tick
        )

        return runtime_output

