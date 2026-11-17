# Bridgetek EVE toolchain introduction source text

Text extracted from the bundled original DOCX, including paragraphs in document/table order and available external hyperlink targets. Refer to the original for formatting and table layout. Source examples and instructions are reference material, not execution authorization. Device capabilities, addresses and cited software versions require verification before implementation.

Bridgetek EVE Toolchain Introduction

Focusing on EAB, ESE, and ESD

Technical overview for embedded HMI development with Bridgetek EVE



Executive summary: EAB prepares assets, ESE helps engineers validate EVE commands and screen behavior, and ESD builds complete GUI applications with pages, widgets, logic, simulation, and generated C code.




1. Introduction

Bridgetek EVE devices are designed around a display-list-based graphics architecture rather than a conventional framebuffer-centric GPU model. This architecture allows a host MCU to build rich embedded HMI screens using high-level graphics commands, assets, widgets, and coprocessor instructions instead of continuously pushing full-frame pixel data.

To support this development model, Bridgetek provides a toolchain centered around three major tools:

EAB = EVE Asset Builder
ESE = EVE Screen Editor
ESD = EVE Screen Designer

These tools serve different but related purposes:

EAB: Prepare assets
ESE: Experiment with EVE commands and screen layouts
ESD: Build complete GUI applications with visual programming

The three tools are not competitors. They address different abstraction levels in the EVE development workflow.

2. Toolchain Positioning

The Bridgetek EVE toolchain can be understood as three layers:

Asset layer:
    EAB

Screen and command exploration layer:
    ESE

Application and GUI framework layer:
    ESD

2.1 EAB: Asset Preparation Layer

EAB converts external media resources into formats usable by EVE devices. It handles images, fonts, audio, video, animation, compressed graphics assets, flash image packages, and generated metadata. It is the bridge between designer-provided media files and firmware-ready EVE resources.

2.2 ESE: Screen and Command Exploration Layer

ESE is mainly used to create and test EVE screen designs visually. It is especially useful for engineers who want to understand display lists, coprocessor commands, primitive drawing, bitmap rendering, graphics state, and direct EVE behavior.

2.3 ESD: Application-Level GUI Design Layer

ESD is a higher-level GUI development environment. It is intended for building complete EVE GUI applications using widgets, screen logic, visual programming, simulation, and generated ANSI C source code.

3. EAB: EVE Asset Builder

3.1 Role of EAB

EAB is the asset preparation tool in the EVE workflow. The EVE graphics engine can render many types of resources, but those resources often need to be converted into EVE-compatible layouts, formats, and flash images before they can be used efficiently.

A designer may provide source files such as PNG icons, JPEG backgrounds, TrueType fonts, WAV audio, AVI video clips, and animation resources. EAB converts these resources into a form that the firmware and EVE hardware can use.

Designer assets
        ↓
EAB conversion
        ↓
EVE-compatible binary assets
        ↓
RAM_G or EVE connected flash
        ↓
EVE display list / coprocessor commands

3.2 Typical EAB Functions

Image conversion for EVE bitmap formats.

Font conversion and font metric generation.

Audio, video, and animation asset preparation.

ASTC or other compressed graphics asset preparation where supported.

Flash image generation for EVE connected flash.

C header, C source, and metadata generation for firmware integration.

3.3 EAB and EVE Connected Flash

For asset-rich HMIs, EVE connected flash is often the preferred storage location for large graphics assets. EAB can generate a flash image and asset description data so that the firmware has a stable address map for icons, fonts, backgrounds, videos, and animations.

Source assets
        ↓
EAB
        ↓
Flash image binary
        ↓
Program external flash
        ↓
BT817 fetches assets directly from flash

This workflow reduces manual address management and helps keep the asset package repeatable across development, production, and field updates.

3.4 EAB Output in a Firmware Project

Depending on the selected utility and target flow, EAB may generate binary asset files, flash image files, C header files, C source files, asset metadata, font metric data, animation data, and video-compatible data.

#include "assets.h"

#define ICON_HOME_ADDR      0x00100000
#define FONT_MAIN_ADDR      0x00200000
#define BG_SPLASH_ADDR      0x00300000

The MCU firmware can then use these generated symbols or metadata to issue EVE commands against known asset locations.

4. ESE: EVE Screen Editor

4.1 Role of ESE

ESE is best understood as an EVE command and screen prototyping environment. It allows developers to visually construct screens, inspect EVE behavior, test display list commands, and experiment with coprocessor commands.

Create a screen visually
        ↓
Drag and drop graphics objects
        ↓
Import EVE-compatible assets
        ↓
