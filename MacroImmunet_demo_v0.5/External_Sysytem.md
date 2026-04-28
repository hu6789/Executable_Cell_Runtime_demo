🌍 External System (v0.5)
Overview

The External System of MacroImmunet governs how cells interact with the environment and with each other.

It defines how:

the world is perceived (ScanMaster),
signals are translated into decision inputs (InputBuilder),
cell decisions are materialized into actions (IntentBuilder),
and actions are resolved into world state (LabelCenter).

This forms a closed loop between cells and environment.

Execution Pipeline

Each simulation tick:

World State (fields + cells)
    ↓
ScanMaster         (event detection)
    ↓
InputBuilder       (structured perception → node input)
    ↓
CellMaster / InternalNet
    ↓
IntentBuilder      (decision → intent)
    ↓
LabelCenter        (intent → world update)
    ↓
Updated World State
Key Principle

The external system operates entirely through Events → Inputs → Intents → Field Projection

And enforces:

❗ No direct world modification outside LabelCenter
❗ No raw field exposure to decision systems
❗ No direct cell-to-cell mutation
🧠 Core Components
1. ScanMaster
Role

Transforms the world into discrete events.

Responsibilities
Detect:
cell–cell contacts
local field signals
environmental context (e.g. hotspot)
Convert continuous world state into:
Event list
Event Schema
{
  "event_id": "...",
  "type": "field_signal | contact | context | ...",

  "source": {
    "type": "cell | field | world",
    "id": "..."
  },

  "target": {
    "type": "cell | broadcast",
    "id": "..."
  },

  "payload": {},

  "meta": {
    "position": [x, y],
    "distance": 1.2,
    "tick": 123
  }
}
Constraints
Does NOT interpret biology
Does NOT make decisions
Only performs detection + encoding
2. InputBuilder
Role

Transforms events into structured decision inputs for cells.

Responsibilities
1️⃣ Aggregation

Merge:

field signals
contact events
context tags

into:

external_field
2️⃣ ASI Modulation (optional)

Applies antigen-specific modulation:

TCR–pMHC matching
affinity weighting
3️⃣ Mapping

Convert:

external_field → node_input

via:

node schema (external_key)
mapping rules
4️⃣ Interpretation ⭐

Generate biologically meaningful abstractions:

effective signals
contact flags
nonlinear responses

Example:

effective_pMHC = f(distance, concentration)
contact_infected = True
IL2_signal = sigmoid(IL2)
Output
node_input (fixed schema)
Key Idea

We do NOT expose raw fields — only a structured decision interface.

3. ASI (Adaptive Specificity Interpreter)
Role

Applies antigen-specific matching logic on top of perception.

Responsibilities
Evaluate binding likelihood:
match_score = pMHC × receptor specificity
Select best interaction target
Modulate signals (not generate new ones)
Constraints
Acts as a modifier, not a decision layer
Input/output schema identical to InputBuilder
4. IntentBuilder
Role

Transforms cell decisions into world-action requests (intents).

Responsibilities

Convert:

behavior outputs
state updates
fate decisions

into unified:

Intent objects
Intent Schema
{
  "type": "interaction | field | fate",

  "source": "cell_id",

  "target": "cell_id | null",

  "payload": {
    "kind": "damage | secretion | ...",
    "value": 0.5
  },

  "meta": {
    "position": [x, y]
  }
}
Constraints
No direct world writes
No physics
Only expresses what should happen
5. LabelCenter
Role

The only system allowed to modify the world.

Responsibilities
1️⃣ Intent Collection
intents → queue
2️⃣ Intent → Source

Convert intents into:

source terms
3️⃣ Projection (Kernel-based) ⭐
field[x] += Σ source × kernel(distance)

Kernel types:

Gaussian (default)
Top-hat
directional (optional)
4️⃣ Aggregation

Combine all contributions:

field += sum(all sources)
5️⃣ Dynamics

Apply:

diffusion
decay
(optional) saturation
Key Insight

LabelCenter does NOT reconstruct reality —
it projects local effects into a continuous evolving field

Constraints
❗ No direct behavior logic
❗ No decision-making
❗ No dependence on execution order
🔄 System-Level Properties
1. Event-Driven Perception

World → Events → Inputs

2. Structured Decision Interface

Cells only see:

node_input

NOT:

raw fields
full environment
3. Intent-Based Action

All actions must be expressed as:

Intent → LabelCenter → World
4. Deferred Execution

All world updates occur:

at end of tick (atomic apply)
5. Field as Ground Truth

The world is represented as:

continuous fields + cell instances
🌱 Design Philosophy
Separation of Concerns
Layer	Responsibility
ScanMaster	detect
InputBuilder	translate
InternalNet	decide
IntentBuilder	express
LabelCenter	realize
Controlled Complexity

Only expose what is necessary for decision-making.

Multi-Scale Compatibility

Supports:

agent-based modeling
reaction-diffusion systems
particle-inspired projection
📌 One-Sentence Summary

MacroImmunet external system converts continuous world → discrete perception → structured decision → projected action → evolving fields.
