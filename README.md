# Executable Cell Runtime v0.6 — Multi-Cell Simulation Core

# 1.Overview

Executable Cell Runtime (ECR) is a graph-driven runtime framework for executable biological cells, where cellular behaviors emerge from executable internal networks and interactions with the surrounding environment.

Unlike traditional agent-based simulations that represent cells as predefined behavioral agents, ECR models cells as programmable runtime entities. Each cell is constructed from declarative templates, assembled with executable molecular graphs, and executed through a layered intracellular runtime.

At runtime, environmental events are translated into intracellular signals, processed through cellular execution networks, and converted into world-level changes through a controlled intent-based update system. This creates a closed computational loop between extracellular conditions, intracellular state transitions, cellular behaviors, and multicellular dynamics.

The goal of ECR is to provide a general runtime architecture for modeling biological cells as executable systems, where cellular diversity, state transitions, and behaviors emerge from graph composition, runtime regulation, and environmental interactions rather than hard-coded cell-specific logic.

# 2.Core Concepts
## 2.1 Cell as executable runtime entity

In ECR, a cell is not represented as a static data container, but as an executable runtime entity capable of maintaining internal states, receiving external signals, executing intracellular computation, and producing biological actions.

A cell runtime entity is constructed through a three-stage process:

Cell Template
        ↓
Cell Factory
        ↓
Runtime Entity
Cell Template

The cell template defines the initial specification and biological identity of a cell type.

It describes:

cellular identity and lineage information
initial intracellular node states
runtime parameters
associated internal graph references
HIR capability profiles
environmental exposure rules

A template does not execute any biological process. It only provides the blueprint required for runtime construction.

Example:

host_cell template

identity:
    cell_type = host
    lineage = host

graph_refs:
    base_graph
    host_graph

init_node_state:
    ATP
    DNA
    RNA
    protein
    membrane
    pathogen_signal

The template therefore defines what a cell is initialized as, rather than what a cell does.

Cell Factory

The Cell Factory is the construction layer responsible for transforming a template into an executable object.

Its responsibilities include:

loading the selected cell template
initializing stochastic runtime states
assembling internal execution graphs
attaching runtime execution contexts
constructing the runtime entity

The factory performs:

Template Definition
        +
Runtime Graph Assembly
        +
Initial State Initialization
        ↓
Executable Cell Entity

The factory does not execute cellular behaviors or modify the world state. It only creates the runtime object.

Runtime Entity

The resulting runtime entity is the executable representation of a cell during simulation.

A runtime entity contains:

Runtime Entity

├── Identity
│
├── Runtime State
│      └── intracellular node values
│
├── Runtime Graph
│      ├── nodes
│      ├── behaviors
│      └── edges
│
├── HIR Capability
│
├── Exposure Rules
│
└── Runtime Parameters

During simulation, each runtime entity can:

receive external perception inputs from the environment
World interaction
        ↓
ScanMaster
        ↓
InputBuilder
        ↓
Cell Runtime Input
execute intracellular computation
Node Runtime
        ↓
Passive Runtime
        ↓
Runtime Modulation
        ↓
HIR
        ↓
Behavior Runtime
produce semantic actions
Behavior Output
        ↓
IntentBuilder
        ↓
Intent
        ↓
LabelCenter
        ↓
World Update

Therefore, a cell runtime entity forms a closed executable loop:

             World
               ↑
               |
        LabelCenter
               ↑
            Intent
               ↑
        Behavior Output
               ↑
        Internal Runtime
               ↑
        Runtime Entity
               ↑
        InputBuilder
               ↑
             World

Unlike traditional agent-based models where cells are rule-driven agents with predefined behaviors, ECR treats cells as graph-executable biological systems. Their behaviors are not directly encoded as fixed actions but emerge from the interaction between:

internal executable networks,
runtime physiological states,
regulatory modulation,
environmental signals.

Thus, the cell is the fundamental computational unit of ECR: a self-contained executable biological runtime capable of state evolution, decision generation, and interaction with the simulated ecosystem.


## 2.22.2 Graph-driven intracellular execution

In ECR, intracellular computation is represented as an executable graph system rather than a collection of manually defined behavioral rules.

Each runtime cell contains an internal execution graph assembled from multiple graph fragments, including:

node definitions
behavior definitions
regulatory structures
lineage- or cell-type-specific extensions

The graph defines the computational structure of the cell, while runtime engines interpret and execute this structure.

The overall intracellular execution flow is:

Runtime Graph
      |
      ↓
Node Runtime
      |
      ↓
Passive Regulation
      |
      ↓
