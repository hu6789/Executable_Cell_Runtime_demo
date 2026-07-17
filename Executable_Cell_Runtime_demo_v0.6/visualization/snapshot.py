# visualization/snapshot.py

"""
=========================================================
Visualization Snapshot
=========================================================

Visualization Contract for MacroImmunet v0.6

Purpose
-------
Provide immutable visualization data for Viewer.

Viewer should NEVER access runtime objects directly.

Pipeline

Runtime
    ↓
Recorder
    ↓
Visualization Snapshot
    ↓
Viewer
"""

from copy import deepcopy


# =========================================================
# Visualization Snapshot
# =========================================================

def build_snapshot(
    world,
    inspectors=None,
    events=None,
    metadata=None
):
    """
    Root visualization snapshot.

    Viewer only consumes this object.
    """

    return {

        "world":
            deepcopy(world),

        "inspectors":
            deepcopy(inspectors or {}),

        "events":
            deepcopy(events or []),

        "metadata":
            deepcopy(metadata or {})
    }


# =========================================================
# World Snapshot
# =========================================================

def build_world_snapshot(
    tick,
    width,
    height,
    cells=None,
    particles=None,
    fields=None
):
    """
    Data consumed by WorldRenderer.
    """

    return {

        "tick":
            tick,

        "width":
            width,

        "height":
            height,

        "cells":
            deepcopy(cells or []),

        "particles":
            deepcopy(particles or []),

        "fields":
            deepcopy(fields or [])
    }


# =========================================================
# Cell Snapshot
# =========================================================

def build_cell_snapshot(
    cell_id,
    cell_type,
    position,
    alive=True
):
    """
    Lightweight world cell.

    Renderer only needs these.
    """

    return {

        "id":
            cell_id,

        "type":
            cell_type,

        "position":
            tuple(position),

        "alive":
            alive
    }


# =========================================================
# Particle Snapshot
# =========================================================

def build_particle_snapshot(
    particle_id,
    particle_type,
    position,
    strength=None
):

    return {

        "id":
            particle_id,

        "type":
            particle_type,

        "position":
            tuple(position),

        "strength":
            strength
    }


# =========================================================
# Field Snapshot
# =========================================================

def build_field_snapshot(
    field_type,
    values
):
    """
    values:

        {

            (0,0):100,

            (0,1):80,

            ...

        }
    """

    return {

        "type":
            field_type,

        "values":
            deepcopy(values)
    }


# =========================================================
# Inspector Snapshot
# =========================================================

def build_inspector_snapshot(
    cell_id,
    cell_type,
    nodes=None,
    behaviors=None
):
    """
    Data consumed by Sidebar.
    """

    return {

        "cell_id":
            cell_id,

        "cell_type":
            cell_type,

        "nodes":
            deepcopy(nodes or []),

        "behaviors":
            deepcopy(behaviors or [])
    }


# =========================================================
# Node Snapshot
# =========================================================

def build_node_snapshot(
    name,
    value
):
    """
    Example

        ATP

        86
    """

    return {

        "name":
            name,

        "value":
            value
    }


# =========================================================
# Behavior Snapshot
# =========================================================

def build_behavior_snapshot(
    name,
    strength=None
):
    """
    Example

        Translation

        ATP Production
    """

    return {

        "name":
            name,

        "strength":
            strength
    }


# =========================================================
# Event Snapshot
# =========================================================

def build_event_snapshot(
    tick,
    message,
    level="info"
):
    """
    Human-readable event.

    Example

        Tick 12

        Host released CXCL10
    """

    return {

        "tick":
            tick,

        "message":
            message,

        "level":
            level
    }


# =========================================================
# Metadata Snapshot
# =========================================================

def build_metadata_snapshot(
    scenario=None,
    title=None,
    description=None
):

    return {

        "scenario":
            scenario,

        "title":
            title,

        "description":
            description
    }
