# Bridgetek MCP server guidance

Verified against official Bridgetek pages on 2026-10-27. Recheck installation details and available tools when using a different release.

## Server selection

| Task / target | Server | Required local software or source |
| --- | --- | --- |
| EVE asset preparation | EAB MCP Server | EVE Asset Builder |
| BT820 / BT82X application development | BT820 MCP Server, also called EveApps-BT82X MCP Server | [EveApps-BT82X](https://github.com/Bridgetek/EveApps-BT82X/) |
| BT817/BT818 and earlier EVE application development | EveApps-Pre82X MCP Server | [EveApps](https://github.com/Bridgetek/EveApps/) |

Identify the exact IC before routing. Verify repository support for other part numbers rather than inferring it from a family nickname.

## EAB MCP Server

Use EAB for image conversion, fonts from TTF/OTF, compression, audio, supported video/GIF, raw graphics buffers, SPI flash images, asset validation and approved programming. Supported output formats and targets depend on the installed EAB version.

The npm route requires Node.js 18 or later, EVE Asset Builder and an MCP-compatible client. Official commands:

```text
npm install -g @bridgetek/eab-mcp-server
npx @bridgetek/eab-mcp-server
```

The VS Code route installs the Bridgetek EAB MCP Server extension. Run `EAB MCP Server: Input eab_tools.exe`, select the EAB installation and reload VS Code.

Keep the existing emulator-first workflow's EAB approval rules: present actual input, exact command, options and output path before each asset operation. Privileged EAB commands require explicit confirmation. Do not infer executable paths or run a conversion merely from these examples.

Sources: [EAB documentation](https://brtchip.com/eab-mcp-server/), [requested EAB link](https://brtchip.com/#EABMCP).

## BT820 / EveApps-BT82X MCP Server

This server uses a local EveApps-BT82X checkout for sample discovery, command/register/symbol explanations, feature tracing, screen scaffolding, code checks and build guidance. Install or download the repository and configure its actual local path.

```text
npm install -g @bridgetek/bt820-mcp-server
bt820-mcp-server --eveapps <local-EveApps-BT82X-path>
```

Node.js 18 or later is recommended for npm installation. Alternatively install the Bridgetek BT820 MCP Server VS Code extension and select the EveApps-BT82X workspace path.

Apply this skill's strict BT82x access policy to generated code. Source-backed validation does not establish that a build, emulator run or hardware test passed.

Sources: [BT820 documentation](https://brtchip.com/bt820-mcp-server/), [requested BT820 link](https://brtchip.com/#BT820MCP).

## EveApps-Pre82X MCP Server

Use this server with a local EveApps checkout for BT817/BT818 and earlier devices. It supports sample discovery, symbols, source navigation, feature tracing, scaffolding, code checks and configuration-aware build commands.

```text
npm install -g @bridgetek/eveapps-pre82x-mcp-server
eveapps-pre82x-mcp-server --eveapps <local-EveApps-path>
```

Node.js 18 or later is recommended for npm installation. The VS Code alternative is the Bridgetek EveApps-Pre82X MCP Server extension, configured to the local EveApps workspace.

Check the selected checkout's actual device and platform support; earlier-family support does not establish BT82x compatibility.

Sources: [Pre82X documentation](https://brtchip.com/Pre82X-mcp-server/), [requested Pre82X link](https://brtchip.com/#Pre82XMCP).

## Applying the guidance

These are installation examples, not commands to execute automatically. Replace placeholder paths and use the client's documented configuration format. The website links are documentation, not remote MCP endpoint URLs.

Discover the current session's tools and inspect their schemas before calling them. Tool names can vary by release or host; never fabricate a tool call. If connected, use the applicable engineering assistant, sample and symbol lookup, source reading, build guidance and validation tools as exposed. Confirm platform, graphics, display and SPI choices before generating build commands.

When a server is unavailable, explain the missing connection or local prerequisite and consult official source files for guidance. Do not report that a server ran, a repository was indexed, or an operation passed without evidence. A knowledge reference does not install, enable or connect an MCP server.

Combine approved EAB asset work with the generation-appropriate EveApps server. Preserve emulator Gate A and physical hardware Gate B as separate evidence requirements in [the emulator-first workflow](emulator-first-workflow.md).

The official [toolchain overview](https://brtchip.com/toolchains/) corroborates the repository split. Some dedicated pages contain inconsistent generic text about chip support or EAB; use the explicit repository/target descriptions and verify technical applicability against the configured source.