Runtime Modulation
      |
      ↓
HIR Regulation
      |
      ↓
Behavior Execution
Node: intracellular computational state

Nodes represent the fundamental intracellular variables of a cell.

A node is not simply a stored value, but an executable computational element whose value is determined by graph contributions and runtime conditions.

Examples include:

Metabolism:
    ATP
    glucose
    mitochondria

Information:
    DNA
    RNA
    protein

Stress:
    ROS
    Ca

Immune signals:
    pathogen_signal
    TCR
    pMHC
    cytokines

During runtime, the Node Engine evaluates each node through:

Incoming Graph Contributions
            ↓
Contribution Transformation
            ↓
Category Aggregation
            ↓
Node Skeleton Formula
            ↓
Runtime Gate
            ↓
Final Node State

Therefore, node values are dynamically computed from the internal graph rather than directly assigned.

For example:

glucose
    ↓
mitochondria
    ↓
ATP production
    ↓
ATP state

represents a computational dependency rather than a static annotation.

Passive: continuous physiological regulation

Passive systems represent intrinsic physiological processes that continuously affect cellular states.

Unlike behaviors, passives are not intentional cellular actions. They describe unavoidable physical and biochemical consequences.

Examples:

Ca overload
        ↓
ROS increase

ROS accumulation
        ↓
protein damage

ATP depletion
        ↓
cellular stress

Passive execution follows:

Runtime State
      ↓
Passive Gate
      ↓
Passive Formula
      ↓
Passive Transformation
      ↓
State Adjustment

Passives therefore provide continuous background dynamics that maintain physiological realism.

They model processes such as:

metabolic stress
molecular degradation
ion imbalance
damage accumulation

The passive layer ensures that cellular states evolve even without explicit behavioral activation.

HIR: hierarchical internal regulation

HIR (Hierarchical Internal Regulation) represents the regulatory layer that determines how internal conditions influence cellular priorities.

HIR does not directly execute behaviors. Instead, it modulates the cellular execution landscape by interpreting runtime states.

Inputs include:

Node States
    +
Passive Effects
    +
Runtime Modulation
    ↓
HIR

HIR evaluates conditions such as:

energy availability
cellular stress
damage level
pathogen burden
activation signals

and produces regulatory outputs that influence behavior execution.

Conceptually:

Internal State
       ↓
HIR Interpretation
       ↓
Behavior Regulation
       ↓
Behavior Selection

HIR therefore acts as the bridge between physiological state and cellular response.

It allows the same behavioral graph to produce different outcomes depending on cellular conditions.

Behavior: executable cellular actions

Behaviors represent executable biological processes generated by the internal network.

Examples:

Host cell:

pathogen detection
        ↓
CXCL10 production
        ↓
immune signaling

CD8 T cell:

TCR activation
        ↓
perforin production
        ↓
target cell killing

Viral infection:

viral RNA
        ↓
viral protein production
        ↓
assembly
        ↓
budding

Behavior execution follows:

Behavior Graph
       ↓
Contribution Evaluation
       ↓
Behavior Drive Calculation
       ↓
HIR Regulation
       ↓
Runtime Scaling
       ↓
Behavior Package

The output of the behavior layer is not a direct world modification.

Instead:

Behavior Output
        ↓
Intent
        ↓
LabelCenter
        ↓
World Update

This preserves the separation between intracellular computation and world state management.

Executable intracellular architecture

Together, the four components form a layered intracellular runtime:

                    Runtime Graph

                         |
        --------------------------------
        |              |               |
      Nodes        Passives          Behaviors
        |              |               |
        -------- Runtime State --------
                         |
                        HIR
                         |
                  Behavior Regulation
                         |
                  Behavior Execution
                         |
                      Intent

The key principle of ECR is:

Cellular behavior is not predefined as an external rule. It emerges from executable graph computation operating on evolving intracellular states.

Therefore, the intracellular system of ECR is a graph-driven runtime where:

Nodes define what the cell contains
Passives define how physiology continuously evolves
HIR defines how internal states regulate priorities
Behaviors define what biological actions can emerge

Together, these components transform a static cell description into an executable biological system.


## 2.3 Intent-based world mutation

In ECR, cellular computation and world modification are strictly separated.

A cell never directly writes to the world state.

Instead, cellular behaviors generate semantic intents, which are interpreted and applied by a centralized world-state management layer.

The mutation pipeline is:

Cell Runtime Entity
          |
          ↓
InternalNet Execution
          |
          ↓
Behavior Output
          |
          ↓
IntentBuilder
          |
          ↓
