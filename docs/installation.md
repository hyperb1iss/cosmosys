# Installation Guide 🛠️

Getting Cosmosys up and running on your system is a straightforward process. This guide will walk you through the installation steps for various platforms and package managers.

## Prerequisites 📋

Before installing Cosmosys, ensure that you have the following:

- Python 3.9 or higher 🐍
- pip (Python package installer) or Poetry (dependency management tool) 📦

You can check your Python version by running:

```bash
python --version
```

## Installation Methods 🔧

### Using pip 🐍

Pip is the standard package manager for Python. To install Cosmosys using pip:

1. Open your terminal or command prompt.
2. Run the following command:

   ```bash
   pip install cosmosys
   ```

3. Verify the installation by checking the version:

   ```bash
   cosmosys --version
   ```

### Using Poetry 📜

Poetry is a modern dependency management tool for Python. To install Cosmosys using Poetry:

1. If you haven't installed Poetry yet, follow the [official Poetry installation guide](https://python-poetry.org/docs/#installation).
2. Once Poetry is installed, run:

   ```bash
   poetry add cosmosys
   ```

3. Activate your Poetry shell:

   ```bash
   poetry shell
   ```

4. Verify the installation:

   ```bash
   cosmosys --version
   ```

## Platform-Specific Instructions 💻

### Windows 🪟

1. Ensure Python is in your PATH.
2. Open Command Prompt or PowerShell.
3. Follow the pip or Poetry installation method above.

### macOS 🍎

1. We recommend using [Homebrew](https://brew.sh/) to manage Python:
   
   ```bash
   brew install python
   ```

2. Then follow the pip or Poetry installation method.

### Linux 🐧

Most Linux distributions come with Python pre-installed. If not:

1. Use your distribution's package manager to install Python. For example, on Ubuntu:
   
   ```bash
   sudo apt-get update
   sudo apt-get install python3 python3-pip
   ```

2. Then follow the pip or Poetry installation method.

## Installing from Source 📦

For the latest development version:

1. Clone the Cosmosys repository:

   ```bash
   git clone https://github.com/hyperb1iss/cosmosys.git
   ```

2. Navigate to the cloned directory:

   ```bash
   cd cosmosys
   ```

3. Install using pip:

   ```bash
   pip install .
   ```

   Or using Poetry:

   ```bash
   poetry install
   ```

## Troubleshooting 🔍

If you encounter any issues during installation:

- Ensure your Python version is 3.9 or higher.
- Check that pip or Poetry is up to date.
- If you get a "Permission denied" error, try using `sudo` (on Unix-based systems) or run your command prompt as Administrator (on Windows).
- If you're behind a proxy, configure pip to use it:
  
  ```bash
  pip install --proxy [your-proxy] cosmosys
  ```

For more help, consult our [support page](support.md) or open an issue on our [GitHub repository](https://github.com/hyperb1iss/cosmosys/issues).

## Next Steps 🚀

Now that you have Cosmosys installed, head over to our [Quick Start Guide](quickstart.md) to begin your cosmic journey in release management!