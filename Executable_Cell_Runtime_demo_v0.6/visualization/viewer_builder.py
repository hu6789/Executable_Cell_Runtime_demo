from visualization.viewer import Viewer


class ViewerBuilder:

    def build(

        self,

        snapshots,

        scenario_name="Unknown"

    ):

        self.viewer = Viewer(

            snapshots=snapshots,

            scenario_name=scenario_name

        )

        return self.viewer

    def launch(self):

        self.viewer.run()


def build_viewer(

    snapshots,

    scenario_name="Unknown"

):

    return ViewerBuilder().build(

        snapshots,

        scenario_name

    )


def launch_viewer(

    snapshots,

    scenario_name="Unknown"

):

    build_viewer(

        snapshots,

        scenario_name

    ).run()