Intent
          |
          ↓
LabelCenter
          |
          ↓
World State Update

This design separates biological decision generation from environmental state mutation.

Cell does not write the world

In traditional agent-based simulations, an agent often directly modifies the environment:

Agent
  ↓
modify environment

This creates tight coupling between decision logic and world representation.

In ECR, this coupling is removed:

Cell
  ↓
Behavior computation
  ↓
Intent generation
  ↓
World mutation authority

The cell runtime has no authority to directly modify:

extracellular fields
particles
other cells
spatial structures
links or interactions

The cell only produces a description of a possible biological effect.

For example:

A host cell detecting viral infection does not directly create an interferon field:

❌ Host Cell
      ↓
   World.IFN += value

Instead:

Host Cell
      ↓
CXCL10 release behavior
      ↓
Intent:
    {
        target: extracellular_field,
        action: release,
        substance: CXCL10,
        amount: x
    }
      ↓
LabelCenter
      ↓
Field update

The biological computation and world mutation remain independent.

Intent as the universal mutation language

Intent is the semantic interface between intracellular computation and the external world.

A behavior output is converted into an intent describing:

what should change
where the change occurs
how the change should be applied
the magnitude of the change

Conceptually:

Behavior Output

    {
        behavior:
            cytokine_release,

        strength:
            0.8
    }

          ↓

Intent

    {
        type:
            field_update,

        target:
            CXCL10,

        operation:
            release,

        value:
            0.8
    }

The intent layer therefore provides a common semantic language for all biological actions.

Different biological systems can produce the same type of world mutation without directly depending on each other.

For example:

Host Cell
    ↓
CXCL10 release intent


Immune Cell
    ↓
Chemotaxis intent


Virus
    ↓
Budding intent

All are translated into world changes through the same mutation mechanism.

LabelCenter as world-state authority

LabelCenter is the Single Source of Truth (SSOT) for world state mutation.

Its responsibilities are:

collect intents
validate mutation requests
aggregate compatible changes
apply world updates
maintain consistency

The mutation process:

Intent Queue
      ↓
Intent Bucketing
      ↓
Semantic Aggregation
      ↓
World Projection
      ↓
Cleanup

LabelCenter manages different mutation categories:

Intent

├── Entity Update
│
├── Runtime State Update
│
├── Field Projection
│
├── Directed Effect
│
└── Link Update

This prevents individual runtime components from creating inconsistent world states.

Benefits of intent-based mutation
Modular biological computation

Cells only need to produce biological meanings.

They do not need to know:

how fields are stored
how particles diffuse
how spatial structures are updated

Therefore:

Cell Logic
≠
World Implementation
Global consistency

Because all mutations pass through LabelCenter:

conflicting requests can be merged
updates can be ordered
world transitions remain deterministic

Example:

Multiple cells release cytokines:

Cell A
    ↓
IFN release intent

Cell B
    ↓
IFN release intent

Cell C
    ↓
IFN release intent


        ↓

LabelCenter

        ↓

Combined field update
Multi-scale extensibility

The same intent mechanism supports different biological scales:

Molecular:

protein production


Cellular:

cell activation


Tissue:

cytokine diffusion


Ecological:

population interaction

All are expressed as world mutation intents.

ECR mutation architecture

The complete separation is:

          Intracellular Runtime

       Node
        |
     Passive
        |
       HIR
        |
    Behavior
        |
        ↓

       Intent

        |
        ↓

    LabelCenter

        |
        ↓

       World

The fundamental rule of ECR is:

Cells compute biological decisions, but only intents can change the world.

By enforcing intent-based mutation, ECR achieves a clean separation between:

biological reasoning,
runtime execution,
environmental state management.

This allows executable cells to evolve complex behaviors while keeping the simulated ecosystem consistent, extensible, and interpretable.


# 3.Architecture and Runtime Lifecycle

ECR adopts a layered runtime architecture that integrates environmental perception, intracellular execution, semantic action generation, and centralized world-state mutation into a unified simulation framework.

Unlike traditional agent-based systems where cellular agents directly modify environmental states, ECR separates biological computation from world mutation. Cells operate as executable runtime entities that receive environmental information, perform intracellular graph-based computation, generate biological behaviors, and communicate with the external environment through intent-based interactions.

The overall architecture follows a closed-loop execution cycle:

World State
      |
      v
Perception
      |
      v
Runtime Input
      |
      v
Cellular Execution
      |
      v
Behavior Generation
      |
      v
Intent-based Mutation
      |
      v
Updated World State

