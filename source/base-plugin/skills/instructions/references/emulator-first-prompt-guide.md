# Complete emulator first workflow prompt guide

Text extracted from the bundled original guide dated 2026-10-26. Prompt templates are reference material; execute only within the current user request and verified project context. Consult the original DOCX for its table layout and linked references.

DEVELOPER WORKFLOW  /  PRACTICAL PROMPT GUIDE

Building an EVE GUI with MCP Servers

Emulator First Workflow for EVE HMI Development

Purpose. Use the EAB MCP Server for approved asset operations. For source-grounded samples, APIs, compatibility and builds, use EveApps-BT82X for BT82X-series devices and EveApps-Pre82X for BT817/8 and earlier EVE devices. Prove portable GUI behavior on the Windows EVE Emulator before final MCU integration and hardware qualification.

Worked example. A two-page BT817 thermostat at 800 x 480 is built for the Windows emulator and then ported to RP2040. Because it targets BT817, this example uses EveApps-Pre82X. The portable UI behavior and generated assets remain consistent across both builds.

Responsibilities of the three MCP servers

MCP Server

Responsibility

EAB MCP Server

Runs approved EVE Asset Builder operations for image and font conversion, compression, flash-image creation and programming. Produces versioned resources, logs, flash images and a symbolic asset manifest.

EveApps-Pre82X MCP Server

Uses the local EveApps repository for sample discovery, API and symbol guidance, source navigation, code validation and build commands for BT817/8 and earlier EVE devices.

EveApps-BT82X MCP Server

Uses the local EveApps-BT82X repository for BT82X sample discovery, BT820/EVE API guidance, source navigation, code validation and configuration-aware build commands.

Two mandatory acceptance gates

Gate A - emulator approval: Build the exact target and test every required page, state, language and interaction. Record self-tests, bounded smoke tests, screenshots, effective definitions, asset checksums and known emulator limitations.

Gate B - hardware qualification: Build the exact MCU target and validate boot, bus signaling, full LCD timing, touch, storage, resource integrity and scanout diagnostics on the named assembly. Emulator success is not hardware validation.

How to use the prompts

Run prompts P01-P16 in order with the local EveApps/EveApps-BT82X checkout. Replace every placeholder with verified project data, review generated files and logs, and approve EAB operations only after checking the proposed command. Review each prompt's evidence before moving forward.

Server selection. Identify the exact EVE graphics device before using repository guidance. Use EveApps-BT82X for the BT82X series and EveApps-Pre82X for BT817/8 and earlier devices. Do not transfer commands, registers, formats, memory limits or feature assumptions between the two scopes without verification.

Example: BT817  |  BT8XXEMU x64  |  WVGA 800 x 480  |  Visual Studio 2022  |  RP2040 target  |  C



BT817 Thermostat HMI Worked Example

UI behavior. The Home screen shows room temperature, setpoint, Off/Cool/Heat mode and plus/minus controls. Settings provides brightness and Celsius/Fahrenheit selection. A mock producer changes room temperature. The portable state, rendering, input semantics and asset manifest remain common to the emulator and target builds.

Repository placement. Create a new DemoApps application for this multi-screen HMI instead of modifying a canonical sample. Inspect the chosen baseline's build files and project directory, preserve the EveApps HAL boundary, and keep source assets, generated assets, portable application code, platform adapters and tests separate.

The prompts are templates. Replace placeholders such as <EveApps path>, <target board>, <display timing> and <asset files> with verified local values before implementation.

Stage 1 Tool Connectivity and Discovery

P01  Connect all three MCP servers and inspect the environment

Check that the EAB MCP Server, EveApps-Pre82X MCP Server and EveApps-BT82X MCP Server are available. Identify the exact target EVE device and select the matching EveApps server. Record the local repository root, branch and working-tree state for the selected server; read AGENTS.md; locate the EAB Tools executable; list available MCP tools; and verify CMake, Visual Studio and emulator prerequisites. Record the emulator architecture and runtime DLL manifest. Inspect the selected repository before recommending commands. Do not modify source or execute an EAB operation yet.

