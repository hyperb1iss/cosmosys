# Cosmosys Plugin Architecture 🧩

Cosmosys's plugin architecture allows you to extend and customize its functionality to fit your specific needs. Whether you want to add support for a new project type, integrate with a specific tool, or create a custom release step, plugins make it possible. This guide will walk you through using plugins, creating your own, and best practices for plugin development.

## Understanding Plugins 🤔

In Cosmosys, a plugin is a Python module that defines one or more custom release steps. Plugins can:

- ➕ Add new release steps
- 🔄 Modify existing steps
- 🔗 Integrate with external tools and services
- 🆕 Add support for new project types

## Using Plugins 🔌

### Installing Plugins 📥

Cosmosys plugins can be installed using pip:

```bash
pip install cosmosys-plugin-name
```

Replace `cosmosys-plugin-name` with the actual name of the plugin.

### Configuring Plugins ⚙️

To use a plugin, add it to the `steps` list in your `cosmosys.toml` file:

```toml
[release]
steps = [
    "version_update",
    "my_custom_plugin_step",
    "git_commit"
]
```

### Listing Installed Plugins 📋

To see all installed plugins:

```bash
cosmosys plugins --list
```

### Getting Plugin Information ℹ️

To get information about a specific plugin:

```bash
cosmosys plugins --info my_custom_plugin
```

## Creating Plugins 🛠️

### Plugin Structure 🏗️

A basic Cosmosys plugin structure looks like this:

```python
from cosmosys.steps.base import Step, StepFactory
from cosmosys.config import CosmosysConfig

@StepFactory.register("my_custom_step")
class MyCustomStep(Step):
    def __init__(self, config: CosmosysConfig):
        super().__init__(config)

    def execute(self) -> bool:
        self.log("Executing my custom step")
        # Your custom logic here
        return True

    def rollback(self) -> None:
        self.log("Rolling back my custom step")
        # Rollback logic if necessary
```

### Step-by-Step Guide to Creating a Plugin 📝

1. Create a new Python file for your plugin (e.g., `my_plugin.py`).
2. Import necessary modules from Cosmosys.
3. Define your custom step class, inheriting from `Step`.
4. Implement the `execute()` method with your custom logic.
5. Implement the `rollback()` method if your step needs rollback capabilities.
6. Use the `@StepFactory.register` decorator to register your step with Cosmosys.

### Plugin API 🔧

Cosmosys provides a rich API for plugin development:

- `self.config`: Access the Cosmosys configuration
- `self.log(message)`: Log messages during step execution
- `self.execute() -> bool`: Main method for step execution. Return `True` for success, `False` for failure.
- `self.rollback()`: Method to undo the step's actions if needed

### Accessing Project Information 📊

Plugins can access project information through the `self.config` object:

```python
project_name = self.config.project.name
project_version = self.config.project.version
```

### Interacting with Git 🐙

For Git operations, use the `git` module provided by Cosmosys:

```python
from cosmosys.utils import git

git.commit(self.config.git.files_to_commit, "Commit message")
git.tag(f"v{self.config.project.version}")
```

## Best Practices for Plugin Development 🌟

1. **Single Responsibility**: Each plugin should do one thing and do it well.
2. **Error Handling**: Implement robust error handling and provide informative error messages.
3. **Configuration**: Allow users to configure your plugin through the `cosmosys.toml` file.
4. **Documentation**: Provide clear documentation on how to use your plugin and its configuration options.
5. **Testing**: Write unit tests for your plugin to ensure reliability.
6. **Versioning**: Use semantic versioning for your plugin releases.

## Publishing Plugins 📢

To share your plugin with the Cosmosys community:

1. Package your plugin using setuptools.
2. Upload your plugin to PyPI.
3. Create a GitHub repository for your plugin source code.
4. Add a `README.md` file with usage instructions and examples.

## Plugin Security 🔒

When developing or using plugins, keep these security considerations in mind:

1. Only install plugins from trusted sources.
2. Review the plugin code before using it in your release process.
3. Be cautious with plugins that require sensitive information (e.g., API keys).

## Troubleshooting Plugins 🔍

If you encounter issues with a plugin:

1. Check the Cosmosys log for error messages.
2. Verify that the plugin is compatible with your version of Cosmosys.
3. Ensure that all plugin dependencies are installed.
4. Try running Cosmosys with the `--verbose` flag for more detailed output.

By leveraging the power of plugins, you can customize Cosmosys to fit perfectly into your development workflow. Happy coding! 🚀