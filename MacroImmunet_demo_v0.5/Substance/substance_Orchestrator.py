class SimulationRuntime:

    def __init__(self, world, scan_master, input_builder,
                 substance_master, cell_master, intent_builder, label_center):

        self.world = world
        self.scan_master = scan_master
        self.input_builder = input_builder
        self.substance_master = substance_master
        self.cell_master = cell_master
        self.intent_builder = intent_builder
        self.label_center = label_center

    def step(self, tick):

        # 1️⃣ Scan（A层）
        events = self.scan_master.scan(tick)

        # 2️⃣ InputBuilder（B层双发）
        inputs = self.input_builder.build(
            events,
            cells=self.world.cells,
            world=self.world
        )

        cell_inputs = inputs["cell"]
        substance_inputs = inputs["substance"]

        # 3️⃣ C层：各自决策（完全独立）
        substance_actions = self.substance_master.step(substance_inputs)
        cell_actions = self.cell_master.step(cell_inputs)

        # 4️⃣ 汇总 → IntentBuilder
        all_actions = substance_actions + cell_actions
        intents = self.intent_builder.build(all_actions)

        # 5️⃣ Apply（唯一写世界）
        self.label_center.apply(intents)