This architecture enables cellular behaviors to emerge from interactions between intracellular states, regulatory mechanisms, and environmental conditions.

## 3.1 Overall Architecture

The ECR runtime consists of five major functional layers:

                        World
                          |
                          |
                  +---------------+
                  |  ScanMaster   |
                  |  Perception   |
                  +---------------+
                          |
                  Biological Events
                          |
                          v
                  +---------------+
                  | InputBuilder  |
                  | Signal        |
                  | Translation   |
                  +---------------+
                          |
                   Runtime Inputs
                          |
                          v
                  +---------------+
                  | CellMaster    |
                  | Runtime       |
                  | Orchestration |
                  +---------------+
                          |
                          v

             =================================
                Intracellular Runtime Network
             =================================

                  +---------------+
                  | Node Engine   |
                  +---------------+

                  +---------------+
                  | Passive       |
                  | Engine        |
                  +---------------+

                  +---------------+
                  | Runtime       |
                  | Modulation    |
                  +---------------+

                  +---------------+
                  | HIR           |
                  +---------------+

                  +---------------+
                  | Behavior      |
                  | Engine        |
                  +---------------+

                          |
                   Behavior Output
                          |
                          v

                  +---------------+
                  | IntentBuilder |
                  +---------------+
                          |
                          v

                  +---------------+
                  | LabelCenter   |
                  | World SSOT    |
                  +---------------+
                          |
                          v

                        World

The architecture separates responsibilities across layers.

Environmental perception layer

The perception layer connects the simulation environment with individual cells.

ScanMaster observes spatial relationships, extracellular signals, and biological interactions within the world. It converts environmental changes into standardized biological events.

InputBuilder then translates these events into intracellular computational inputs by applying signal interpretation, receptor processing, and semantic transformation.

This layer does not perform cellular decisions. It only provides information entering the runtime system.

Runtime orchestration layer

CellMaster acts as the execution coordinator of cellular runtime.

Its responsibilities include:

scheduling cellular execution
constructing runtime contexts
invoking intracellular computation
collecting runtime outputs

CellMaster does not perform biological reasoning and does not directly modify the world.

Instead, it coordinates execution between external inputs and the intracellular runtime network.

Intracellular execution layer

The intracellular runtime network is the computational core of ECR.

Each runtime cell contains an executable graph composed of:

intracellular nodes
physiological regulation mechanisms
regulatory modulation
hierarchical control
executable behaviors

The runtime network transforms cellular states into biological actions through graph-driven computation.

Semantic mutation layer

The output of cellular computation is represented as semantic intents.

Behaviors do not directly update environmental states. Instead:

Behavior Output
        |
        v
Intent
        |
        v
LabelCenter
        |
        v
World Update

IntentBuilder converts runtime behavior outputs into standardized world mutation requests.

LabelCenter serves as the single source of truth for world-state modification, ensuring that all environmental changes are applied consistently.

## 3.2 Runtime Lifecycle

ECR advances the simulation through discrete runtime ticks.

Each tick represents one complete perception–computation–mutation cycle.

The execution sequence is:

Simulation Tick

        |
        v

1. Scan

        |
        v

2. Input Translation

        |
        v

3. Runtime Scheduling

        |
        v

4. Cell Execution

        |
        v

5. Substance Interaction

        |
        v

6. Intent Generation

        |
        v

7. World Commit
1. Scan

At the beginning of each tick, the current world state is analyzed by the perception layer.

ScanMaster detects:

spatial interactions
environmental changes
cell–cell contacts
extracellular signals

The result is a set of standardized biological events.

2. Input Translation

Detected events are translated into intracellular signals.

InputBuilder performs:

event dispatching
semantic processing
receptor interpretation
field signal conversion

The output is a set of runtime inputs delivered to corresponding cells.

3. Runtime Scheduling

CellMaster determines which runtime entities should execute during the current tick.

The scheduler evaluates:

execution eligibility
runtime priority
persistence conditions
computational budget

Only eligible cells enter intracellular execution.

4. Cell Execution

Each scheduled cell executes its internal runtime network.

The execution sequence is:

Node Runtime
      |
      v
Passive Regulation
      |
      v
Runtime Modulation
      |
      v
HIR Regulation
      |
      v
Behavior Execution

The result is a set of behavior outputs representing potential biological actions.

5. Substance Interaction

Extracellular substances and molecular entities are processed through the substance interaction layer.

SubstanceMaster evaluates biochemical interactions and generates corresponding requests.

This allows extracellular molecules to influence:

cellular states
environmental fields
molecular interactions

without directly bypassing the runtime architecture.

