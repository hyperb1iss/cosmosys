# Cosmosys: Stellar Release Management 🌠

[![Python Version](https://img.shields.io/badge/python-3.9%2B-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-Apache%202.0-green.svg)](https://opensource.org/licenses/Apache-2.0)
[![Poetry](https://img.shields.io/badge/dependency%20management-poetry-blue)](https://python-poetry.org/)
[![Documentation Status](https://readthedocs.org/projects/cosmosys/badge/?version=latest)](https://cosmosys.readthedocs.io/en/latest/?badge=latest)

Cosmosys is a flexible and customizable release management tool that brings the cosmic power of the stars to your software deployment process. Whether you're managing a small project or a complex multi-language ecosystem, Cosmosys provides the tools you need to make your releases smooth, consistent, and enjoyable.

## 🚀 What is Cosmosys?

Cosmosys is designed to simplify and streamline the software release process. It provides a unified interface for managing releases across different project types, including Python, Rust, and Node.js. With its modular architecture and plugin system, Cosmosys can be easily extended to support additional languages and custom workflows.

### Key Features

- 🌈 **Multiple Color Schemes**: Customize your CLI experience with built-in and custom color themes.
- 🎨 **ASCII Art Logo**: Add a touch of personality to your release process with customizable ASCII art.
- 🔧 **Modular Release Flow**: Configure your release steps to match your project's needs.
- 🖥️ **Cross-Platform Compatibility**: Works seamlessly on Windows, macOS, and Linux.
- 🏷️ **Version Management**: Automatically handle version bumping and tagging.
- 🐙 **Git Integration**: Commit changes, create tags, and push to remote repositories.
- 🔍 **Customizable Pre-Release Checks**: Ensure your project is ready for release with configurable checks.
- 📝 **Release Notes Generation**: Automatically generate and manage release notes.
- 📜 **Changelog Management**: Keep your changelog up-to-date with each release.
- 🔗 **CI/CD Integration**: Easily integrate with popular CI/CD platforms.
- 🧩 **Plugin System**: Extend functionality with custom plugins.
- 🏜️ **Dry-Run Mode**: Test your release process without making any changes.
- ↩️ **Rollback Functionality**: Safely undo changes if something goes wrong.
- 🌐 **Multi-Language Support**: Manage releases for projects in different programming languages.

## 🛠️ Installation

Cosmosys requires Python 3.9 or higher. You can install it using pip:

```bash
pip install cosmosys
```

Or if you prefer using Poetry:

```bash
poetry add cosmosys
```

## 🚀 Quick Start

1. Initialize a new Cosmosys configuration:

   ```bash
   cosmosys config --init
   ```

2. This creates a `cosmosys.toml` file. Customize it to fit your project:

   ```toml
   [project]
   name = "YourAwesomeProject"
   version = "0.1.0"
   
   [release]
   steps = ["version_update", "changelog_update", "git_commit", "git_tag"]
   
   [theme]
   name = "neon"
   
   [git]
   main_branch = "main"
   ```

3. Run your first release:

   ```bash
   cosmosys release
   ```

## 📚 Usage

Cosmosys provides a rich set of commands to manage your release process:

- **Release**: `cosmosys release [OPTIONS]`
  - Options include `--dry-run`, `--verbose`, `--interactive`, `--new-version`, and `--part [major|minor|patch]`
- **Configuration**: `cosmosys config [OPTIONS]`
  - Manage your Cosmosys configuration
- **Themes**: `cosmosys theme [OPTIONS]`
  - List, set, or preview themes
- **Plugins**: `cosmosys plugins [OPTIONS]`
  - List and manage plugins

For detailed usage instructions, refer to our [comprehensive documentation](https://cosmosys.readthedocs.io).

## 🎨 Theming

Cosmosys supports multiple color schemes to make your CLI experience more enjoyable. Choose from built-in themes or create your own:

```bash
# List available themes
cosmosys theme --list

# Set a theme
cosmosys theme --set neon

# Preview a theme
cosmosys theme --preview pastel
```

## 🧩 Plugins

Extend Cosmosys functionality with plugins. Create custom release steps, integrations, or add support for new project types.

```bash
# List installed plugins
cosmosys plugins --list

# Get info about a specific plugin
cosmosys plugins --info my_awesome_plugin
```

Check out our [Plugin Development Guide](https://cosmosys.readthedocs.io/en/latest/plugins/developing/) to create your own plugins.

## 🤝 Contributing

We welcome contributions to Cosmosys! Whether it's bug reports, feature requests, or code contributions, please check out our [Contributing Guide](CONTRIBUTING.md) for more information on how to get started.

## 📜 License

Cosmosys is released under the Apache License 2.0. See the [LICENSE](LICENSE) file for more details.

## 🌟 Acknowledgements

Cosmosys was inspired by the vastness of the cosmos and the desire to make software releases as smooth as the motion of celestial bodies. We thank all the stars in the open-source community for their guidance and inspiration.

---

<div align="center">

Created by [Stefanie Jane 🌠](https://github.com/hyperb1iss)

If you find this project useful, [buy me a Monster Ultra Violet!](https://ko-fi.com/hyperb1iss)! ⚡️

</div>