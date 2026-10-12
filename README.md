# 1. Overview and Core Concepts

## 1.1 What Is ECR?

The **Executable Cell Runtime (ECR)** is a modular framework for executing explicit, graph-based biological mechanisms in cellular models over discrete time steps.

ECR is built around the idea that cellular behavior can be represented through composable mechanisms whose components, relationships, and execution logic remain explicit. Its primary focus is not simply to predict cellular outcomes, but to provide a structured way to define, execute, and inspect the mechanisms that produce those outcomes.

The framework is intended to support biological models spanning multiple interacting scales, from molecular regulation and intracellular processes to cellular behavior and environmental interactions. By organizing these mechanisms into reusable components, ECR aims to support models containing different cell types while maintaining a shared computational framework.

This explicit mechanistic structure also provides a foundation for data-driven analysis. Experimental observations can eventually be used to evaluate model behavior, estimate parameters, and characterize uncertainty without requiring the biological mechanism graph itself to be treated as an automatically inferred black box.

## 1.2 Design Goals

ECR is organized around three connected goals:

- **Explicit mechanistic execution:** Represent biological components, their relationships, and their associated behaviors as inspectable and executable mechanisms.
- **Multi-scale and modular modeling:** Compose reusable mechanisms into models that connect different biological scales and accommodate distinct cell types within a shared environment.
- **Mechanism-guided data-driven analysis:** Establish a structured basis for comparing model behavior with experimental observations, calibrating model parameters, and evaluating predictive performance while retaining an explicit mechanistic model.

These goals are complementary. Explicit mechanistic execution defines the computational foundation; modular composition supports the construction of more complex biological models; and data-driven analysis provides a route toward evaluating and refining those models against experimental evidence.

ECR does not assume that biological mechanisms must be discovered automatically from data. The model structure remains an explicit part of the modeling process, while data-driven methods can be developed to assess and calibrate the resulting model.

## 1.3 Core Concepts

ECR uses several interconnected concepts to organize biological models and their execution:

- **World:** The shared simulation context in which cellular and environmental states evolve.
- **Cell Runtime:** The execution context responsible for evaluating a cell's applicable mechanisms and producing its state changes.
- **Graph:** A composable representation of biological components and their relationships, defining mechanisms that can be incorporated into execution.
- **Cell Type:** A representation of cellular identity that determines how applicable mechanisms and graph configurations are associated with a cell.
- **Lineage Tree:** A representation of developmental relationships among cell types. Each type can be associated with configuration information, including the graphs available or selected for its execution.

Together, these concepts provide the foundation for ECR: cells execute explicit mechanisms within a shared world, graph composition organizes the mechanisms available to them, and lineage relationships provide a developmental context for organizing cell types and their configurations.

## 2.1 Overall Architecture

ECR organizes simulation around a shared World and a globally synchronized execution cycle. Cells and environmental fields participate in the same simulation tick, progressing through a common sequence of stages rather than advancing independently through complete cell-level cycles.

The architecture separates environmental input, intracellular execution, output collection, and persistent state updates. Each stage operates within the same global tick, allowing the simulation to coordinate cellular mechanisms and environmental dynamics under a consistent execution schedule.

At a high level, the execution workflow consists of five stages:

1. **World state:** Establish the current persistent state of cells and environmental fields.
2. **Input preparation:** Prepare the relevant cellular and environmental information required by the current execution stage.
3. **Mechanism execution:** Execute the applicable cellular mechanisms and environmental processes according to the global schedule.
4. **Output collection:** Collect the results and effects produced during the current tick.
5. **State update:** Commit the collected changes to the persistent World state and advance the simulation to the next tick.

These stages describe the global simulation cycle, not five independent steps performed separately by each cell. All cells and fields participate in the same coordinated progression.

## 2.3 Intracellular Execution and Hierarchical Integration

Within the global execution cycle, each cell evaluates its applicable biological mechanisms through a modular runtime. Graph composition determines which mechanisms are available, while the runtime coordinates their execution using the cell's current state and prepared inputs.

The execution architecture separates several responsibilities:

- **Node processing** evaluates relationships between state variables.
- **Passive processes** represent state changes such as decay and diffusion.
- **Gene processing** handles gene-associated state and regulatory mechanisms.
- **Behavior execution** evaluates the mechanisms that produce cellular actions and other outputs.
- **HIR (Hierarchical Integration and Regulation)** coordinates and dispatches the execution of lower-level mechanisms, integrating regulatory influences and resource constraints into the execution process.

HIR is not itself a collection of biological formulas. It acts as an integration and coordination layer that determines how the relevant mechanisms are brought together and executed. The underlying engines remain responsible for their respective calculations, while HIR organizes their interactions and integrates their results.

This separation allows the runtime to coordinate complex cellular behavior without collapsing distinct biological mechanisms into a single monolithic execution component.

## 2.4 Globally Synchronized Tick Progression

