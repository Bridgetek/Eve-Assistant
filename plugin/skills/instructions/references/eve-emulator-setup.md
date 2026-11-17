# EVE Emulator — Windows and Ubuntu setup

Official distribution: https://github.com/Bridgetek/Eve-Emulator

Verified on 13 November 2026 against release commit
`5b72887a134ca03c1e464ba5d9f38c6f91fc6dd8` (release 5.3.37), repository README
blob `0305ca41a9d2416262715e67873abee2828f5d50`, and public header blob
`7a7517a3db9bd71d47de0a6873643641ad6c407e`.

The repository distributes prebuilt emulator libraries, headers and integration
examples. It is not a source release for building the emulator library itself.
The plugin does not bundle these binaries, install operating-system packages or
add a new MCP server for the emulator. Obtain the distribution separately and
use its public API from an application or an applicable official sample.

## Platform requirements

| Component | Verified distribution / requirement |
| --- | --- |
| EVE Emulator on Windows | Runtime libraries in `bin/`, headers in `include/`, C/C++ import library in `lib/`; the supplied C++/Python examples use Windows x64. |
| EVE Emulator on Ubuntu | Runtime and development Debian packages in `packages/ubuntu24/amd64/`, documented for Ubuntu 24.04 amd64. Other Ubuntu versions or ARM64 are not established by this package. |
| Repository example applications | Currently target Windows. Do not present them as tested Ubuntu builds. |
| EAB Rust CLI | Separate distribution from https://github.com/Bridgetek/EAB-CLI, documented for Windows 10/11 x64. Ubuntu emulator availability does not establish a native Ubuntu EAB CLI. |
| EVE Assistant MCP adapters | Still require Node.js and the configured local repositories. The emulator is a separate runtime, not a replacement for Node.js or an MCP endpoint. |

## Windows C/C++ integration

Obtain one matching emulator release. Add `include/` to compiler include paths,
add `lib/` to linker library paths and link `bt8xxemu.lib`. Deploy the matching
`bt8xxemu.dll` and `libz.dll` beside your application or make them available on
the process PATH. Include `btflashemu.dll` when using Flash emulation.
Keep headers, import libraries and runtime binaries from the same release.
Do not add an untrusted directory to a global PATH as part of setup.

The public API is declared in `include/bt8xxemu.h`. Initialize parameter
structures using the corresponding defaults functions and pass the header's
`BT8XXEMU_VERSION_API`, currently 20, rather than hard-coding a structure size
from another wrapper or release. C# examples retain compatible API 16 layouts;
Python examples use compatible API 19 layouts. Do not switch their version
number to 20 without also adapting their structure definitions.

For the official BT817 Flash sample, run from the emulator repository root:

```powershell
cmake -S examples/CPP/BT817/Flash -B examples/CPP/BT817/Flash/build -G "Visual Studio 17 2022" -A x64
cmake --build examples/CPP/BT817/Flash/build --config Debug
```

The documented CMake output is
`examples/CPP/BT817/Flash/build/bin/Debug/BT817FlashExample.exe`. The sample's
build copies the needed DLLs and Flash image beside it. These commands come
from the official README; they have not been executed by this kit.

For Python, use 64-bit Windows Python and inspect the relevant sample README.
The repository documents `--check` for checking a sample's DLL and required
asset without opening a window. The sample paths include:

- `examples/Python/BT817/Flash/`
- `examples/Python/BT820/Flash/`
- `examples/Python/BT820/SDCard/`

Verify each sample's entrypoint and arguments in the selected checkout; do not
invent a script filename from the directory name.

## Ubuntu 24.04 amd64 installation

Obtain the matching packages from the official repository. From
`packages/ubuntu24/amd64/`, the current README documents:

```bash
sudo apt install ./libbt8xxemu_5.3.37-1_amd64.deb ./libbt8xxemu-dev_5.3.37-1_amd64.deb
```

