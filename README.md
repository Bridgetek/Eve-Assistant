# Bridgetek EVE Assistant — Desktop integration candidate 0.9.16

Prepared 13 November 2026. Status: integrated and protocol-tested; NOT submission-ready, submitted, approved or publicly published. The original workspace plugin and portal 0.9.13 draft have not been changed.

## What is included

- Both original skills, technical references and icon, with desktop setup/routing added.
- Three bundled local MCP servers: EAB 0.0.14 (30 tools), EveApps-BT82X 1.2.0 (8 tools), EveApps-Pre82X 1.1.0 (9 tools). The deprecated bt820-mcp-server is not used.
- Portable mcp.json plus Codex compatibility manifest/configuration. Runtime dependencies are bundled; server startup does not run npm or download packages. Node.js is still required.
- Per-user repository/EAB configuration, source-boundary checks, tool annotations, 5 positive/3 negative proposed reviewer cases for each server, automated verification evidence, rebuild source and license notices.

## Start using the candidate locally

1. Extract this complete kit to a permanent directory. Install Node.js 20.19+ (Node.js 22 LTS recommended) from the official Node.js distribution if it is not installed.
2. Obtain local official repository checkouts appropriate to your target. EveApps: https://github.com/Bridgetek/EveApps ; BT82X: https://github.com/Bridgetek/EveApps-BT82X . Each selected checkout must contain common and SampleApp. Configure a dedicated checkout containing only project material you authorize the assistant to inspect. BT819 device support must be checked explicitly.
3. For actual asset conversions, obtain the Rust EVE Asset Builder CLI distribution from https://github.com/Bridgetek/EAB-CLI and keep eab_tools.exe, exts/ and dependencies/ together. The documented package runs on Windows 10/11 x64 and does not require a Rust compiler. See docs/rust-eab-cli.md for verified syntax and setup. Select the rust edition in the configuration wizard; legacy and auto remain available for older installations. EAB executable, MCU SDKs, compilers, emulator binaries, hardware drivers and repositories are not included. EAB query/catalog tools can be tested without EAB installed. This package does not download or install EAB automatically.
4. From the kit's plugin directory run `node scripts/configure.mjs`. Choose rust, legacy or auto, then enter absolute repository paths and, where installed, the path to eab_tools.exe. Rust mode validates the full adjacent distribution layout and selects the bundled EAB 4.6 specification. New setups prefer Rust; old path-only configurations retain auto-detection. Leave unavailable components blank and configure them later. A repository server will intentionally refuse to start until its path is configured.
5. From the KIT ROOT (the directory containing README.md and .agents), register the local marketplace: `codex plugin marketplace add .` . This changes your local marketplace configuration; run it only on your intended development computer. Restart the ChatGPT desktop app, find Bridgetek EVE Assistant under the Bridgetek EVE Desktop Preview marketplace and install/enable it for a local thread. The exact install surface depends on your client version. This local marketplace registration is NOT public directory publication. Do not expect these local processes to run in a cloud thread.
6. Confirm the host shows all three MCP connections and 47 tools. Start with: 'For BT817, identify the graphics chip in ME817EV'; 'For BT820, explain CMD_BUTTON using my local checkout'; 'Which EAB command converts a PNG to RGB565? Do not execute it.' Several tools share names between servers: inspect the server qualification.
7. Run the bundled verifier from plugin/: `node scripts/verify.mjs --pre82x "C:\Projects\EveApps" --bt82x "C:\Projects\EveApps-BT82X"` . It performs read-only MCP checks and synthetic path-boundary tests. It does not compile or program hardware. On Windows, symlink tests may be reported Blocked if OS permissions prohibit creating symlinks.

Per-user config defaults to ~/.config/bridgetek-eve-assistant/config.json. Environment overrides: EVE_ASSISTANT_CONFIG, EVEAPPS_PRE82X_ROOT, EVEAPPS_BT82X_ROOT, EAB_TOOLS_PATH, EVE_EAB_CLI_FLAVOR. An explicit EAB_MCP_SPEC overrides edition-based spec selection. Do not include this local config, credentials or customer repositories in a public upload. The launcher forces EAB stdio, even if an HTTP transport environment setting exists. It does not expose a public server.

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