ECR advances the entire simulation through discrete, globally synchronized ticks. Within a tick, cells and environmental fields participate in the same sequence of execution stages. The simulation progresses from the current World state through input preparation, mechanism execution, output collection, and state updates according to the global schedule.

**World state → Input preparation → Coordinated execution across cells and fields → Output collection → State update → Next tick**

The global tick defines the shared temporal boundary for the simulation. Individual cells do not independently complete a full tick before other cells begin theirs. Instead, the execution of cellular and environmental processes is coordinated as part of one simulation-wide progression.

This organization provides a consistent basis for modeling interactions among cells and environmental fields over time.

# 3. Key Design Details

## 3.1 Graph Composition and Cell Identity

ECR represents biological mechanisms as composable Graphs. Each Graph organizes biological components and their relationships into a unit that can be selected for cellular execution.

Graphs can be shared across multiple cell types or associated with specific cellular identities. A cell's type configuration determines which Graphs are permitted and which are active in its current execution context. This allows cells to reuse common mechanisms while retaining cell-specific mechanisms where necessary.

The Lineage Tree represents developmental relationships among cell types. Cell-type configurations are associated with nodes in this tree and organize information such as permitted and active Graphs. The tree describes developmental relationships, while the associated configurations determine how those relationships connect to executable mechanisms.

This separation allows ECR to represent developmental identity and mechanism composition independently, while linking them within a common model.

## 3.2 Division of Mechanistic Responsibilities

ECR separates biological state representation, state evolution, gene-associated regulation, and behavior execution into distinct responsibilities.

- **Node:** Represents a modeled biological entity or state variable, including structured or multi-component states. Nodes provide the state on which mechanisms operate.
- **Passive:** Represents state evolution that does not require an explicit behavior decision, such as decay or diffusion.
- **Gene:** Represents gene-associated baseline values and their modifications. Changes to these values belong to the gene-level state and can persist across ticks.
- **Behavior:** Represents an executable biological mechanism. Its execution evaluates relevant inputs and produces an intention or computational result.
- **HIR (Hierarchical Integration and Regulation):** Coordinates the invocation of relevant mechanisms and integrates regulatory influences and resource constraints into their execution.

These responsibilities are distinct but connected. Nodes represent modeled states; Passive processes describe particular forms of state evolution; Gene mechanisms handle gene-associated baseline changes; and Behaviors execute biological mechanisms. HIR coordinates these components without replacing their individual calculations with a single centralized formula.

## 3.3 HIR and Execution-Time Transcription-Factor Regulation

ECR distinguishes gene-level baseline modification from transcription-factor (TF) regulation applied during behavior execution.

Gene-associated baseline values and their modifications belong to the Gene layer. By contrast, TF regulation can modify the parameters or effective output of a relevant Behavior during the current tick. Such execution-time modulation does not, by itself, imply a persistent change to the gene's baseline state.

HIR coordinates this relationship by dispatching the relevant mechanisms and integrating TF-mediated adjustments into behavior execution. It also coordinates resource allocation and realization where these are required by the model.

The responsibilities are therefore separated as follows:

- **Gene** maintains and modifies gene-associated baseline state.
- **Behavior** executes the relevant biological mechanism and can be modulated by TFs during the current tick.
- **HIR** coordinates execution and connects regulatory modulation and resource handling to the appropriate behavior process.

HIR is an orchestration and integration layer, not a repository of biological formulas. The underlying mechanisms and their respective engines remain responsible for their own calculations.

This design makes persistent gene-level changes distinguishable from context-dependent regulatory effects on an individual behavior execution.

## 3.4 Persistent State and Tick-Level Execution

ECR distinguishes persistent simulation state from the intermediate state used during mechanism execution.

The **World** maintains the persistent state of the simulation across ticks. Each cell's runtime provides the context in which applicable mechanisms evaluate the current state, exchange intermediate results, and produce outputs for the current tick.

Mechanism execution and persistent state updates are separate responsibilities. A calculation performed during a tick does not automatically constitute a persistent World update; its result must be handled by the appropriate state-update process.

The simulation advances through globally synchronized ticks. Cells and environmental fields participate in the same sequence of stages, and their resulting changes are integrated according to the model's update rules. The updated World then provides the persistent starting state for the next tick.

This separation supports explicit state transitions and coordinated multi-cell execution while keeping biological calculations distinct from the management of persistent simulation state.


# 4. Current Scope and Limitations

## 4.1 Mechanistic Formulations and Biological Validation

The current ECR demonstrations use illustrative mechanistic formulations to exercise the runtime and explore how explicitly defined biological mechanisms can be executed over successive time steps.

These formulations are intended to support software development and simulation experiments. They have not yet been systematically calibrated against real biological time-series data or established as validated quantitative descriptions of the corresponding biological processes.

A simulation that runs successfully demonstrates the execution of a configured model, not necessarily the biological validity of its assumptions, equations, or parameter values.

Establishing biological validity will require suitable experimental datasets, explicit mappings between measured quantities and model states, parameter estimation, and evaluation against observations that were not used for calibration.

## 4.2 System Integration and Implementation Status

