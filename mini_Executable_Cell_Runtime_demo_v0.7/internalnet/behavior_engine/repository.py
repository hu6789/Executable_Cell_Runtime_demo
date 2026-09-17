# internalnet/behavior_engine/repository.py

class BehaviorRepository:
    """Repository for static BehaviorDefinition objects."""

    def __init__(self, behaviors=None):
        self._behaviors = {}

        if behaviors is not None:
            for behavior in behaviors:
                self.register(behavior)

    def register(self, behavior):
        if behavior.name in self._behaviors:
            raise ValueError(
                f"Behavior already registered: {behavior.name}"
            )

        self._behaviors[behavior.name] = behavior

    def get(self, name):
        try:
            return self._behaviors[name]
        except KeyError:
            raise KeyError(f"Unknown behavior: {name}") from None

    def has(self, name):
        return name in self._behaviors

    def names(self):
        return tuple(self._behaviors.keys())
