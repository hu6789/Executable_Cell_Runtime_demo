# visualization/event_builder.py


"""
=========================================================
Visualization Event Builder
=========================================================

Convert runtime outputs into human-readable events.

This layer is ONLY for visualization.

It does NOT:
- create biological events
- modify runtime
- affect simulation


Input sources:
    - scan/input exposure
    - behavior output
    - substance behavior
    - runtime events


Output:
    viewer-friendly event list
"""


class VisualizationEventBuilder:


    def build(

        self,

        tick,

        state_snapshot=None,

        runtime_result=None

    ):


        events = []


        #
        # 1.
        # sensed signals
        #
        # field exposure / input events
        #

        events.extend(

            self.build_signal_events(

                tick,

                runtime_result

            )

        )


        #
        # 2.
        # cell behaviors
        #

        events.extend(

            self.build_behavior_events(

                tick,

                runtime_result

            )

        )


        #
        # 3.
        # substance behaviors
        #

        events.extend(

            self.build_substance_events(

                tick,

                runtime_result

            )

        )


        return self.deduplicate_events(events)
    # =====================================================
    # Signal
    # =====================================================


    def build_signal_events(

        self,

        tick,

        runtime_result

    ):


        output = []


        if runtime_result is None:

            return output


        #
        # current runtime event
        #
        # field exposure
        #

        for event in runtime_result.get(

            "events",

            []

        ):


            if event.get(

                "event_type"

            ) != "field_exposure_event":

                continue



            target = event.get(

                "target_id"

            )


            payload = event.get(

                "payload",

                {}

            )


            field = payload.get(

                "field_type",

                "signal"

            )


            output.append(

                {

                    "tick": tick,

                    "category": "Signal",

                    "type": "field_exposure",

                    "source": field,

                    "target": target,

                    "message":
                        f"{target} sensed {field}",

                    "level": "info"

                }

            )


        return output



    # =====================================================
    # Cell Behavior
    # =====================================================


    def build_behavior_events(

        self,

        tick,

        runtime_result

    ):


        output = []


        if runtime_result is None:

            return output



        for package in runtime_result.get(

            "cell_packages",

            []

        ):


            cell_id = package.get(

                "cell_id"

            )


            behavior_output = package.get(

                "behavior_output",

                {}

            )


            trace = behavior_output.get(

                "behavior_trace",

                []

            )


            for item in trace:


                name = item.get(

                    "behavior",

                    "unknown"

                )


                strength = item.get(

                    "strength",

                    None

                )


                message = (
                    f"{cell_id} executed {name}"
                )

                output.append(

                    {

                        "tick": tick,

                        "category": "Behavior",

                        "type": "cell_behavior",

                        "source": cell_id,

                        "target": None,

                        "message": message,

                        "level": "success"

                    }

                )


        return output

    # =====================================================
    # Substance Behavior
    # =====================================================
    def build_substance_events(

        self,

        tick,

        runtime_result

    ):

        output = []


        if runtime_result is None:

            return output



        for item in runtime_result.get(

            "effect_events",

            []

        ):


            operation = item.get(
 
                "type",

                "effect"

            )


            source = item.get(

                "source",

                "substance"

            )


            target = item.get(

                "target"

            )
            
            if target == "cd8_001":
                continue

            if operation == "membrane_damage":

                message = (
                    f"{source} damaged {target} membrane"
                )


                output.append({

                    "tick": tick,

                    "category": "Substance",

                    "type": "directed_effect",

                    "source": source,

                    "target": target,

                    "message": message,

                    "level": "warning"

                })


        return output
   
    def deduplicate_events(
        self,
        events
    ):

        seen = set()

        output = []


        for event in events:
  
            key = (

                event.get("tick"),

                event.get("type"),

                event.get("source"),

                event.get("target"),

                event.get("message")

            )


            if key in seen:

                continue


            seen.add(key)

            output.append(event)


        return output