ECR is being developed incrementally across versions. The earlier v0.6 implementation includes an external runtime structure for coordinating simulation execution, while the v0.7.n series has prioritized changes to the internal execution engine, gene-associated mechanisms, lineage-related organization, and the integration of these components.

As a result, the external runtime components from v0.6 have not yet been fully migrated into v0.7.n. This reflects the current development sequence: changes to the core mechanisms and their interfaces have taken priority, with the integration and migration of the external runtime structure remaining ongoing work.

The architecture described in this document represents the intended overall design across these components and development stages. It should not be interpreted as a claim that the complete v0.6 external runtime and the newer v0.7.n internal execution engine have already been fully integrated into a single implementation.



## 4.3 Experimental Data Integration

The systematic use of real experimental data remains an open development task.

Several questions need to be addressed before quantitative biological validation can be established:

- **Dataset selection:** Identify experiments with suitable temporal resolution, measurable variables, and sufficient contextual information.
- **Observation-to-state mapping:** Define how experimental measurements correspond to ECR's modeled state variables and state components.
- **Parameter identification:** Determine which model parameters can be estimated from the available observations and which require independent evidence or constraints.
- **Model evaluation:** Assess whether a calibrated model reproduces observed dynamics and predicts held-out time points or experimental conditions.

These questions are not merely implementation details. They affect the design of the model, the interpretation of its parameters, and the strength of any biological conclusions drawn from simulation results.

## 4.4 Scope of Data-Driven Analysis

ECR is being developed toward a workflow that connects explicit mechanistic models with experimental evidence and quantitative model evaluation.

The future ECR-DA direction is intended to support evidence interpretation, parameter estimation, uncertainty characterization, and evaluation of model behavior against experimental observations. The biological mechanism graph remains an explicit part of the model rather than something that the data-analysis component is assumed to discover and rewrite automatically.

This direction is still under development. A systematic workflow for fitting real biological time-series data, quantifying uncertainty, and evaluating predictions under held-out conditions has not yet been established as a validated end-to-end capability.

## 4.5 Current Interpretation

ECR should therefore be understood as an evolving mechanistic simulation framework with an explicit architectural design and an implementation that is being developed incrementally.

Its current# 5. Roadmap: Toward ECR-DA

## 5.1 Near-Term Development Priorities

The next stage of ECR development will focus on identifying suitable approaches for integrating real experimental data and refining the design of the World. This work will include evaluating datasets against ECR's modeling requirements and developing the physical modeling knowledge needed to extend the representation of the simulation environment.

These investigations are expected to inform the next stage of architectural development. The immediate goal is to establish a clearer basis for connecting explicit mechanistic execution with experimental observations and a more expressive environmental model.

## 5.2 Runtime Integration and Migration

Migration of the external runtime components into the evolving v0.7.n architecture remains an outstanding development task. Rather than prioritizing this work immediately, the current plan is to first clarify the requirements arising from experimental data integration and the future development of the World.

The timing and scope of runtime integration will be revisited as these design decisions become clearer.

## 5.3 Toward Dedicated Data Analysis Development

ECR is intended to develop toward a dedicated data analysis component, referred to as **ECR-DA**. Its purpose is to support the analysis of experimental evidence in the context of explicitly defined mechanistic models.

The specific methods, capabilities, and implementation strategy for ECR-DA remain under exploration. Its development direction will be refined as suitable datasets are identified, modeling requirements become clearer, and the next-stage research direction is established.

This roadmap is therefore provisional rather than a fixed implementation schedule. Future updates will reflect the outcomes of these investigations and the requirements of the research direction pursued in the next stage. demonstrations provide a basis for developing and testing runtime mechanisms. Demonstrating that the framework can quantitatively reproduce and predict real biological dynamics remains a separate and necessary stage of development.


# 6. Data Provenance, AI Assistance, and Demonstrations

## 6.1 AI-Assisted Development

AI tools have been used to assist with code writing, debugging, and implementation tasks during ECR development. The architecture, design requirements, and development decisions are iteratively defined and reviewed as part of the project.

ECR is an evolving research-oriented software project, and its implementation and documentation remain subject to revision.

## 6.2 Demonstrations and Data Provenance

The v0.6 visualization demo provides an illustrative view of the simulation framework and its intended behavior.

The example data and mechanistic formulas used in the demonstrations are manually constructed for development and illustration. They should not be interpreted as experimental measurements, experimentally fitted parameters, or validated quantitative descriptions of biological systems.

The demonstrations are intended to illustrate software structure and mechanistic execution, rather than to claim biological validation.

## 6.3 Research Collaboration

ECR is an ongoing independent development project exploring explicit mechanistic execution, multi-scale biological modeling, and mechanism-guided data analysis.

I am currently exploring potential research directions and looking for a suitable research group or principal investigator (PI) with whom to develop the project further. I would welcome opportunities for research collaboration, academic guidance, or a student research position in which ECR could be refined and evaluated in the context of real biological questions and experimental data.