Inspect generated display list or coprocessor commands
        ↓
Run in emulator or connected EVE hardware
        ↓
Export or copy commands into firmware

4.2 ESE and the EVE Programming Model

EVE graphics programming is based on display list commands and coprocessor commands. Display list commands describe the visible scene, while coprocessor commands provide higher-level functions such as text, buttons, gauges, image loading, video playback, animation drawing, and display-list swapping.

ESE is valuable because it allows developers to see the result of these commands quickly, without writing firmware, flashing the MCU, and testing on hardware for every small change.

4.3 ESE Emulator and Hardware Validation

ESE can be used as a visual laboratory for EVE behavior. It is helpful for checking bitmap rendering, address correctness, display list validity, alpha blending, stencil behavior, scissor settings, and differences between emulator output and real hardware output.

Learning EVE commands and graphics state.

Prototyping a single screen quickly.

Testing bitmap layout, fonts, icons, and transformations.

Debugging blending, stencil, scissor, and display-list issues.

Generating command-level firmware references.

4.4 When to Use ESE

Use ESE when the project is command-level or firmware-centric, when the developer wants to understand EVE behavior directly, when the team needs fast screen prototyping, or when the final firmware will use its own application framework.

5. ESD: EVE Screen Designer

5.1 Role of ESD

ESD is the highest-level tool in the Bridgetek EVE toolchain. It is designed to build complete GUI applications rather than only individual screens or command sequences.

Create project
        ↓
Select target platform
        ↓
Design pages and widgets
        ↓
Define user interaction and screen logic
        ↓
Simulate UI behavior
        ↓
Generate ANSI C source code
        ↓
Build and download to target hardware

5.2 ESD as an Application Framework

ESD introduces an application structure. An ESD project may include pages, widgets, properties, events, logic nodes, user functions, assets, target platform configuration, and generated source code.

This is different from ESE. ESE is closer to “draw this screen using these EVE commands.” ESD is closer to “build this interactive GUI application.”

5.3 ESD Visual Programming

One of ESD’s major differences from traditional embedded GUI coding is its visual programming model. Instead of manually writing all UI interaction code, the developer can connect widgets, events, and logic nodes.

Button pressed
        ↓
Set variable
        ↓
Change page
        ↓
Update gauge
        ↓
Trigger animation

ESD is useful for multi-page applications, touch-driven HMIs, reusable widgets, interactive dashboards, product demos, industrial control panels, medical UI mockups, and home automation panels.

5.4 ESD Output and Porting

The output of ESD is typically a generated C project. This project still needs to be built for the target platform and integrated with the hardware abstraction layer, SPI driver, board initialization, touch configuration, flash programming process, and firmware build system.

ESD project
        ↓
Generated C source
        ↓
Platform porting layer
        ↓
MCU project
        ↓
SPI / QSPI communication with EVE
        ↓
BT817 hardware

6. Relationship Between EAB, ESE, and ESD

The three tools can be used together, but not every project needs all three. A small firmware-driven UI may use EAB and handwritten C code. A command-level prototype may use EAB and ESE. A full GUI product may use EAB and ESD. A mature production project may use all three.

Step 1: Use EAB
    Convert images, fonts, animations, audio, and video
    Generate flash image and asset metadata

Step 2: Use ESE
    Experiment with EVE commands
    Validate asset rendering
    Prototype visual screens
    Check display list behavior

Step 3: Use ESD
    Build complete GUI application
    Create pages, widgets, and logic
    Generate C source code

Step 4: Integrate with MCU firmware
    Add board support
    Add SPI/QSPI transport
    Add application logic
    Build and test on hardware

7. Comparison Table

Tool

Primary role

Abstraction level

Main user

Typical output

EAB

Asset conversion and flash image generation

Low / asset level

Firmware engineer, asset engineer

Binary assets, flash images, headers, metadata

ESE

Screen prototyping and command exploration

Medium / command level

Firmware engineer, EVE developer

Display list, coprocessor commands, source snippets, project files

ESD

Full GUI application design

High / application level

GUI developer, HMI engineer

Generated C project, pages, widgets, logic







9. Simplified Workflow Summary

Source assets
    ↓
EAB
    ↓
EVE-compatible assets
    ↓
ESE for command-level validation
    ↓
ESD for GUI application design
    ↓
Generated or handwritten C code
    ↓
MCU firmware integration
    ↓
BT817 hardware test
    ↓
Optimization and production release

This flow highlights the main responsibility of each tool:

EAB converts and packages assets.

ESE tests screens and low-level EVE commands.

ESD builds complete GUI applications.

