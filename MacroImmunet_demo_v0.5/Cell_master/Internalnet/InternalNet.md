# InternalNet (v0.5)

## Overview

**InternalNet** is the core intracellular decision and dynamics engine of MacroImmunet.

It models how a single cell:

* processes signals,
* evolves internal physiological state,
* evaluates viability (HIR),
* selects behaviors,
* and updates itself accordingly.

It is a **closed-loop causal system**, not a simple rule engine.

---

## Execution Pipeline

Each simulation tick follows a strict, ordered pipeline:

```
external_field
    ↓
Node Engine        (signal integration)
    ↓
Passive Engine     (intrinsic / physical dynamics)
    ↓
HIR                (Homeostatic / Integrity Regulation)
    ↓
Behavior Engine    (decision layer)
    ↓
State Update       (feedback into node_state)
    ↓
Emitters           (output to external world)
```

### Key Principle

> Each layer has a **single responsibility** and must not overlap with others.

---

## Core Components

### 1. Node Engine

**Role:**
Transforms external signals and internal graph propagation into updated node states.

**Responsibilities:**

* Integrate receptor inputs (already mapped to node space)
* Propagate node → node signals via weighted graph
* Apply update rules per node (clamp, mode, etc.)

**Constraints:**

* Does NOT perform biological decisions
* Does NOT apply behavior effects
* Only computes **state evolution**

---

### 2. Passive Engine

**Role:**
Simulates intrinsic, non-decision biological processes.

**Examples:**

* Viral replication
* Calcium flux
* Resource depletion

**Characteristics:**

* Continuous dynamics
* No decision logic
* Executed before HIR and behavior

> Passive processes represent **physics/biochemistry**, not agency.

---

### 3. HIR (Homeostatic / Integrity Regulator)

**Role:**
Evaluates whether the cell is physiologically capable of acting.

**Input:**

* node_state

**Output:**

* `fate` (normal / stressed / dying / etc.)
* `group_modifiers` (scaling factors)
* `blocks` (hard constraints on behavior)

**Key Principle:**

> HIR has final authority over **biological feasibility**, but does not generate actions.

---

### 4. Behavior Engine

**Role:**
Selects actions based on current state and HIR constraints.

**Pipeline:**

1. Gate (threshold conditions)
2. Drive (weighted node inputs)
3. HIR modulation (block / scale)
4. Cell-specific parameter adjustment
5. Activation (deterministic or probabilistic)
6. Output (intent or internal state change)

**Output:**

* Behavior list with activation and effects

**Important:**

* Behavior inputs come **only from behavior definitions**, not from graph
* Supports **parallel execution of multiple behaviors**

---

### 5. State Update

**Role:**
Applies behavior effects back into node_state.

**Features:**

* Supports dynamic modes:

  * `instant`
  * `integrator`
  * `leaky`
  * `switch`
* Handles accumulation and decay
* Applies clamping (0–1)

**Constraints:**

* No HIR logic here
* No decision-making

> This is a **dynamical system layer**, not a logic layer.

---

### 6. Emitters

**Role:**
Exports internal state to external environment.

**Examples:**

* Cytokine secretion (IL2, IFN)
* Danger signals

**Mechanism:**

* Nodes marked as `io_role: emitter`
* Converted into external field signals

---

## Data Flow Separation

| Layer           | Reads            | Writes           |
| --------------- | ---------------- | ---------------- |
| Node Engine     | node_state       | node_state       |
| Passive Engine  | node_state       | node_state       |
| HIR             | node_state       | (no write)       |
| Behavior Engine | node_state       | behavior_outputs |
| State Update    | behavior_outputs | node_state       |
| Emitters        | node_state       | external_field   |

---

## Design Principles

### 1. Separation of Concerns

* Physics → Passive
* Physiology constraints → HIR
* Decision → Behavior
* Dynamics → StateUpdate

No layer should mix responsibilities.

---

### 2. Configuration-Driven

* Nodes, behaviors, passives, and HIR rules are defined in JSON
* Engine code remains generic

---

### 3. No Direct World Mutation

InternalNet:

* does NOT modify world state directly
* outputs must go through IntentBuilder → LabelCenter

---

### 4. Deterministic Core (by default)

* Deterministic activation supported
* Probabilistic modes optional (sigmoid)

---

### 5. Extensibility

New features can be added without modifying core engine:

* Add new node.json
* Add new behavior.json
* Add new passive.json
* Extend HIR config

---

## Minimal Example (Conceptual)

```
viral_load ↑
    → passive replication ↑
    → stress ↑
    → HIR: stressed

pMHC ↑
    → TCR_signal ↑ (via node graph)

TCR_signal + IL2_signal
    → behavior: release_perforin

release_perforin
    → target damage ↑
```

---

## Directory Structure

```
Internalnet/
├── node/              # node definitions
├── behavior/          # behavior definitions
├── passsive/          # passive processes
├── graph/             # node propagation graphs
├── HIR/               # HIR engine + config
├── state/             # state update logic
├── node_engine.py
├── passive_engine.py
├── behavior_engine.py
```

---

## Future Extensions

Planned or supported extensions:

* InputBuilder (external → node_input mapping)
* IntentBuilder integration (action → world)
* Multi-cell interaction scaling
* Per-cell high-fidelity simulation (ODE backend)

---

## Summary

InternalNet is a **multi-layer causal engine** that separates:

* signal processing,
* intrinsic dynamics,
* physiological constraints,
* and decision-making.

This separation enables:

* biological realism,
* modular extensibility,
* and stable large-scale simulation.

---

