# @bridgetek/eab-mcp-server

**Bridgetek Eve Asset Builder (EAB) MCP server** — a Model Context Protocol (MCP) server that lets AI agents drive **Bridgetek EAB Tools** (`eab_tools.exe`) to convert, compress, validate and program EVE graphics assets (images, fonts, audio, video, GIF animations, raw pixel buffers, SPI flash images).

It exposes typed per-command tools (`eab_*`), a natural-language assistant (the mandatory `eab` routing tool), Server Instructions, resources, prompt templates, workflows and sampling — all backed by a **mandatory user-confirmation flow** before any `eab_tools.exe` command runs. The package is fully self-contained (the `@modelcontextprotocol/sdk` is bundled) and has **no runtime dependencies**.

This is one of three distributions of the same server — also available as a **VS Code extension (VSIX)** and to **run from source code** (see `https://github.com/BridgetekChip/EAB-CLI-MCP-Server`).

## Quick Start

1. **Install** the package (two ways):

   ```bash
   # global — launches directly as a command
   npm install -g @bridgetek/eab-mcp-server
   # Test it
   eab-mcp-server --help  

   # local — runs via npx
   npm install @bridgetek/eab-mcp-server
   # Test it
   npx @bridgetek/eab-mcp-server --help  
   ```

2. **Register** it in your MCP client using one of the entries under [MCP Client configuration](#mcp-client-configuration-full-list).

3. **Ask your agent**, e.g. in Copilot Chat:

   - *"List the available EAB tools."*
   - *"Convert image.png to RGB565 for BT82X."*
   - *"Build a font from my TTF file."*
   - *"Program this flash image onto the SPI flash."*

**Requirements:** Node.js 18+ and Bridgetek EAB installed (https://brtchip.com/eab/). The server auto-discovers `eab_tools.exe` under `C:\Users\Public\Documents\EVE Asset Builder\<version>\tools\eab_tools.exe`; set `EAB_TOOLS_PATH` to override.

**No EAB installed?** Ask the agent to install it: `check_eab_installation` reports the local state, and `install_eab_cli` downloads EAB from [Bridgetek/EAB-CLI](https://github.com/Bridgetek/EAB-CLI) into `%LOCALAPPDATA%\EAB-CLI` (call it with `confirm: true` after approving). That repository is private, so set `EAB_GITHUB_TOKEN` (or `GITHUB_TOKEN` / `GH_TOKEN`, or run `gh auth login`) so the download can authenticate.

**EAB version support:** the package ships two specs and picks the one matching your installed CLI — `EAB_mcp_data_for_EAB4.6.0.json` for EAB 4.6+ (chip tokens `bt82x` / `bt81x` / `bt88x` / `ft81x` / `ft80x`) and `EAB_mcp_data.json` for EAB ≤ 4.5 (chip groups `82x` / `pre82x`). Override with `EAB_MCP_SPEC` or `--spec`.

## Usage Examples

> Typed `eab_*` tools **never run the CLI directly** — they return a preview + `requestId`. Execution requires an explicit final confirmation via `execute_eab_tool_call` with `confirm: true`.

- **Find the right command** — call `eab` (or `ask_eab`) with `query = "convert an image to RGB565"`; it returns `img_cvt` as the best match, with required flags and an example invocation.
- **Convert an image** — call `eab_img_cvt` with `{ "input": "assets/logo.png", "output_dir": "./out", "format": "RGB565", "chip_gen": "bt82x" }` → get a `requestId`; adjust options with `update_eab_tool_call` if needed; then `execute_eab_tool_call` with `{ "requestId": "...", "confirm": true }`.
- **Build a font** — `eab_font` with the TTF/OTF path and an output folder.
- **Program SPI flash** — `eab_flash_gen` / `eab_flash_prog` (always gated behind confirmation — never auto-run).
- **Compress assets** — `eab_compress` (zlib / zopfli) — a shared command with no `chip_gen`.
- **Explain a command** — `explain_eab_command` with `command = "img_cvt"` returns the chip, every option and an example invocation.

## MCP Client configuration (full list)

The server is an MCP **stdio** server by default (run `eab-mcp-server --help` for flags: `--transport`, `--port`, `--host`, `--spec`).

**Universal config** for `mcpServers`-style clients (VS Code, Cursor, Cline, …):

```json
{
  "mcpServers": {
    "eab_tools": {
      "type": "stdio",
      "command": "npx",
      "args": ["@bridgetek/eab-mcp-server"]
    }
  }
}
```

If you installed **globally**, you can launch the bin directly:

```json
{
  "mcpServers": {
    "eab_tools": {
      "type": "stdio",
      "command": "@bridgetek/eab-mcp-server"
    }
  }
}
```

| Client | Configure |
|---|---|
| **VS Code / Copilot** | Paste the universal config into `mcp.json` / MCP settings (or install the [VS Code extension](https://github.com/BridgetekChip/EAB-CLI-MCP-Server) instead — it auto-registers). |
| **Claude Code** | `claude mcp add eab_tools --scope user -- npx @bridgetek/eab-mcp-server` |
| **Cursor** | Settings → MCP → Add server → universal config |
| **Cline** | MCP settings → universal config |
| **Codex** | `codex mcp add eab_tools -- npx @bridgetek/eab-mcp-server` |
| **Copilot CLI** | `/mcp add` → Local, command `npx`, args `["@bridgetek/eab-mcp-server"]` |
| **Gemini CLI** | `gemini mcp add eab_tools npx @bridgetek/eab-mcp-server` |
| **Gemini Code Assist** | MCP settings → universal config |
| **Windsurf** | MCP configuration → universal config |
| **Amp** | `amp mcp add eab_tools -- npx @bridgetek/eab-mcp-server` |
| **Antigravity** | Custom local MCP server → universal config |
| **Command Code** | `cmd mcp add eab_tools --scope user -- npx @bridgetek/eab-mcp-server` |
| **Factory CLI** | `droid mcp add eab_tools "npx @bridgetek/eab-mcp-server"` |
| **JetBrains AI / Junie** | Settings → MCP → local server → universal config |
| **Kiro** | MCP configuration → universal config |
| **Mistral Vibe** | `~/.vibe/config.toml`: `command = "npx"`, `args = ["@bridgetek/eab-mcp-server"]` |
| **OpenCode** | `mcp` config → `type: "local"`, universal config |
| **Qoder / Qoder CLI** | `qodercli mcp add eab_tools -- npx @bridgetek/eab-mcp-server` |
| **Visual Studio** | MCP settings → local server → universal config |
| **Warp** | AI → Manage MCP Servers → universal config |
| **Katalon Studio** | Via an MCP proxy / HTTP endpoint |

Optional per-client env: `EAB_TOOLS_PATH` (absolute path to `eab_tools.exe`), `EAB_MCP_SPEC` (alternative spec file), `EAB_CLI_INSTALL_DIR` (where `install_eab_cli` unpacks EAB, default `%LOCALAPPDATA%\EAB-CLI`) and `EAB_GITHUB_TOKEN` (token for the private `Bridgetek/EAB-CLI` repository).

## License

MIT
