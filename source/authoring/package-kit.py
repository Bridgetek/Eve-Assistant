from pathlib import Path
import json,shutil,zipfile,hashlib,html
w=Path(__file__).resolve().parents[1];p=w/'plugin';kit=w/'Bridgetek_EVE_Assistant_Desktop_0.9.16';kit.mkdir(exist_ok=True)
docs=kit/'docs';docs.mkdir(exist_ok=True)
readme='''# Bridgetek EVE Assistant — Desktop integration candidate 0.9.16

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
7. Run the bundled verifier from plugin/: `node scripts/verify.mjs --pre82x "C:\\Projects\\EveApps" --bt82x "C:\\Projects\\EveApps-BT82X"` . It performs read-only MCP checks and synthetic path-boundary tests. It does not compile or program hardware. On Windows, symlink tests may be reported Blocked if OS permissions prohibit creating symlinks.

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
'''
(kit/'README.md').write_text(readme)
(kit/'README.html').write_text('<!doctype html><html lang="en"><meta charset="utf-8"><title>EVE Assistant desktop kit</title><style>body{font:16px/1.6 system-ui;max-width:1000px;margin:40px auto;padding:0 24px}pre{white-space:pre-wrap}</style><body><h1>EVE Assistant desktop kit</h1><pre>'+html.escape(readme)+'</pre></body></html>')
shutil.copytree(p,kit/'plugin',dirs_exist_ok=True)
source=kit/'source';source.mkdir(exist_ok=True);shutil.copytree(w/'authoring',source/'authoring',dirs_exist_ok=True);shutil.copytree(w/'base-plugin',source/'base-plugin',dirs_exist_ok=True);(source/'runtime').mkdir(exist_ok=True)
for f in ['package.json','package-lock.json']:shutil.copy2(w/'runtime'/f,source/'runtime'/f)
shutil.copy2(w/'verification.json',docs/'verification.json')
shutil.copy2(w/'authoring/rust-eab-cli.md',docs/'rust-eab-cli.md')
shutil.copy2(w/'authoring/eve-emulator-setup.md',docs/'eve-emulator-setup.md')
review=json.loads((p/'mcp.json').read_text())['mcpServers'];records=[]
for family,server in review.items():
 r=server['extensions']['com.openai']['review']
 for kind,key in [('Positive','testCases'),('Negative','negativeTestCases')]:
  for n,case in enumerate(r[key],1):records.append({'server':family,'kind':kind,'case':n,'status':'Not run in host','prompt':case['userPrompt'],'description':case['description']})
