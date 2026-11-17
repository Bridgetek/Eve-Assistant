# Bridgetek EVE Assistant

Bridgetek EVE Assistant combines EVE engineering guidance with local MCP tools for asset preparation, API and sample lookup, source review, and application planning. This repository contains the **0.9.16 desktop preview**.

The plugin runs on your development PC in a supported local ChatGPT/Codex environment. The three MCP adapters are bundled; you do **not** need to install their npm packages separately or run `npm install` in `plugin/` for normal use. EAB, EveApps repositories, compilers and the emulator are separate prerequisites.

## What runs where

| Component | Purpose | Local prerequisite |
| --- | --- | --- |
| EAB MCP (`eab`) | Asset-command lookup, conversion planning and approved EAB operations | Node.js; an installed EAB CLI for actual conversions |
| EveApps-Pre82X MCP (`pre82x`) | Earlier-generation EveApps API/sample lookup and source review | Node.js and a local [EveApps](https://github.com/Bridgetek/EveApps) checkout |
| EveApps-BT82X MCP (`bt82x`) | BT820/BT82X API/sample lookup and source review | Node.js and a local [EveApps-BT82X](https://github.com/Bridgetek/EveApps-BT82X) checkout |
| [Rust EAB CLI](https://github.com/Bridgetek/EAB-CLI) | Executes asset conversions | Separate complete distribution; documented for Windows 10/11 x64 |
| [EVE Emulator](https://github.com/Bridgetek/Eve-Emulator) | Runs an emulator application | Separate Windows binaries or Ubuntu 24.04 amd64 packages; current upstream examples target Windows |

Node.js **20.19+** is required by this kit; Node.js **22 LTS** is recommended. You also need Git and a supported host/client exposing local plugins. The commands below assume a current Codex CLI with `codex plugin marketplace` support. See [OpenAI's plugin setup documentation](https://developers.openai.com/plugins/build/plugins) for client availability and installation.

## Windows quick start

Use PowerShell on the same Windows PC where you will run the desktop host. The example directory is `C:\Bridgetek`; replace it if needed.

### 1. Check prerequisites

```powershell
node --version
git --version
codex --version
codex plugin marketplace --help
```

If a command is not found, install the corresponding prerequisite and reopen PowerShell. Also restart the desktop host after installing Node.js so it receives the updated PATH.

### 2. Download the plugin and the source repositories

```powershell
New-Item -ItemType Directory -Force C:\Bridgetek | Out-Null
Set-Location C:\Bridgetek

git clone https://github.com/Bridgetek/Eve-Assistant.git
git clone https://github.com/Bridgetek/EveApps.git
git clone https://github.com/Bridgetek/EveApps-BT82X.git
```

If you already have these repositories, keep using their actual locations instead of cloning duplicates. Each EveApps path must point to the repository root containing **both `common/` and `SampleApp/`**, not to a project or `Src` subdirectory. Use a checkout containing only material you authorize the AI host to inspect.

For asset conversions, obtain the full [Rust EAB CLI distribution](https://github.com/Bridgetek/EAB-CLI), for example by cloning the distribution repository:

```powershell
git clone https://github.com/Bridgetek/EAB-CLI.git C:\Bridgetek\EAB-CLI
```

Check that the distribution contains real executable/dependency files, not an incomplete download. Keep these items together:

```text
C:\Bridgetek\EAB-CLI\
  eab_tools.exe
  exts\
  dependencies\
```

You do not need a Rust compiler to use its prebuilt executable. Check the installed CLI without converting an asset:

```powershell
& 'C:\Bridgetek\EAB-CLI\eab_tools.exe' --version
& 'C:\Bridgetek\EAB-CLI\eab_tools.exe' list-tools
```

See the [Rust EAB setup guide](docs/rust-eab-cli.md) for command syntax and dependency checks. The Rust CLI uses explicit chip/family names such as `bt817` or `bt82x`; do not use the older `82x`/`pre82x` prefixes with it.

### 3. Configure your EAB and EveApps paths

Run the configuration wizard from this repository's `plugin` directory:

```powershell
Set-Location C:\Bridgetek\Eve-Assistant\plugin
node scripts/configure.mjs
```

Enter your actual local paths at the prompts. For the example layout above:

| Prompt, in order | Example answer |
| --- | --- |
| `EAB CLI edition: rust, legacy or auto` | `rust` |
| `EveApps repository` | `C:\Bridgetek\EveApps` |
| `EveApps-BT82X repository` | `C:\Bridgetek\EveApps-BT82X` |
| `EAB executable` | `C:\Bridgetek\EAB-CLI\eab_tools.exe` |

At the wizard prompts, enter the path itself **without surrounding quotation marks**, even if it contains spaces. Quotes are needed around paths in shell commands, not in these interactive answers.

- Select **`rust`** for the new EAB CLI. It selects the bundled EAB 4.6 command specification and checks for `exts/` and `dependencies/` beside the executable.
- Select **`legacy`** only for an older installed CLI that actually supports the legacy command syntax.
- Select **`auto`** to let the MCP adapter detect the installed executable's CLI flavor. Existing path-only configurations retain this behavior.
- For a fresh configuration, leaving an unavailable component blank lets you configure it later. An EveApps server without its required path will refuse to start. EAB catalog/query tools can be used without an EAB executable, but actual conversion cannot.
- On subsequent runs, pressing Enter **keeps the saved value**; it does not clear it. To remove a saved setting, edit the JSON file described below.

The wizard only saves local paths and edition settings. It does not clone repositories, install EAB or register the plugin in your host.

### 4. Register the local plugin marketplace

From the **repository root**, which contains `.agents/plugins/marketplace.json`:

```powershell
Set-Location C:\Bridgetek\Eve-Assistant
codex plugin marketplace add .
codex plugin marketplace list
```

Restart the supported ChatGPT desktop app, open its Plugins Directory, select **Bridgetek EVE Desktop Preview**, and install/enable **Bridgetek EVE Assistant**. Use it in a thread that runs locally on this PC. The exact UI and availability depend on your client and organization settings.

The marketplace ID is `bridgetek-eve-desktop-preview`; its plugin directory is `./plugin`. Do not register `plugin/` itself as the marketplace root, and do not edit files in the host's generated plugin cache.

If you prefer a Git-backed marketplace, you can register the public repository instead of the local checkout:

```powershell
codex plugin marketplace add Bridgetek/Eve-Assistant
```

Choose one registration route. The per-user configuration created in step 3 works for the installed plugin copy too, provided the host runs as the same OS user in the same environment.

### 5. Verify and start using it

From the plugin directory, run the bundled read-only verifier with the same repository paths:

```powershell
Set-Location C:\Bridgetek\Eve-Assistant\plugin
node scripts/verify.mjs --pre82x 'C:\Bridgetek\EveApps' --bt82x 'C:\Bridgetek\EveApps-BT82X'
```

The verifier checks the MCP integrations and synthetic path-boundary cases. It does not execute EAB conversions, compile an application or test hardware. Windows may report symlink tests as blocked if the OS does not permit creating symlinks.

In your local AI host, confirm the `eab`, `pre82x` and `bt82x` servers are connected. The bundled versions expose **47 tools** in total (30 + 9 + 8). Several tool names occur on both EveApps servers, so identify the target chip in your prompt.

Try these first:

- **Earlier-generation EveApps:** “I use BT817. Identify the graphics chip in ME817EV and find an appropriate touch-widget sample in my local EveApps checkout.”
- **BT82X EveApps:** “I use BT820. Explain CMD_BUTTON and show a relevant sample from my EveApps-BT82X checkout.”
- **EAB:** “Which EAB command converts a PNG to RGB565 for BT817? Show the required options; do not execute it.”

For an actual conversion, provide the input, chip, format and output location, review the prepared operation, then approve it through the applicable workflow. A returned scaffold, command suggestion or code check is not evidence that a build, emulator run or hardware test passed.

## Where configuration is saved

The same user-specific file is used by all installed copies of this plugin:

- **Windows:** `%USERPROFILE%\.config\bridgetek-eve-assistant\config.json`
- **Linux:** `~/.config/bridgetek-eve-assistant/config.json`

The launcher uses Node.js `os.homedir()` to resolve the home directory. It does not use the repository's working directory or the Windows AppData directory for this file.

Example Windows configuration:

```json
{
  "eabCliFlavor": "rust",
  "pre82xRepo": "C:\\Bridgetek\\EveApps",
  "bt82xRepo": "C:\\Bridgetek\\EveApps-BT82X",
  "eabToolsPath": "C:\\Bridgetek\\EAB-CLI\\eab_tools.exe"
}
```

JSON requires doubled backslashes, or you can use forward slashes such as `C:/Bridgetek/EveApps`. The configuration values must be actual absolute paths; strings such as `$HOME` or `%USERPROFILE%` inside JSON are not expanded by the launcher.

To inspect or edit the default file in PowerShell:

```powershell
Get-Content (Join-Path $HOME '.config\bridgetek-eve-assistant\config.json')
notepad (Join-Path $HOME '.config\bridgetek-eve-assistant\config.json')
```

After moving EAB or a repository, rerun `node scripts/configure.mjs` or edit this file, then restart/reconnect the plugin's MCP servers. Do not commit personal machine paths, credentials or customer repositories to this repository.

### Environment overrides

Use these only when you need a different configuration for a host or project:

| Variable | Effect |
| --- | --- |
| `EVE_ASSISTANT_CONFIG` | Use a different JSON configuration file; specify an absolute path. Applies to both the wizard and launcher. |
| `EVEAPPS_PRE82X_ROOT` | Overrides `pre82xRepo`. |
| `EVEAPPS_BT82X_ROOT` | Overrides `bt82xRepo`. |
| `EAB_TOOLS_PATH` | Overrides `eabToolsPath`. |
| `EVE_EAB_CLI_FLAVOR` | Overrides `eabCliFlavor`; use `rust`, `legacy` or `auto`. |
| `EAB_MCP_SPEC` | Explicit EAB command-spec override. Takes precedence over edition-based selection; a stale legacy spec can cause incorrect Rust commands. |

For example, set a custom configuration location **before** running the wizard:

```powershell
$env:EVE_ASSISTANT_CONFIG = 'C:\Bridgetek\eve-assistant-config.json'
node C:\Bridgetek\Eve-Assistant\plugin\scripts\configure.mjs
```

A variable assigned with `$env:` is available to that PowerShell session and its child processes. A separately launched desktop app does not automatically inherit it. The plugin host must receive the same override; otherwise use the default shared per-user configuration file. No environment variables are required for the normal wizard-based setup.

## Ubuntu and WSL

Use paths and installed programs belonging to the environment that actually runs the MCP processes:

- For a **Windows desktop host**, use Windows Node.js and Windows paths in the Windows user's config file.
- For a host running **inside WSL/Linux**, use Linux Node.js, Linux paths and that Linux user's config file. For example, a Windows checkout may be visible under `/mnt/c/Bridgetek/EveApps`, but `C:\Bridgetek\EveApps` is not a Linux absolute path.
- Do not assume Windows and WSL share the same home directory, PATH, environment variables or plugin installation.

The EveApps adapters support local source workflows in a Linux environment. The documented Rust EAB CLI distribution is Windows-only; this kit does not provide a verified native Ubuntu EAB conversion setup. The emulator has separate **Ubuntu 24.04 amd64** packages. See [EVE Emulator setup](docs/eve-emulator-setup.md); the upstream examples currently target Windows and are not automatically portable to Ubuntu.

## Troubleshooting

| Symptom | What to check |
| --- | --- |
| `node`, `git` or `codex` is not recognized | Install the prerequisite, reopen the terminal and restart the desktop host. Check the host's own PATH. |
| The CLI does not recognize `plugin marketplace` | Update to a client with local-plugin marketplace support; check the official setup documentation linked above. |
| Plugin does not appear | Register the repository root, retain the hidden `.agents` directory, restart the desktop app and check organization/local-plugin policies. |
| “An absolute repository path is required” | Run the wizard under the same OS user/environment as the host, or check its `EVE_ASSISTANT_CONFIG`/repository environment overrides. |
| Missing `common` or `SampleApp` | Select the repository root, not a subfolder. Check that the checkout is complete. |
| Rust EAB requires `exts/` and `dependencies/` | Obtain the full distribution and select the executable beside both directories. |
| Settings look correct but the host uses another path | Check the environment override table, the host OS user and whether the host runs in Windows or WSL. Reconnect MCP servers after changes. |
| Old `82x`/`pre82x` syntax appears for Rust EAB | Select `rust`, remove an unintended `EAB_MCP_SPEC` override and inspect the installed CLI's help/version. |
| A server started manually appears to wait | MCP uses stdio and waits for client messages. Use the host connection or `scripts/verify.mjs`; do not type chat prompts into the server process. |
| An emulator does not start | Install the matching separate emulator runtime and consult its OS-specific guide; the bundled adapters do not supply an emulator-launch tool. |

## Updating your local copy

For a local-checkout marketplace, pull changes in the checkout and refresh/reinstall the plugin using your host's supported flow, then restart the desktop app. For a Git-backed marketplace, use:

```powershell
codex plugin marketplace upgrade bridgetek-eve-desktop-preview
```

Recheck the installed version after updating. Keep the per-user configuration outside the checkout and cache; do not overwrite it when replacing a plugin ZIP.

## Distribution and verification status

This repository provides a GitHub/local-marketplace desktop preview. That is separate from publication in the official OpenAI public directory. Customers need a compatible host/account and remain subject to its availability, permissions and usage limits.

The recorded automated checks and remaining end-to-end verification work are detailed below. Neither the Windows EAB executable nor either platform's emulator was executed as part of preparing this README.

<details>
<summary>Maintainer notes: recorded verification, directory submission, release details and rebuilding</summary>

## Verification actually completed

The unchanged MCP runtime has 31 automated checks recorded as passed on Linux / Node.js 24.22.1 using real official repository checkouts during version 0.9.15 verification. This 0.9.16 update changes emulator guidance and metadata; it does not change the MCP launch/runtime code. Runtime bytes are compared with 0.9.15 instead of repeating the same protocol tests. See docs/verification.json. Checks cover 3 server startups, 47 tools and boolean annotations, 15 representative functional tool calls, 4 traversal/symlink rejection tests and failure on missing repository configuration. Eight additional checks cover Rust/legacy/auto specification selection, custom overrides, invalid editions, full Rust distribution layout and live MCP catalog chip tokens. The 0.9.15 release ZIP was extracted and protocol-tested to detect packaging/path problems. This update validates the new archive structure, guide links and unchanged runtime bytes. It does not imply that the external emulator was executed.

EveApps commit: 2e54debc089db20bdbcffc578da3c4a8bb122629
EveApps-BT82X commit: 6b5a57eb55e6729a80980655a0b6b7ab2e89a16f

Not verified: installation in the user's Windows ChatGPT desktop host; Windows EAB execution and approval UI; compiler/emulator/hardware behavior; host prompt routing of the proposed reviewer cases; a real recorded demo. A protocol test is not an end-to-end host review test.

## Public publication requirements still outstanding

1. OpenAI currently restricts local-MCP submissions to approved partners. Request local-MCP allowlisting for the submitting organization from your OpenAI representative. A draft request is in docs/openai-eligibility-request.txt. No message has been sent.
2. Update the three published company pages for the actual desktop behavior. Proposed HTML content is in docs/website-updates/. These are company-review drafts, not published policies. The privacy accessibility warning observed in the portal also needs investigation by the website administrator; loading in one browser does not prove crawler access.
3. Install and rehearse this exact candidate in a local host. Execute each server's five positive and three negative review prompts in mcp.json, recording actual host tool calls and outcomes. All 24 host-level review cases are currently Not run. No credentials are needed for the read-only sample workflows; installation/update functions may separately require authorized repository access.
4. Record the real host demonstration described in docs/demo-walkthrough.md, host it at a reviewer-accessible URL, verify playback, and add the actual recording URL to extensions.com.openai.review.demo_recording_url. A script is not a video.
5. After allowlisting and material completion, create the supported new local-MCP submission containing the servers in its initial upload. Do not try to attach them to the existing skills-only portal draft: the current documentation says that conversion is unsupported. Preserve the old draft and source. Confirm exact verified publisher identity, countries, policy URLs and server/skill findings in the new saved submission.
6. The authorized developer completes legal/policy attestations. Submit for review only after blocking findings and required checks are resolved. Publish is a separate action after approval. No eligibility or approval is guaranteed by adding MCP.

Official references:
https://developers.openai.com/plugins/deploy/desktop-only
https://developers.openai.com/plugins/deploy/submission
https://developers.openai.com/plugins/build/plugins

## EVE Emulator update

The official distribution at https://github.com/Bridgetek/Eve-Emulator provides Windows binaries and Ubuntu 24.04 amd64 runtime/development packages. The inspected release is 5.3.37 and the public native API is 20. See docs/eve-emulator-setup.md for Windows linking/sample builds and the documented Ubuntu package-install commands. The included upstream examples currently target Windows; Linux integration requires suitable native application code. Emulator libraries are obtained separately, and no fourth MCP server or emulator-launch tool is added. Ubuntu emulator support does not establish Ubuntu support for the Windows Rust EAB CLI. Neither OS emulator was executed for this update.

## Rust CLI update

The kit now links the Rust EAB distribution, documents its Windows runtime and complete folder layout, supports explicit rust/legacy/auto selection, and uses chip names/families such as bt817 and bt82x instead of the rejected legacy 82x/pre82x prefixes. The documented Rust default is BT82X when no chip is specified; the assistant must specify the intended chip explicitly. Commands for --version, list-tools and dependency inspection are provided for local verification. Actual Windows Rust CLI execution remains unverified here; no EAB binaries or distribution payloads are added to the ZIP.

## Engineering changes in this integration

The npm packages are pinned with integrity hashes in source/runtime/package-lock.json. The two EveApps servers were bundled with their SDK/runtime dependencies and data indexes. Integration patches add read-only/non-destructive/closed-world annotations to their tools, skip symlinks in source search and enforce real-path containment in the BT82X file reader. EAB tool listings receive annotations: command preparation changes in-memory request state; execution can overwrite files/program hardware and is conservatively destructive; installation, remote checks, sampling and execution can interact beyond the static index. Existing EAB preview/approval behavior is retained. EAB upstream docs may recommend automatic installation; the EVE skill requires explicit authorization first.

The plugin does not provide a security sandbox. EAB is a local development tool and can access selected files and hardware. The host's tool permissions and user approvals still matter. Query text, paths, snippets and tool results returned to the AI host can be processed by that host; local execution does not mean all information stays outside the conversation.

## Rebuild

The distributable plugin is in plugin/. The inner Bridgetek_EVE_Assistant_0.9.16_Desktop_DRAFT.zip is the plugin-only archive for a future eligible portal upload; do NOT upload this whole kit.

Rebuild prerequisites: Node.js, npm and Python 3. From source/runtime run `npm ci --ignore-scripts`; from source/ run `node authoring/build.mjs`, then `python authoring/finalize.py`. The build uses source/base-plugin as its preserved seed. Package only source/plugin/. Do not include node_modules, test checkouts or user configuration. License notices are retained. Use the verifier on the resulting copy before deployment.

</details>
