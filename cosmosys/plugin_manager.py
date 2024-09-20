import importlib
import os
from typing import Dict, Type

from cosmosys.config import CosmosysConfig
from cosmosys.steps.base import Step, StepFactory


class PluginManager:
    def __init__(self, config: CosmosysConfig):
        self.config = config
        self.plugins: Dict[str, Type[Step]] = {}

    def load_plugins(self):
        plugin_dir = self.config.get('plugins.directory', 'plugins')
        if not os.path.exists(plugin_dir):
            return

        for filename in os.listdir(plugin_dir):
            if filename.endswith('.py') and not filename.startswith('__'):
                plugin_name = filename[:-3]
                module = importlib.import_module(f'{plugin_dir}.{plugin_name}')
                for attr_name in dir(module):
                    attr = getattr(module, attr_name)
                    if isinstance(attr, type) and issubclass(attr, Step) and attr != Step:
                        self.plugins[plugin_name] = attr
                        StepFactory.register(plugin_name)(attr)

    def get_plugin(self, name: str) -> Type[Step]:
        return self.plugins.get(name)