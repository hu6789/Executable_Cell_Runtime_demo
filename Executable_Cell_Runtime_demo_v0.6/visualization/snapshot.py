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
# Root Snapshot
# =========================================================

def build_snapshot(
    tick,
    world,
    inspectors,
    events,
    metadata
):

    return {

         "tick": 
            tick,
        
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
    alive=True,
    color=None
):

    """
    Lightweight cell representation.

    Used by:
        - WorldRenderer
        - Cell selector

    """

    return {

        "id":
            cell_id,

        "type":
            cell_type,

        "position":
            tuple(position),

        "alive":
            alive,

        "color":
            color
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
    values,
    max_value=None,
    sources=None
):

    """
    Continuous field layer.

    Example:

        IL2 field

        {
            (0,0):10,
            (1,0):20
        }


    Renderer uses values
    to generate transparency / gradient.
    """

    return {

        "type":
            field_type,

        "values":
            deepcopy(values),

        "max_value":
            max_value,

        "sources":
            deepcopy(sources or [])
    }



# =========================================================
# Inspector Snapshot
# =========================================================

def build_inspector_snapshot(
    object_type,
    object_id,
    **kwargs
):

    """
    Generic detail panel data.

    Supports:

        cell

        field

    Example:

        {
            type:"cell",
            id:"cd4_1",
            nodes:[],
            behaviors:[]
        }

    """

    snapshot = {

        "type":
            object_type,

        "id":
            object_id
    }


    snapshot.update(

        deepcopy(kwargs)

    )

    return snapshot



# =========================================================
# Node Snapshot
# =========================================================

def build_node_snapshot(
    name,
    value
):

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
    category=None,
    level="info",
    event_type=None,
    source=None,
    target=None
):

    """
    Human readable biological event.

    Examples:

        CD4_1 TCR binds pMHC

        CD8_1 releases perforin

    """

    return {

        "tick":
            tick,
            
        "category":
            category,

        "type":
            event_type,

        "source":
            source,

        "target":
            target,

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
