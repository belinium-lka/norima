File Type & Language Icons for Norima

This extension ships a minimal icon theme that maps `.norm` files to the Norima logo SVG.

How to enable (VS Code):

1. Open the Extension Development Host (or install this extension).
2. Open Command Palette -> `Preferences: File Icon Theme` -> choose `Norima Icons`.
3. In Explorer, `.norm` files will show the Norima icon.

Notes:
- The icon provided is an SVG at `vscode-extension/icons/norima.svg`.
- The icon theme maps the extension `norm` to the `norima` icon via `icons/icon-theme.json`.

OS MIME / System file association (recommended steps):

Linux (desktop):
- Copy `tools/file-associations/norima-mime.xml` to `~/.local/share/mime/packages/` and run `update-mime-database ~/.local/share/mime`.
- Place `norima.svg` into an icon folder or update the desktop icon cache to reference it.

macOS / Windows:
- Installers should register the `.nor` extension and provide an appropriate icon asset during packaging (electron-builder, pkg, or native installer).

JetBrains IDEs:
- JetBrains requires a plugin to register a file type and icon. Place the `norima.svg` in the plugin and declare a `fileType` entry mapping `.norm` to the Norima file type.
