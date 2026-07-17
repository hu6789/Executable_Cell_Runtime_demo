# substance/substance_master/substance_master.py

from substance.substance_master.interaction_context import (
    build_interaction_context
)

from substance.substance_master.rule_evaluator import (
    evaluate_interaction_rules
)

from substance.substance_master.target_gate import (
    evaluate_target_gate
)

from substance.substance_master.effect_strength import (
    compute_effect_strength
)

from substance.substance_master.effect_projection import (
    project_effect
)

from substance.substance_master.request_generator import (
    generate_requests
)

class SubstanceMaster:

    """
    Active biochemical interaction interpreter

    Does NOT:
        - update world
        - apply intents
        - run diffusion

    Only:
        substance → requests
    """

    def process(

        self,

        substance,

        template,

        candidate_cells=None,

        candidate_substances=None,

        world=None
    ):

        candidate_cells = (
            candidate_cells or []
        )

        candidate_substances = (
            candidate_substances or []
        )

        # ==========================
        # build context
        # ==========================

        context = build_interaction_context(

            substance=substance,

            nearby_cells=
                candidate_cells,

            nearby_substances=
                candidate_substances,

            world=world
        )
        # ==========================
        # evaluate rules
        # ==========================

        rules = evaluate_interaction_rules(

            interaction_context=context,

            template=template
        )
                
        all_requests = []
        
        # ==========================
        # per rule
        # ==========================

        for rule in rules:

            targets = (

                evaluate_target_gate(

                    interaction_context=
                        context,

                    interaction_rule=
                        rule
                )
            )

            for target in targets:

                strength_result = (

                    compute_effect_strength(

                        interaction_context=
                            context,

                        interaction_rule=
                            rule,

                        target=
                            target
                    )
                )

                effect = (

                    project_effect(

                        interaction_rule=
                            rule,

                        strength_result=
                            strength_result
                    )
                )
                

                requests = (

                    generate_requests(

                        substance_id=
                            substance.id,

                        projected_effect=
                            effect
                    )
                )

                all_requests.extend(
                    requests
                )


        return all_requests
