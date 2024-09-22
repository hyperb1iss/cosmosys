# Cosmosys Theming System

Cosmosys offers a robust theming system that allows you to customize the look and feel of your CLI experience. Whether you prefer a sleek, professional appearance or a vibrant, eye-catching display, Cosmosys has you covered. This guide will walk you through using built-in themes, creating custom themes, and applying themes to your Cosmosys setup.

## Understanding Themes

A Cosmosys theme defines colors for different elements of the CLI output:

- `primary`: Main color for important elements
- `secondary`: Color for less prominent elements
- `success`: Color for success messages
- `error`: Color for error messages
- `warning`: Color for warning messages
- `info`: Color for informational messages

Themes also include emoji definitions for various message types, adding a touch of personality to your CLI interactions.

## Built-in Themes

Cosmosys comes with several pre-defined themes:

1. **default**: A balanced, easy-on-the-eyes color scheme
2. **neon**: Bright and vibrant colors for a futuristic feel
3. **pastel**: Soft, soothing colors for a gentle look
4. **monochrome**: A simple black and white theme for minimalists

### Viewing Available Themes

To see all available themes:

```bash
cosmosys theme --list
```

### Previewing Themes

To preview a theme:

```bash
cosmosys theme --preview neon
```

This command will display sample output using the specified theme.

### Setting a Theme

To set a theme, update your `cosmosys.toml` file:

```toml
[theme]
name = "neon"
```

Alternatively, use the CLI:

```bash
cosmosys theme --set neon
```

## Creating Custom Themes

Cosmosys allows you to create your own themes to match your project's branding or personal preferences.

### Custom Theme Structure

Custom themes are defined in the `cosmosys.toml` file under the `[custom_themes]` section. Here's an example:

```toml
[custom_themes.my_awesome_theme]
name = "My Awesome Theme"
description = "A custom theme with awesome colors"
primary = "#FF6B6B"
secondary = "#4ECDC4"
success = "#45B7D1"
error = "#EC4E20"
warning = "#FF9F1C"
info = "#6B48FF"
emojis = { success = "🚀", error = "💥", warning = "⚠️", info = "💡" }
```

### Color Specification

Colors are specified using hexadecimal color codes (#RRGGBB). You can use any valid hex color code.

### Emoji Customization

You can customize emojis for different message types. Make sure to use emojis that are widely supported for the best compatibility across different systems.

### Applying Custom Themes

To use your custom theme, set it in the `[theme]` section of your `cosmosys.toml`:

```toml
[theme]
name = "my_awesome_theme"
```

## Theme Best Practices

1. **Contrast**: Ensure good contrast between text and background colors for readability.
2. **Consistency**: Keep your color choices consistent with your project's branding.
3. **Accessibility**: Consider color-blind friendly palettes for better accessibility.
4. **Testing**: Test your themes in different terminal environments to ensure compatibility.

## Troubleshooting Themes

If you encounter issues with themes:

1. Ensure your terminal supports 256 colors for the best experience.
2. Check that your custom theme definition includes all required colors.
3. Verify that your `cosmosys.toml` file is correctly formatted.

## Theme Sharing

Consider sharing your custom themes with the Cosmosys community! You can:

1. Create a GitHub repository for your theme.
2. Share your theme configuration in the Cosmosys community forums.
3. Submit a pull request to include your theme in the Cosmosys built-in themes.
