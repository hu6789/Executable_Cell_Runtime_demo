# CellMaster Engine (MacroImmunet v0.5)

## 🧠 Role

CellMaster is the **orchestration layer** responsible for:

- managing cell instances
- scheduling InternalNet execution
- converting decisions into intents

It acts as the bridge between:


ScanMaster → Cell → InternalNet → IntentBuilder → LabelCenter


---

## 🧩 Responsibilities

### 1. Cell lifecycle management

- create cell instances (via CellFactory)
- maintain identity and spatial position
- track alive/dead state

---

### 2. Decision scheduling

For each tick:

``` id="g3l4nn"
for cell in cells:
    external_field = scan_result[cell]
    result = internal_net.step(cell, external_field)
3. Decision translation

Convert InternalNet outputs:

behavior_outputs → intents

CellMaster itself does NOT:

evaluate behaviors
modify node_state
apply world updates
4. System boundary enforcement

CellMaster ensures:

Rule	Meaning
❌ no direct world write	must go through Intent
❌ no biological logic	handled by InternalNet
❌ no fate override	HIR is final authority
🧬 Core Components
Cell (cell_instance.py)

Runtime container for a single cell.

class Cell:
    id
    type
    position

    node_state

    params = {
        "feature": {},
        "receptor": {},
        "behavior": {}
    }

    status = {
        "alive": True
    }

    meta
CellFactory (cell_factory.py)

Creates cells from templates.

Responsibilities:
load template JSON
initialize node_state
sample parameters
apply subtype variation
Cell Templates (cell/*.json)

Define parameter layer only

DO NOT include:

graph
behavior logic
HIR rules

Example:

{
  "cell_type": "cd8_t",

  "init_node_state": {
    "ATP": 0.6,
    "stress": 0.1
  },

  "hir_params": {
    "energy_from_ATP": 1.0
  },

  "behavior_params": {
    "release_perforin": {
      "sensitivity": 1.5
    }
  }
}
⚙️ Execution Pipeline

Per tick, per cell:

1️⃣ Input
external_field = ScanMaster output
2️⃣ InternalNet Execution
result = internal_net.step(cell, external_field)

Includes:

node update
passive dynamics
HIR (fate + modifiers)
behavior evaluation
state update
3️⃣ Output
result = {
    behaviors,
    fate,
    hir,
    features
}
4️⃣ Intent Conversion (next stage)
behaviors → intents → LabelCenter.apply()
🔄 Data Ownership
Data	Owner
node_state	InternalNet
parameters	Cell
fate	HIR
behaviors	BehaviorEngine
world state	LabelCenter
🧠 Design Principles
1. Strict Layer Separation
Layer	Responsibility
CellMaster	orchestration
InternalNet	biology
LabelCenter	world
2. Stateless Scheduling

CellMaster does NOT accumulate hidden state.

All state is inside:

cell.node_state
3. Parameter-driven diversity

Cells differ by:

feature_params
receptor_params
behavior_params

NOT by logic branching.

4. HIR Authority

HIR has final control over:

fate (dying / stressed / normal)
behavior suppression (blocks)
scaling (group_modifiers)

CellMaster MUST NOT override HIR.

🚫 Anti-patterns

❌ Injecting graph into cell instance
❌ Modifying node_state outside InternalNet
❌ Letting behavior directly affect world
❌ Encoding biology inside CellMaster

🔧 Extension Points
IntentBuilder integration
spatial movement controller
cell-cell interaction policies
multi-state lifecycle (naive → activated → exhausted)
✅ Summary

CellMaster is a pure execution coordinator:

owns cell instances
runs InternalNet
forwards outputs to next layer

It guarantees:

modularity
determinism
clean system boundaries