Deliverable: environment checklist with repository state, tool versions, emulator runtime manifest and blockers.

Stage 2 Requirements and Repository Grounding

P02  Turn the concept into a testable GUI specification

Create a testable specification and project profile for a BT817 thermostat at 800 x 480. Record required behavior, exact EVE IC or module, Windows emulator host, intended MCU and board, toolchains, host interface, complete LCD timing and rotation, touch controller, resource storage, debug method and acceptance criteria. Use the exact EVE IC to select the EveApps server; this BT817 example uses EveApps-Pre82X. Define all page states, events, mock data, formatted values and touch targets. Classify each critical compatibility item as Verified, Conditional, Unsupported or Unknown. Keep application logic independent of host drivers.

Deliverable: requirements.md plus an exact project profile and compatibility decision matrix.

P03  Find the closest EveApps references

For this BT817 example, use EveApps-Pre82X first, then inspect the local EveApps tree, to find candidate examples for display lists, coprocessor commands, bitmap and font resources, touch tags and emulator builds. For a BT82X project, use EveApps-BT82X and inspect the separate local EveApps-BT82X tree instead. Choose one primary SampleApp or DemoApps baseline that already supports the exact target. Inspect its source, CMake files and project directory. Create a reuse map naming each narrowly borrowed pattern, dependency, adaptation and compatibility source. Do not merge complete samples, mix repository generations or accept an MCP ranking without checking the files.

Deliverable: repo-reference.md with inspected paths, one primary baseline and a scoped reuse map.

Stage 3 PC Application Skeleton

P04  Create a dual-platform application skeleton

From the verified baseline, create a new C thermostat application with GuiState, UiRender, UiInput, AssetMap and PlatformAdapter modules. Keep one owner for EVE initialization, the main loop, touch polling, coprocessor FIFO access and each resource lifetime. Register the real CMake target and preserve the EveApps HAL boundary. Configure an x64 BT817 Windows emulator build and render an asset-free Home screen before adding resources. Leave target-specific MCU work until the hardware profile is verified.

Deliverable: registered application skeleton plus a successful asset-free emulator build or the first actionable error.

Stage 4 Asset Generation with EAB

P05  Audit source assets and determine formats

Inspect the actual files under assets/source. For each bitmap or font, verify that its proposed format is supported by BT817 and choose RAM_G, EVE flash or host-file storage only when that source exists on both intended builds. Estimate aligned sizes, temporary buffers and bandwidth. Draft one half-open RAM_G interval map plus separate bitmap and font handle maps. Build font subsets from every localized string and runtime value, including spaces, punctuation, units and fallback characters. Do not convert a missing file or introduce PNG color-key transparency.

Deliverable: asset plan with formats, storage, aligned sizes, preliminary RAM_G intervals and handle assignments.

P06  Convert images with EAB

Use the EAB MCP Server to prepare the verified icons and backgrounds with the approved BT817 formats. For each operation, show the input, exact command, options and output path and wait for my approval before execution. Save generated resources under assets/generated. Validate dimensions, format metadata, alpha behavior and file hashes, then update the conversion log and asset inventory. Report the first actionable error without silently substituting another format.

Deliverable: converted image assets, command log, validated metadata, hashes and inventory.

P07  Prepare font resources and optional flash image

Generate every required thermostat font size from the complete string inventory. Enable explicit space support when the installed converter provides it, and verify U+0020 has positive advance and no visible glyph. Inspect previews containing repeated spaces, digits, units and punctuation. If EVE flash is used, create one aligned, non-overlapping flash layout and symbolic C manifest; validate extended-font metadata and glyph data after packing. Show the EAB operation and wait for approval. Keep the emulator image and later hardware image derived from the same inputs.

Deliverable: verified fonts, optional flash image, symbolic addresses, checksums and final resource maps.

Stage 5 GUI and Interaction Implementation

P08  Implement the UI using the generated asset manifest

