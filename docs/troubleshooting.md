# Troubleshooting and FAQs 🔧🤔

This guide aims to help you resolve common issues you might encounter while using Cosmosys and answer frequently asked questions. If you don't find a solution to your problem here, please don't hesitate to reach out to our community support channels or open an issue on our GitHub repository.

## Troubleshooting 🛠️

### Installation Issues 📦

#### Q: I'm getting a "Command not found" error when trying to run Cosmosys.

A: Ensure that Cosmosys is properly installed and that your PATH is set correctly. Try the following:

1. Reinstall Cosmosys: `pip install --upgrade cosmosys`
2. Check if the installation directory is in your PATH.
3. Try using the full path to the Cosmosys executable.

#### Q: I'm facing dependency conflicts when installing Cosmosys.

A: Try creating a virtual environment for Cosmosys:

```bash
python -m venv cosmosys_env
source cosmosys_env/bin/activate  # On Windows, use `cosmosys_env\Scripts\activate`
pip install cosmosys
```

### Configuration Issues ⚙️

#### Q: Cosmosys is not recognizing my configuration file.

A: Ensure that:

1. Your configuration file is named `cosmosys.toml` and is in the root directory of your project.
2. The file is properly formatted TOML. You can use a TOML validator to check.
3. You're running Cosmosys from the correct directory.

#### Q: I'm getting a "KeyError" when Cosmosys tries to read my configuration.

A: This usually means a required configuration key is missing. Check the error message for the specific key and ensure it's present in your `cosmosys.toml` file.

### Release Process Issues 🚀

#### Q: The version update step is failing.

A: Common causes include:

1. Incorrect version format in your project files.
2. Lack of write permissions for the files containing version information.
3. Misconfiguration of the version update step in `cosmosys.toml`.

Try running with the `--verbose` flag for more detailed error information.

#### Q: Git operations are failing during the release process.

A: Ensure that:

1. You have the necessary permissions for the Git repository.
2. Your Git configuration (user.name and user.email) is set correctly.
3. You're not trying to push to a protected branch without the proper permissions.

#### Q: The changelog update step is not working as expected.

A: Check that:

1. Your Git commit messages follow the expected format for changelog generation.
2. The `CHANGELOG.md` file exists and is writable.
3. Your changelog configuration in `cosmosys.toml` is correct.

### Plugin Issues 🔌

#### Q: My custom plugin is not being recognized by Cosmosys.

A: Verify that:

1. The plugin file is in the correct directory (as specified in your `cosmosys.toml`).
2. The plugin class is decorated with `@StepFactory.register("step_name")`.
3. The plugin file is a valid Python module (ends with `.py` and contains no syntax errors).

## Frequently Asked Questions 🤔

### General Questions ❓

#### Q: What is Cosmosys?

A: Cosmosys is a flexible and customizable release management tool designed to streamline the software release process. It supports various project types, offers customizable release steps, and provides features like theming and plugin support.

#### Q: Which programming languages does Cosmosys support?

A: Out of the box, Cosmosys supports Python, Rust, and Node.js projects. However, its plugin system allows for easy extension to support other languages and project types.

#### Q: Can I use Cosmosys with my existing CI/CD pipeline?

A: Yes, Cosmosys is designed to integrate smoothly with various CI/CD systems. Check our [CI/CD Integration guide] for detailed information.

### Configuration and Customization 🛠️

#### Q: How do I customize the release steps?

A: You can customize release steps by modifying the `steps` list in the `[release]` section of your `cosmosys.toml` file. You can also create custom steps using plugins.

#### Q: Can I use environment variables in my Cosmosys configuration?

A: Yes, you can use environment variables in your `cosmosys.toml` file using the syntax `${ENV_VAR_NAME}`.

#### Q: How do I create a custom theme?

A: Custom themes can be defined in the `[custom_themes]` section of your `cosmosys.toml` file. See our [Theming guide](theming.md) for more details.

### Features and Functionality 🚀

#### Q: Does Cosmosys support semantic versioning?

A: Yes, Cosmosys supports semantic versioning out of the box. You can specify which part of the version to bump (major, minor, patch) during the release process.

#### Q: Can Cosmosys automatically generate release notes?

A: Yes, Cosmosys can generate release notes based on your Git commit history. This feature is customizable through the changelog configuration in `cosmosys.toml`.

#### Q: Is it possible to roll back a release if something goes wrong?

A: Yes, Cosmosys includes rollback functionality for its release steps. If a step fails, Cosmosys will attempt to roll back the changes made by previous steps.

### Best Practices 🌟

#### Q: Should I commit my `cosmosys.toml` file to version control?

A: Yes, it's generally a good practice to commit your `cosmosys.toml` file to version control. This ensures that all team members and your CI/CD pipeline use the same configuration.

#### Q: How often should I run Cosmosys releases?

A: The frequency of releases depends on your project and team preferences. Some teams prefer frequent, small releases, while others opt for less frequent, larger releases. Cosmosys supports both approaches.

#### Q: How can I ensure the security of my release process with Cosmosys?

A: To enhance security:
1. Use environment variables for sensitive information.
2. Implement proper access controls for your repository and release environments.
3. Regularly update Cosmosys and its dependencies.
4. Consider implementing release signing as part of your release process.
