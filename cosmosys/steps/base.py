"""Base classes and utilities for Cosmosys release steps."""

from abc import ABC, abstractmethod
from typing import Callable, Dict, Type

from cosmosys.config import CosmosysConfig


class Step(ABC):
    """Abstract base class for release steps."""

    def __init__(self, config: CosmosysConfig) -> None:
        """
        Initialize a Step instance.

        Args:
            config (CosmosysConfig): The Cosmosys configuration.
        """
        self.config = config

    @abstractmethod
    def execute(self) -> bool:
        """
        Execute the release step.

        Returns:
            bool: True if the step was successful, False otherwise.
        """
        pass

    @abstractmethod
    def rollback(self) -> None:
        """Rollback the changes made by this step."""
        pass

    def log(self, message: str) -> None:
        """
        Log a message during the release process.

        Args:
            message (str): The message to log.
        """
        # TODO: Implement proper logging
        print(f"[{self.__class__.__name__}] {message}")


class StepFactory:
    """Factory class for creating and managing release steps."""

    _steps: Dict[str, Type[Step]] = {}

    @classmethod
    def register(cls, step_name: str) -> Callable[[Type[Step]], Type[Step]]:
        """
        Decorator for registering a step class.

        Args:
            step_name (str): The name of the step.

        Returns:
            Callable: A decorator function.
        """

        def decorator(step_class: Type[Step]) -> Type[Step]:
            cls._steps[step_name] = step_class
            return step_class

        return decorator

    @classmethod
    def create(cls, step_name: str, config: CosmosysConfig) -> Step:
        """
        Create a step instance by name.

        Args:
            step_name (str): The name of the step to create.
            config (CosmosysConfig): The Cosmosys configuration.

        Returns:
            Step: An instance of the requested step.

        Raises:
            ValueError: If the step name is unknown.
        """
        step_class = cls._steps.get(step_name)
        if not step_class:
            raise ValueError(f"Unknown release step: {step_name}")
        return step_class(config)

    @classmethod
    def get_available_steps(cls) -> Dict[str, Type[Step]]:
        """
        Get all available steps.

        Returns:
            Dict[str, Type[Step]]: A dictionary of step names and their corresponding classes.
        """
        return cls._steps.copy()