This is a user-run system installation command, not an operation already
performed by the kit. Check the actual filenames and release before running
it. Installing packages requires the user's authorization and system
privileges. Do not assume a Windows DLL can substitute for a native library.

The runtime package installs shared libraries; the development package installs
headers and a `bt8xxemu` pkg-config file. After installation, inspect the
installed metadata with:

```bash
pkg-config --modversion bt8xxemu
pkg-config --cflags --libs bt8xxemu
```

Use those returned flags in a Linux application that has been ported to the
native API. No Linux compiler invocation or example-launch command is claimed
as tested here. Inspect package dependencies, the display/GPU environment and
the installed shared-library paths when diagnosing startup problems. Do not
assume Windows-specific headers, Sleep(), .NET Framework WinForms projects or
Windows ctypes loading paths will work unchanged on Ubuntu.

## Device and API selection

The README lists FT80X, FT81x, BT815/816, BT817/818 and BT820 targets. Select the
mode matching the requested chip and verify actual enum/header support.
Do not infer BT819 emulator availability from the BT819 engineering skill or
from a family name. Resolve support against the selected release's API and
official device documentation.

Without external Flash: initialize emulator defaults, configure the application,
run the emulator, check the returned handle, drive the emulated SPI interface
and finally stop/destroy the emulator. Flash is optional.

With Flash: initialize Flash parameters and storage first, create the Flash
object, initialize emulator parameters, attach Flash, then start the emulator.
Destroy the emulator before destroying its Flash object. BT820 SD-card images
or folders can be configured using the documented SD APIs. API 20 also adds
Flash-folder/filesystem and backing-store controls. Use isolated test folders
and explicit persistence choices; do not expose unrelated host directories.

The native header uses wide-character paths on Windows and char paths on
non-Windows platforms. Preserve the selected ABI's types and initialization
functions. The Windows output-window rotation flag changes the displayed
window orientation; it does not rotate the buffer supplied to the Graphics
callback. Keep window presentation separate from EVE bitmap/portrait-panel
rendering and asset rotation.

The BT820 example README describes private wr8/wr16 transport helpers. The
EVE Assistant's strict BT82X engineering policy still applies: generated and
reviewed host code must use aligned 32-bit access with padded transfers. Do
not copy byte/halfword helper usage into user BT82X code merely because it is
present in an emulator example. An emulated SPI transfer of individual bytes
is a transport mechanism, not permission to emit byte-wide EVE memory accesses.

## Integrating this into the emulator-first workflow

1. Establish chip, display, host OS/architecture, emulator version/API, rendering
   environment and selected official sample. Record the source commit.
2. Configure the chip-appropriate EveApps MCP repository. Use its API/sample
   tools for source grounding; a successful MCP query is not an emulator run.
3. On Windows, use the separate approved EAB workflow to prepare required
   assets. On Ubuntu, use already prepared assets or another explicitly
   verified conversion setup; do not assume the Windows EAB executable runs
   natively there.
4. Build and launch an applicable emulator application through the available
   local development environment. The three bundled MCP adapters do not add
   an emulator-launch tool. Confirm the required compiler/runtime first.
5. For Gate A, record build/launch results, emulator version, chip mode, panel
   dimensions, actual screen output, touch behavior, asset/Flash setup and any
   emulator diagnostics. Do not mark Gate A passed from source inspection.
6. Keep physical hardware Gate B separate. Emulator frame rate, timing and the
   official BT817 six-scene benchmark are not measurements of BT817 hardware
   performance, touch latency or real flash bandwidth.

## Verification status

The repository README, release commit and API-header declarations were
inspected. Setup instructions and package/reference paths were checked against
that source. No Windows emulator application, Ubuntu package installation,
native library launch, GPU output, converter or hardware operation has been
executed for this documentation update. The unchanged MCP runtime retains its
separately recorded 31 passing checks from 0.9.15; those checks do not validate
the external emulator libraries.