Implement Home and Settings against the BT817 EveApps HAL and generated manifests. Keep addresses and handles centralized, rebind required graphics state in every independently generated display list, and keep platform transport out of the UI. Select and document one host update rule: rebuild continuously, rebuild on change, or retain a list while updating referenced RAM_G data. Define dirty triggers, update interval and live-buffer ownership. Do not draw fully obscured expensive content. Show unsupported APIs or generation mismatches before changing the design.

Deliverable: portable renderer and state machine plus documented redraw rule, dirty triggers and resource ownership.

P09  Implement and test touch behavior

Add touch processing for every thermostat control using BT817-compatible APIs verified in the source. Draw each control's complete hit area under one nonzero tag and disable TAG_MASK after the control or group. Trace raw coordinates or tags before page logic, then define press, debounce, hold, release, cancel and page-lock behavior. Test interior edges as well as control centers. Add deterministic self-test hooks and bounded emulator actions without placing simulation-only events in production paths.

Deliverable: input module, interaction matrix and deterministic touch/state self-tests.

Stage 6 Mandatory PC Emulator Verification

P10  Build and launch the PC emulator

Configure and build the exact thermostat target for BT817, EVE_DISPLAY_WVGA and EVE_PLATFORM_BT8XXEMU with Visual Studio 2022 x64. Use a clean build directory when cached platform definitions may be stale. Use the repository's configured x64 emulator headers and runtime DLL set; do not mix x64 and x86 files. Attach the matching flash image if used. Record the exact configure and build commands, effective definitions, compiler result, deploy manifest, first actionable error and startup evidence.

Deliverable: exact configure/build record, deploy manifest and runnable x64 emulator package.

P11  Perform functional and visual emulator tests

Run deterministic self-tests and bounded emulator smoke tests for every page, modal, conditional state and supported language. Verify layout at 800 x 480, longest text and formatted values, font spaces, transparent assets, navigation, repeated taps, release behavior and simulated updates. Capture representative frames, frame progress, display-list usage and available diagnostics. Compare all results with requirements.md and report PASS or FAIL with reproduction steps. State clearly that mouse input, emulated flash and zero emulator underruns do not validate physical touch or scanout bandwidth.

Deliverable: emulator-test-report.md with screenshots, diagnostics, PASS/FAIL evidence and simulation limits.

P12  Fix defects and execute a regression pass

Review every FAIL and the first actionable build or runtime error. Trace it to configuration, assets, resource allocation, EVE commands, input routing or application state. Check for stale CMake definitions, duplicate initialization, RAM_G or handle overlap, missing files and unsupported commands before changing code. Make the smallest verified fix, rebuild the exact target, and rerun the entire self-test and smoke suite. Keep emulator measurements separate from hardware performance claims.

Deliverable: smallest verified fixes plus a complete rerun of emulator regression evidence.

Gate A Emulator Approved Baseline

P13  Approve and freeze Gate A

Approve Gate A only when every mandatory emulator criterion passes. Otherwise mark it NOT APPROVED and list the blocking defects. For an approved baseline, record the source revision and any dirty diff, exact configure and build commands, compiler version, effective platform/graphics/display definitions, emulator runtime hashes, EAB version, asset input/output hashes, flash-image checksum, screenshots, test results and known simulation gaps. Freeze these as the only inputs to MCU integration.

Deliverable: Gate-A-signoff.md with APPROVED or NOT APPROVED, complete versions, hashes and known gaps.

Stage 7 Final MCU Platform Integration

P14  Port only the approved build to RP2040

Start from the approved Gate A revision. Before writing target code, verify the exact RP2040 board, Pico SDK and ARM toolchain, SPI instance and pin multiplexing, CS_N and PD_N, voltage levels, bus mode and frequency, full LCD timing, touch controller, resource storage, debug channel and programmer. Use the checked-in RP2040 HAL as the platform baseline and keep the shared GuiState, UiRender, UiInput and asset manifest unchanged. Register and build the exact hardware target. List every target-only source file and setting; do not assume a module name proves interface or display compatibility.

