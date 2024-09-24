"""Plugin management system for Cosmosys."""

import importlib
import os
from typing import Dict, Optional, Type

from cosmosys.context import CosmosysContext
from cosmosys.steps.base import Step, StepFactory


class PluginManager:
    """Manages the loading and retrieval of plugins for Cosmosys."""

    def __init__(self, context: CosmosysContext) -> None:
        """
        Initialize a PluginManager instance.

        Args:
            context (CosmosysContext): The context object for Cosmosys.
        """
        self.context = context
        self.config = context.config
        self.plugins: Dict[str, Type[Step]] = {}

    def load_plugins(self) -> None:
        """
        Load plugins from the specified plugin directory.

        This method searches for Python files in the plugin directory,
        imports them, and registers any Step subclasses as plugins.
        """
        plugin_dir = self.config.get("plugins.directory", "plugins")
        if not os.path.exists(plugin_dir):
            return

        for filename in os.listdir(plugin_dir):
            if filename.endswith(".py") and not filename.startswith("__"):
                plugin_name = filename[:-3]
                module = importlib.import_module(f"{plugin_dir}.{plugin_name}")
                for attr_name in dir(module):
                    attr = getattr(module, attr_name)
                    if isinstance(attr, type) and issubclass(attr, Step) and attr != Step:
                        self.plugins[plugin_name] = attr
                        StepFactory.register(plugin_name)(attr)

    def get_plugin(self, name: str) -> Optional[Type[Step]]:
        """
        Retrieve a plugin by name.

        Args:
            name (str): The name of the plugin to retrieve.

        Returns:
            Optional[Type[Step]]: The plugin class if found, None otherwise.
        """
        return self.plugins.get(name)

    def get_plugin_info(self, name: str) -> Optional[str]:
        """
        Get information about a plugin.

        Args:
            name (str): The name of the plugin.

        Returns:
            Optional[str]: Description of the plugin if available.
        """
        plugin = self.get_plugin(name)
        if plugin and plugin.__doc__:
            return plugin.__doc__
        return None

    def get_available_plugins(self) -> Dict[str, str]:
        """
        Get a list of available plugins and their descriptions.

        Returns:
            Dict[str, str]: A dictionary of plugin names and descriptions.
        """
        return {
            name: (cls.__doc__ or "No description available") for name, cls in self.plugins.items()
        }