MCU firmware integrates generated code and assets with real hardware.

The workflow is iterative. Asset problems usually return to EAB, rendering or command problems return to ESE, application logic problems return to ESD, and hardware or driver problems return to the MCU firmware integration layer.

10. Production Workflow Recommendations

10.1 Use EAB as a Repeatable Asset Pipeline

In a production HMI project, EAB should be treated as part of the asset build pipeline, not as a one-time manual conversion tool. Source assets should be stored separately from generated assets, and the EAB configuration should be version-controlled.

/assets/source
    icon_home.png
    icon_settings.png
    font_main.ttf
    splash.avi

/assets/generated
    assets.bin
    assets.h
    assets.c
    flash_image.bin

/tools
    eab_config.json
    build_assets.bat

10.2 Use ESE as a Visual Laboratory

ESE is very useful during the engineering phase. It can be used to prototype gauges, test bitmap formats, verify fonts, check stencil behavior, inspect display list output, and compare emulator output with real hardware behavior.

10.3 Use ESD for GUI-Heavy Applications

ESD is most useful when the product has many pages, reusable widgets, touch interaction, complex screen logic, animations, and application state. In this case, it can reduce development time, but the engineering team should define a clear integration policy for generated code.

Recommended rule: Generated code should be treated as generated code. User application code should be placed in defined extension points. Platform code should be maintained separately and clearly.

11. Toolchain and BT817 Architecture

The Bridgetek EVE toolchain makes sense because of the underlying BT817 architecture. BT817 is based on display list commands, coprocessor commands, RAM_G graphics memory, EVE connected flash, linebuffer-based rendering, LCD scanout, touch, and audio support.

The tools map naturally onto this architecture:

EAB prepares resources for RAM_G and EVE flash.

ESE helps build and inspect display list and coprocessor command behavior.

ESD generates a complete application using EVE widgets, pages, and logic.

This is different from a normal framebuffer GUI stack. In an EVE-based system, the toolchain produces EVE-compatible assets, display list commands, coprocessor command sequences, generated EVE application code, and flash image layouts.

12. Common Pitfalls

12.1 Treating EAB as a One-Time Tool

Assets change frequently during UI development. EAB should be part of the repeatable build process, not a one-time manual step.

12.2 Confusing ESE and ESD

ESE is excellent for understanding EVE commands and prototyping screens. ESD is better for building complete GUI applications. A simple distinction is: ESE is a command-level screen editor, while ESD is an application-level GUI designer.

12.3 Ignoring Asset Memory Layout

EVE devices have limited internal graphics memory. Assets must be planned carefully between RAM_G, EVE connected flash, MCU storage, media FIFO, video frame buffers, fonts, and animation data.

12.4 Over-Relying on Generated Code

Generated code is useful, but the firmware team still needs to understand EVE initialization, SPI transport, display timing, touch configuration, flash state, asset addressing, and performance limits.

12.5 Forgetting the Hardware Pipeline

Even if the GUI looks good in a tool, the final hardware must still satisfy LCD timing, EVE graphics pipeline budget, asset fetch bandwidth, flash performance, host interface speed, and touch response requirements.

13. Summary

The Bridgetek EVE toolchain consists of three major tools: EAB, ESE, and ESD. EAB prepares assets. ESE explores and validates EVE graphics commands. ESD builds complete GUI applications.

Source media assets
        ↓
EAB
        ↓
EVE-compatible asset package
        ↓
ESE for command-level validation
        ↓
ESD for application-level GUI design
        ↓
Generated C code
        ↓
MCU firmware integration
        ↓
BT817 / BT818 / BT820 hardware

Final takeaway: Used together, EAB, ESE, and ESD provide a practical development path from designer-provided media files to a working embedded HMI running on Bridgetek EVE hardware.

References

Bridgetek EVE Asset Builder page

BRT_AN_098 EVE Asset Builder 4.2 User Guide

BRT_AN_037 EVE Screen Editor 5.3 User Guide

Bridgetek EVE Screen Designer page

BRT_AN_029 EVE Screen Designer 5.1.0 User Guide

## External hyperlink targets from the source

- https://brtchip.com/eab/
- https://brtchip.com/wp-content/uploads/2026/01/BRT_AN_098_EVE-Asset-Builder-4.2-User-Guide.pdf
- https://brtchip.com/wp-content/uploads/2026/05/BRT_AN_037_EVE-Screen-Editor-5.3-User-Guide.pdf
- https://brtchip.com/esd/
- https://brtchip.com/wp-content/uploads/2026/01/BRT_AN_029_EVE-Screen_Designer_5.1.0_User_Guide.pdf