6. Intent Generation

Behavior outputs and interaction requests are converted into semantic intents.

An intent describes:

the biological meaning of the change
the target object
the magnitude of the effect
the mutation category

Intents provide a unified interface between biological computation and world dynamics.

7. World Commit

At the end of the tick, LabelCenter applies all accepted intents.

The commit process includes:

intent collection
aggregation
validation
world projection
cleanup

After commit, the updated world state becomes the input for the next simulation tick.

Summary

The ECR architecture establishes a closed computational loop:

World
  ↓
Perception
  ↓
Cell Runtime
  ↓
Internal Graph Execution
  ↓
Behavior
  ↓
Intent
  ↓
World Mutation

By separating perception, intracellular computation, and world mutation, ECR enables biological entities to function as executable runtime systems rather than predefined rule-based agents.

This architecture provides the foundation for representing cellular physiology, immune interactions, and multicellular dynamics through a unified graph-driven simulation framework.


# 4.Example Simulation

The adaptive immune response scenario can be executed through the provided Python runtime entry point:

python3 test_adaptive_immunity_demo.py

## 4.1Adaptive Immune Response Scenario

This demo provides an example application of Executable Cell Runtime (ECR) for modeling dynamic immune interactions through an executable, spatially resolved simulation framework.

The current scenario demonstrates a simplified antiviral immune response, showing how extracellular signals, intracellular state transitions, cellular decision processes, and multicellular interactions can be represented within a unified runtime environment.

Rather than explicitly encoding a predefined biological sequence, the simulation represents immune responses as emergent outcomes of executable intracellular networks and environment-mediated interactions.

---

## 4.2Visualization Interface

The visualization system provides multi-scale observation of simulation dynamics.

The central 2D environment represents the spatial organization of cells and extracellular signals, allowing observation of cellular movement, interaction events, and signal distribution over time.

The event panel records temporal changes during simulation, including environmental stimuli, cellular responses, and biological interaction events.

The entity inspection panel provides detailed information for individual entities, including intracellular runtime states, activated behaviors, and extracellular signal information.

Together, these views connect:

* spatial-level biological dynamics,
* cellular-level decision processes,
* intracellular molecular state transitions.

This enables direct observation of how local cellular computation contributes to system-level immune responses.

---

## 4.4Simulation Scenario

The demonstration follows a simplified antiviral immune response involving a host cell, viral perturbation, CD4 T cells, and CD8 T cells.

### 1. External Stimulus and Host State Transition

An influenza-associated extracellular signal is introduced into the environment as an external perturbation.

The host cell receives environmental input through the runtime perception pipeline. These signals are translated into intracellular inputs and processed by the executable internal network.

The resulting intracellular state transition activates host responses, including viral-associated processing and antigen presentation.

Following viral accumulation, antigen presentation is represented through generation of pMHC-related signals, which become available as extracellular communication cues.

---

### 2. Signal-Mediated Immune Cell Activation

The released antigenic signal forms a spatially distributed extracellular cue.

CD4 T cells detect this signal through receptor-associated recognition mechanisms. Intracellular processing leads to activation of cytokine-related behaviors and IL-2 production.

The extracellular IL-2 signal provides an additional communication channel, allowing immune cells to influence neighboring cellular states through environmental interactions.

---

### 3. Adaptive Response Amplification and Effector Activation

The combined antigenic and cytokine signals contribute to CD8 T cell activation.

Through intracellular runtime computation, CD8 T cells integrate receptor signals, internal state conditions, and regulatory modulation to determine behavior activation.

Activated CD8 T cells initiate an effector program represented by perforin production and release.

---

### 4. Cellular Response Outcome

Released effector signals interact with the infected target cell.

The resulting directed interaction modifies target-cell runtime conditions, leading to progressive reduction of cellular integrity.

This represents the transition from immune recognition to functional cellular outcome.

---

## 4.5Purpose of the Demonstration

This scenario demonstrates the ability of Executable Cell Runtime to represent biological processes as executable state transitions.

The simulation connects:

* extracellular environmental signals,
* intracellular executable networks,
* cellular decision processes,
* multicellular interactions,
* and world-level state changes.

Through this architecture, biological behaviors are not represented as isolated scripted events, but emerge from interactions between executable intracellular models and dynamic environments.


# Development Note

The detailed documentation is currently under construction. The project architecture is undergoing further updates, including the integration of regulatory programs for behavior modulation and future lineage-based cell state transitions. This project has been developed with extensive assistance from artificial intelligence tools for architecture exploration, implementation support, and iterative design refinement.