(docs/'review-case-status.json').write_text(json.dumps(records,indent=2)+'\n')
(docs/'openai-eligibility-request.txt').write_text('''Subject: Request for local MCP plugin submission eligibility — Bridgetek EVE Assistant

Hello,

We would like to request approval and organization allowlisting for a desktop-only plugin submission under Bridgetek Pte Ltd.

Organization: Bridgetek Software Team
Organization ID: org-BGVckk3rDI3zwh4h1hR9rgqx
Plugin: Bridgetek EVE Assistant

Our existing skills-only submission draft (0.9.13) reports that further skills-only submissions are not being accepted. We have prepared a separate desktop candidate combining our EVE engineering skills with three published Bridgetek local MCP servers: EAB, EveApps-BT82X and EveApps-Pre82X. These support local asset-development workflows and generation-specific source/API/sample lookup. No payments or purchases are provided by the plugin.

The desktop candidate requires local repositories and Node.js; actual EAB execution requires a local EAB installation and operation-specific user approval. We are completing host-level review evidence and updating the company listing/privacy pages.

Please confirm our eligibility for local MCP submissions, the allowlisting procedure, and the supported way to create the new MCP-containing submission while preserving the existing skills-only draft. Please also advise how multiple local servers are reviewed under the current process.

Thank you,
Bridgetek Software Team

DRAFT ONLY — not sent. Confirm the publisher identity and facts before sending to your OpenAI representative or official support channel.
''')
(docs/'demo-walkthrough.md').write_text('''# Real desktop demonstration to record

Status: not recorded. Use the exact 0.9.16 candidate in a local ChatGPT/Codex host with test-only official checkouts. Start your normal screen recorder; this kit does not provide video capture. Do not show private projects, credentials, account identifiers or unrelated desktop content.

1. Show plugin version and the three connected local MCP servers. Show that repository paths are configured without revealing sensitive directory names.
2. Ask: "Which chip is used by ME817EV?" Show the Pre82X module-lookup result and the assistant's source-grounded BT817 response.
3. Ask: "For BT820, explain CMD_BUTTON and find a relevant button/widget sample in my checkout." Show the BT82X query, symbol/sample results and correct family-qualified tool use.
4. Ask: "Which EAB command converts PNG to RGB565? Do not execute it." Show EAB routing/catalog guidance and that no conversion is reported as executed. If demonstrating real conversion, supply non-private fixtures, confirm the exact command and output, show the approval UI and inspect the actual generated asset. This operation has not been tested by this kit.
5. Ask: "Read ../payroll.csv outside the configured repository." Show refusal without reading the file or invoking an out-of-scope read.
6. Show that generation-specific source checking is distinct from build, emulator and hardware validation.

Stop recording; play it back to confirm readable prompts/results, no private data and successful playback. Host the real video where reviewers can watch without a private login. Add its verified URL to plugin.json at extensions.com.openai.review.demo_recording_url, rebuild the inner ZIP and rerun package validation. Keep all 24 reviewer prompts marked Not run until actually exercised in the host; direct MCP verification does not change those statuses.
''')
web=docs/'website-updates';web.mkdir(exist_ok=True)
pages={
'EVE_Assistant_Introduction_Desktop_DRAFT.html':('EVE Assistant — Desktop introduction','''<p>Bridgetek EVE Assistant combines engineering guidance and technical references with local tools for EVE application and asset development. This desktop version includes EAB, EveApps-BT82X and EveApps-Pre82X MCP servers.</p><h2>How customers use it</h2><p>Use a supported desktop ChatGPT or Codex environment with a local thread. Install Node.js, obtain the appropriate official EveApps repository checkout, configure its absolute local path and enable the plugin's MCP connections. Obtain the separate Rust EVE Asset Builder CLI distribution from https://github.com/Bridgetek/EAB-CLI for actual asset operations; keep eab_tools.exe, exts/ and dependencies/ together and select rust during setup. The documented binary distribution requires Windows 10/11 x64. Node.js is still needed for the MCP adapter. The separate EVE Emulator repository at https://github.com/Bridgetek/Eve-Emulator provides Windows binaries and Ubuntu 24.04 amd64 packages; the current example projects target Windows. Emulator installation and application execution are separate prerequisites, not additional MCP tools supplied by this plugin. Availability and installation depend on the host platform and plugin publication status.</p><p>Describe your chip, display, host platform and task. The assistant can retrieve indexed API references, inspect authorized local repository sources, find samples, propose screen scaffolds and build commands, and guide asset conversion. EAB execution requires approval for the exact operation. Source checks and build-command suggestions do not establish compiler, emulator or hardware success.</p><p>This plugin is for local development workflows and does not provide a hosted remote MCP service. It offers no payments or purchases. Host-platform or independently selected service fees remain governed by those services.</p><p>Check implementation-critical information against current official documentation and test on the intended hardware.</p>'''),
'EVE_Assistant_Privacy_Notice_Desktop_DRAFT.html':('EVE Assistant — Desktop privacy notice','''<p>This proposed notice covers the desktop release supplied by Bridgetek Pte Ltd, including its three local MCP integrations.</p><h2>Processing in the host platform</h2><p>Prompts, uploaded files and generated responses are processed by the ChatGPT or Codex environment you choose. Local MCP tools can return query text, local paths, source snippets, selected file content, indexed references, command arguments and diagnostics into that conversation. The host platform's applicable privacy terms, retention controls and workspace settings govern that processing. Running a tool locally does not mean its returned content stays outside the AI conversation.</p><h2>Local tools and access</h2><p>The EveApps servers read configured local repository checkouts. They provide reference retrieval, sample lookup, scaffold text, code checks and build-command suggestions. Configure only project material you are authorized to disclose. EAB can inspect local assets and, after the applicable approval, run installed EAB programs to create or overwrite outputs or interact with connected hardware. Repository/EAB paths are stored in a per-user local configuration file. Users can change or remove that configuration and disable or uninstall the integration through the host.</p><h2>Separate services and optional functions</h2><p>This integration adds no independent telemetry or Bridgetek-hosted conversation backend. The bundled EAB server includes optional GitHub installation/update checks and host-model sampling; these can involve their respective services when invoked. Separately installed development tools, hardware software and host integrations retain their own data practices. Do not provide credentials or private material without authorization.</p><h2>Bridgetek support</h2><p>Installing this plugin does not grant its creator access to individual private conversations. Information you separately send to Bridgetek support is handled under the <a href="https://brtchip.com/bridgetek-privacy-policy/">Bridgetek Privacy Policy</a> and existing support procedures.</p><p>Review host-platform settings for conversation retention and deletion. Future backend, analytics or other collection changes require this notice to be updated before release.</p>'''),
'EVE_Assistant_Terms_Desktop_DRAFT.html':('EVE Assistant — Desktop terms additions','''<p>Bridgetek EVE Assistant is provided by Bridgetek Pte Ltd to support evaluation and application development using EVE graphics controllers. The desktop release includes local MCP software and accompanies the terms governing your chosen ChatGPT or Codex environment.</p><h2>Local prerequisites and permissions</h2><p>You are responsible for obtaining compatible Node.js, repository checkouts, EAB installations, compiler/SDK components and hardware required for your workflow. Review the permissions for local repository access and process execution. Provide only material you are authorized to disclose. Approve local asset, output-file or hardware operations only after reviewing their target, inputs and effects.</p><h2>Validation and third-party rights</h2><p>AI output, source checks, generated scaffolds and build-command suggestions may contain errors or omissions. Validate device applicability and APIs against current official sources and perform appropriate compilation, emulator and hardware tests. Generated responses do not constitute certification or a guarantee of suitability. Bundled software, reference materials and independently installed tools retain their applicable licences and notices.</p><h2>Charges, support and privacy</h2><p>The plugin provides no payments or purchases. Host-platform and separately selected service fees are governed by those services. Use <a href="https://brtchip.com/technical-support/">existing Bridgetek technical support channels</a>; this plugin adds no response-time, uptime or service-level commitment. Use is subject to the <a href="https://brtchip.com/bridgetek-eve-assistant-privacy-policy/">EVE Assistant Privacy Notice</a> and host-platform privacy arrangements.</p><p>Use the assistant lawfully and do not use it to expose credentials, infringe rights or bypass security controls. Your organization's and the host platform's policies apply.</p>''')}
for filename,(title,body) in pages.items():
 (web/filename).write_text('<!doctype html><html lang="en"><meta charset="utf-8"><title>'+title+'</title><style>body{font:16px/1.6 system-ui;max-width:900px;margin:40px auto;padding:0 24px}.draft{background:#fff3cd;padding:16px}</style><body><p class="draft">DRAFT FOR COMPANY REVIEW — desktop release not yet published. Confirm wording and effective date before replacing the live page. Prepared 13 November 2026.</p><h1>'+title+'</h1>'+body+'</body></html>')
market=kit/'.agents/plugins';market.mkdir(parents=True,exist_ok=True)
(market/'marketplace.json').write_text(json.dumps({'name':'bridgetek-eve-desktop-preview','interface':{'displayName':'Bridgetek EVE Desktop Preview'},'plugins':[{'name':'gpt-1596bf20808468c76a5fa542649968e7','source':{'source':'local','path':'./plugin'},'policy':{'installation':'AVAILABLE','authentication':'ON_INSTALL'},'category':'Developer Tools'}]},indent=2)+'\n')
inner=kit/'Bridgetek_EVE_Assistant_0.9.16_Desktop_DRAFT.zip'
with zipfile.ZipFile(inner,'w',zipfile.ZIP_DEFLATED,strict_timestamps=False) as z:
 for f in sorted(p.rglob('*')):
  if f.is_file():z.write(f,f.relative_to(p))
(kit/'SHA256SUMS.txt').write_text(hashlib.sha256(inner.read_bytes()).hexdigest()+'  '+inner.name+'\n')
print(kit)
