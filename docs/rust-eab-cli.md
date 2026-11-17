# Rust EVE Asset Builder CLI

The Rust-based EVE Asset Builder CLI distribution is available from
https://github.com/Bridgetek/EAB-CLI . This is the executable tool distribution;
`@bridgetek/eab-mcp-server` is the separate Node.js MCP adapter that drives it.
The plugin bundles the adapter, not the EAB executable distribution. Running
the ready-built package does not require a Rust compiler.

## Verified source and installation

Guidance checked against the repository README on 13 November 2026, at commit
`edd47d23439e762596181d37d5addbc639462edb` (README blob
`030a22d9703ea9bbf9d6fe1d739666d7897c5379`). The documented runtime is
Windows 10/11 x64. The README estimates about 260 MB for the full distribution.
WebView2 is required for GUI mode. This does not establish Linux/macOS binary
support. A newer checkout can change the interface; inspect its own help.

Obtain the complete distribution from that official repository through your
authorized GitHub access. Keep this layout together:

```text
EAB-CLI/
  eab_tools.exe
  exts/
  dependencies/
```

Do not copy only the executable: converters and third-party payloads are in
the adjacent directories. Use the distribution's own acquisition instructions;
no release-asset name or download URL is assumed here. The kit neither embeds
the roughly 260 MB tool distribution nor auto-downloads it at startup.

On your Windows computer, run the non-conversion checks from that directory:

```powershell
.\eab_tools.exe --version
.\eab_tools.exe --help
.\eab_tools.exe list-tools
.\eab_tools.exe bt817 img_cvt --help
.\eab_tools.exe deps list
.\eab_tools.exe deps verify
```

These commands are user-run checks, not results already demonstrated by this
kit. `deps install`, `deps update`, `deps unlink` and `deps prune` change the
installation or dependency store; do not run them as routine inspection.

## Configure the plugin

Run `node scripts/configure.mjs` and choose `rust`. Point the EAB executable
setting at the actual `eab_tools.exe` in the full distribution. The launcher
checks for the adjacent `exts/` and `dependencies/` directories and explicitly
selects the bundled `EAB_mcp_data_for_EAB4.6.0.json` command specification.
This prevents an unconfigured fresh session from defaulting to the old
`82x`/`pre82x` command catalog. The launcher uses MCP stdio, not the EAB GUI.

Example per-user configuration (replace paths with real installations):

```json
{
  "eabCliFlavor": "rust",
  "eabToolsPath": "C:\\Bridgetek\\EAB-CLI\\eab_tools.exe",
  "pre82xRepo": "C:\\Projects\\EveApps",
  "bt82xRepo": "C:\\Projects\\EveApps-BT82X"
}
```

The configuration wizard writes outside the package to
`~/.config/bridgetek-eve-assistant/config.json`. Restart MCP connections after
changing it. `EVE_EAB_CLI_FLAVOR` overrides the saved edition; allowed values
are `rust`, `legacy` and `auto`. `EAB_TOOLS_PATH` overrides the saved executable.
An explicit `EAB_MCP_SPEC` overrides specification selection, so remove a stale
override when switching editions. The wizard defaults to Rust for new setups;
existing path-only configurations retain `auto` compatibility. Select `legacy`
only for an installed older CLI that actually accepts its legacy tokens.

## Chip names and command syntax

The Rust distribution accepts chip families `ft80x`, `ft81x`, `bt88x`, `bt81x`
and `bt82x`, and documented part names including `ft800`, `ft813`, `bt815`,
`bt817`, `bt880` and `bt820`. Its README says the omitted-chip default is BT82X.
Always specify the actual chip/family in generated commands rather than rely
on that default. Do not copy defaults from an old proposal or another release.
The legacy `legacy`, `82x` and `pre82x` group tokens are not accepted.

Examples from the current README, shown as templates rather than executed
conversions:

```powershell
.\eab_tools.exe bt82x img_cvt -i input.png -o .\out -f RGB8
.\eab_tools.exe ft80x img_cvt -i input.png -o .\out -f RGB565
.\eab_tools.exe bt817 img_cvt --help
```

Check chip-specific format support and live options with `--help` and
`list-tools`. A catalog describes the bundled MCP adapter version, not every
future executable. For a command absent from the adapter catalog, inspect the
installed CLI's help and explain the missing adapter coverage instead of
inventing a typed MCP tool. BT819 applicability still requires device-specific
documentation and actual CLI support checks; no new BT819 part alias is
declared by this guide.

The repository includes dependency-store commands, converters, flash tools,
GUI mode and additional utilities. Not all standalone utilities have a typed
MCP wrapper in adapter 0.0.14. Do not claim they are connected just because the
CLI supports them.

## Execution and verification boundaries

Read queries, catalog lookup and command planning can be used before an EAB
installation exists. Actual conversions require the installed distribution.
Prepare the exact input, chip, options and output path, inspect the preview,
then obtain the required user approval before execution. Flash programming,
firmware operations, installation changes and dependency updates need their
appropriate explicit authorization. Preserve the existing EAB confirmation
workflow and separate emulator/hardware verification gates.

This update tests command-spec selection, configuration and distribution layout
validation with synthetic fixtures, plus real MCP catalog queries. The Windows
Rust executable, converter outputs, GUI and connected hardware have not been
executed in this Linux environment. A successful adapter query does not prove
a real conversion, build or hardware operation passed.