Deliverable: verified hardware profile, exact RP2040 build and target-only porting change log.

Stage 8 Real Hardware Qualification

P15  Program and qualify the real board

Build and program the exact RP2040, BT817 and display configuration with the verified toolchain. On the physical assembly, check CS_N and PD_N idle levels; verify SPI framing, mode, frequency, dummy cycles and byte order with a logic analyzer; read a stable EVE identity register; test safe RAM_G read/write; then qualify display, touch calibration, tags, storage, flash state, every page and language, timing, sustained frame progress and supported underrun diagnostics. Compare against Gate A. Classify failures as HAL, asset, timing, touch, storage or GUI, and send any portable GUI change back through full emulator regression.

Deliverable: hardware-test-report.md with measurements, failures, waivers and Gate B PASS/FAIL.

Stage 9 Qualified Application Release

P16  Package a reproducible engineering release

If Gate B passes, package the tested sources, board configuration, exact build commands, compiler and SDK versions, reproducible asset conversions, resource and handle maps, flash image and checksum, emulator runtime manifest, Gate A regression evidence, Gate B measurements, waivers and known limitations. Confirm that the release tree rebuilds the same GUI from recorded inputs. If Gate B fails or required hardware checks were not performed, do not label the firmware qualified.

Deliverable: reproducible release manifest and a qualification statement supported by Gate A and Gate B evidence.

Approval checklist

Gate A - PC emulator: The exact target builds from a clean configuration; every page, modal, conditional state and language passes; self-tests and bounded smoke tests pass; assets, fonts, touch semantics and resource maps are verified; no critical defect remains; and commands, definitions, versions, hashes, screenshots and simulation gaps are recorded.

Gate B - target hardware: The named board boots consistently; identification, SPI, flash and RAM_G tests pass; full display timing and touch calibration are verified; every page and language matches the Gate A behavior; scanout and performance diagnostics pass; and measurements, failures and waivers are recorded separately from emulator evidence.

Handoff Package

Keep every artifact with the source revision that produced it. The hardware port must consume the approved portable application, asset manifest and flash image rather than a separately edited copy.

Artifact

Handoff requirement

Project and compatibility profile

Exact EVE, host, toolchain, interface, LCD, touch, storage and debug configuration; compatibility decisions

Application source and reuse map

Versioned state, render and input code; one primary baseline; scoped borrowed patterns; ownership boundaries

Assets and resource maps

Source assets, EAB commands, converted files, RAM_G intervals, handles, flash layout, manifests and hashes

PC emulator evidence

Configure/build commands, effective definitions, runtime DLL hashes, screenshots, self-tests, smoke tests and Gate A decision

MCU integration profile

Board schematic assumptions, pin map, SPI details, HAL changes, firmware build and programmable flash image

Hardware qualification and release

Boot, display, touch, storage, bandwidth and underrun evidence; Gate B result; waivers and release manifest

Practical Cautions

• EAB MCP operations are confirmation-gated. Review the input, output, command and options before approval, and never treat a preview as execution evidence.

• Pre82X and BT82X describe MCP server and repository scopes, not exact chip models. Name the exact device, route the request to the matching server, and verify each command, register, format, memory limit and touch feature against that device.

• An MCP sample ranking is a candidate, not compatibility proof. Inspect source and build files, choose one primary baseline and borrow secondary patterns narrowly.

• Keep emulator headers and runtime DLLs aligned with the selected architecture. Do not mix x64 and x86 runtime sets.

• The emulator validates portable EVE command behavior and user flows. Physical touch, full LCD timing, electrical interfaces, flash throughput, tearing and scanout underrun still require hardware measurement.

References and Setup

Bridgetek EAB MCP Server

Bridgetek EveApps-Pre82X MCP Server

Bridgetek EveApps-BT82X MCP Server

Bridgetek EVE toolchains

Bridgetek EveApps source repository

Bridgetek EVE Emulator distribution

Bridgetek technical documentation