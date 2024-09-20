from abc import ABC, abstractmethod
from typing import Any, Dict

from starforge.config import StarForgeConfig


class Step(ABC):
    def __init__(self, config: StarForgeConfig):
        self.config = config

    @abstractmethod
    def execute(self) -> bool:
        """Execute the release step.

        Returns:
            bool: True if the step was successful, False otherwise.
        """
        pass

    @abstractmethod
    def rollback(self):
        """Rollback the changes made by this step."""
        pass

    def log(self, message: str):
        """Log a message during the release process."""
        # TODO: Implement proper logging
        print(f"[{self.__class__.__name__}] {message}")

class StepFactory:
    _steps: Dict[str, type] = {}

    @classmethod
    def register(cls, step_name: str):
        def decorator(step_class: type):
            cls._steps[step_name] = step_class
            return step_class
        return decorator

    @classmethod
    def create(cls, step_name: str, config: StarForgeConfig) -> Step:
        step_class = cls._steps.get(step_name)
        if not step_class:
            raise ValueError(f"Unknown release step: {step_name}")
        return step_class(config)

    @classmethod
    def get_available_steps(cls) -> Dict[str, type]:
        return cls._steps