# demo/scenario/base_scenario.py

"""
=========================================================
Base Scenario
=========================================================

Abstract scenario definition for MacroImmunet Demo.

Responsibilities
----------------
- describe simulation setup
- provide MiniSIO requests
- expose scenario metadata

DOES NOT
--------
- build SimulationWorld
- execute simulation
- access LabelCenter
- perform biological reasoning
"""

from abc import ABC, abstractmethod


class BaseScenario(ABC):

    """
    Base class of all demo scenarios.

    Runtime

        Scenario
            ↓
        MiniSIO Requests
            ↓
        SimulationBuilder
    """

    def __init__(self):

        self.name = self.__class__.__name__

    # =====================================================
    # Required
    # =====================================================

    @abstractmethod
    def build(self):
        """
        Return a list of MiniSIO-compatible requests.

        Returns
        -------
        list[dict]
            Raw MiniSIO requests.
        """
        raise NotImplementedError

    # =====================================================
    # Optional
    # =====================================================

    def metadata(self):

        """
        Optional scenario metadata.
        """

        return {

            "name": self.name

        }

    def runtime_options(self):

        """
        Optional runtime configuration.

        Can be overridden by subclasses.
        """

        return {}

    # =====================================================
    # Helpers
    # =====================================================

    def __repr__(self):

        return (

            f"<Scenario {self.name}>"

        )
