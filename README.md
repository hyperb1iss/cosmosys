# Cosmosys: Cosmic Release Management 🌠

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-Apache%202.0-green.svg)](https://opensource.org/licenses/Apache-2.0)
[![Poetry](https://img.shields.io/badge/dependency%20management-poetry-blue)](https://python-poetry.org/)

Cosmosys is a flexible and customizable release management tool that brings the cosmic power of the stars to your software deployment process. 🚀

## ✨ Features

- 🌈 Multiple color schemes with easy customization
- 🎨 Customizable ASCII art logo
- 🔧 Modular release flow with pluggable steps
- 🖥️ Cross-platform compatibility
- 🏷️ Version management for various project types
- 🐙 Git integration
- 🔍 Customizable pre-release checks
- 📝 Release notes generation
- 📜 Changelog management
- 🔗 Integration with CI/CD systems
- 🧩 Plugin system for extending functionality
- 🏜️ Dry-run mode for testing release process
- ↩️ Rollback functionality
- 🌐 Multi-language support for messages and prompts

## 🛠️ Installation

Cosmosys can be easily installed using pip:

```bash
pip install cosmosys
```

Or, if you prefer to use Poetry:

```bash
poetry add cosmosys
```

## 🚀 Quick Start

1. Initialize a new Cosmosys configuration:

```bash
cosmosys init
```

2. Customize your `cosmosys.toml` configuration file.

3. Run the release process:

```bash
cosmosys release
```

## 🌌 Configuration

Cosmosys uses TOML for configuration. Here's a sample `cosmosys.toml`:

```toml
[project]
name = "YourAwesomeProject"
version = "0.1.0"

[release]
steps = ["version_update", "run_tests", "build", "publish"]

[color_scheme]
name = "neon"

[git]
main_branch = "main"
```

## 🎨 Color Schemes

Cosmosys comes with several predefined color schemes:

- `default`: A balanced, easy-on-the-eyes scheme
- `neon`: Bright and vibrant for those who like to live dangerously
- `monochrome`: For the minimalists out there

You can also define your own color schemes in the configuration file!

## 🛰️ Contributing

We welcome contributions to Cosmosys! Please check out our [Contributing Guide](CONTRIBUTING.md) for more information on how to get started.

## 📜 License

Cosmosys is released under the Apache License 2.0. See the [LICENSE](LICENSE) file for more details.

## 🌠 Acknowledgements

Cosmosys was inspired by the vastness of the cosmos and the desire to make software releases as smooth as the motion of celestial bodies. We thank all the stars in the open-source community for their guidance and inspiration.

---

<p align="center">
  Made with ❤️ by developers, for developers.<br>
  May your releases be as bright as the stars! ✨
</p>
```
