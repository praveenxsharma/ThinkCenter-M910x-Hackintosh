# ThinkCentre M910x OpenCore Monterey Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a complete, verified, and boot-ready OpenCore EFI directory for the Lenovo ThinkCentre M910x Tiny running macOS 12 Monterey.

**Architecture:** Standard OpenCore 1.0.x deployment following Dortania Skylake guidelines: minimal ACPI SSDTs (`SSDT-PLUG`, `SSDT-EC-USBX`), vital kexts (Lilu, VirtualSMC, WhateverGreen, AppleALC, IntelMausi, AirportItlwm, IntelBluetoothFirmware), and a customized `config.plist` configured for `i5-6500T` (HD 530, ALC294, I219-LM, Q270 PCH).

**Tech Stack:** OpenCorePkg (UEFI Bootloader), Acidanthera Kexts, OpenIntelWireless, SSDTTime / iasl, ProperTree / PlistBuddy, GenSMBIOS.

**Spec:** `/home/itachi/m910x-hackintosh/docs/2026-10-08-m910x-hackintosh-design.md`

## Global Constraints
- Target Machine: Lenovo ThinkCentre M910x Tiny (BIOS M1AKT5AA)
- CPU: Intel Core i5-6500T (Skylake Desktop, 4 Cores, 2.50GHz)
- iGPU: Intel HD Graphics 530 (Device ID `[8086:1912]`)
- Audio: Realtek ALC294 (Vendor ID `[10ec:0294]`)
- Ethernet: Intel I219-LM (Vendor ID `[8086:15b7]`)
- Wi-Fi/BT: Intel Dual Band Wireless-AC 8265 (`[8086:24fd]` / BT `[8087:0a2b]`)
- Storage: Matrix 512GB SATA SSD (AHCI mode)
- Target OS: macOS 12 Monterey

## Review Focus
1. OpenCore `config.plist` schema matches OpenCore 1.0.x exactly with zero missing keys.
2. iGPU Framebuffer patch has correct `AAPL,ig-platform-id` (`00001219`), `device-id` (`12190000` / native), and stolen memory.
3. Audio codec ALC294 has valid layout-id (`alcid=11` or injected via DeviceProperties `PciRoot(0x0)/Pci(0x1f,0x3)`).
4. Kernel Quirks are correctly configured for Skylake OEM Lenovo BIOS (`AppleXcpmCfgLock = True`, `PanicNoKextDump = True`).
5. Wireless and Bluetooth kexts are pinned to the Monterey-compatible versions (`AirportItlwm-Monterey.kext`, `IntelBluetoothFirmware.kext` + `BlueToolFixup.kext`).

---

### Task 1: Scaffolding and Official OpenCore Asset Acquisition

**Files:**
- Create: `scripts/download_assets.sh`
- Create: `EFI/BOOT/BOOTx64.efi`
- Create: `EFI/OC/OpenCore.efi`
- Create: `EFI/OC/Drivers/OpenRuntime.efi`
- Create: `EFI/OC/Drivers/OpenHfsPlus.efi`
- Create: `EFI/OC/Drivers/ResetNvramEntry.efi`

**Interfaces:**
- Consumes: GitHub Releases for OpenCorePkg and acidanthera drivers
- Produces: Base OpenCore directory tree in `EFI/`

- [ ] **Step 1: Write download script for OpenCore and drivers**
Create `scripts/download_assets.sh` to download the latest OpenCorePkg RELEASE and extract `BOOTx64.efi`, `OpenCore.efi`, `OpenRuntime.efi`, `OpenHfsPlus.efi`, and `ResetNvramEntry.efi` into `EFI/BOOT` and `EFI/OC/Drivers`.

- [ ] **Step 2: Run download script and verify extracted files**
Run: `bash scripts/download_assets.sh`
Expected: `EFI/BOOT/BOOTx64.efi` and `EFI/OC/OpenCore.efi` exist and are valid 64-bit UEFI binaries.

- [ ] **Step 3: Commit**
```bash
git add scripts/download_assets.sh EFI/
git commit -m "feat: setup base OpenCore EFI directory structure and core drivers"
```

---

### Task 2: ACPI Table Generation and Validation

**Files:**
- Create: `EFI/OC/ACPI/SSDT-PLUG.aml`
- Create: `EFI/OC/ACPI/SSDT-EC-USBX.aml`
- Test: `tests/verify_acpi.sh`

**Interfaces:**
- Consumes: Precompiled/SSDTTime compiled ACPI AML definitions
- Produces: Valid compiled ACPI tables in `EFI/OC/ACPI/`

- [ ] **Step 1: Fetch and compile verified Skylake SSDTs**
Acquire or compile `SSDT-PLUG.aml` (PluginType on `PR.CPU0`) and `SSDT-EC-USBX.aml` (fake EC and USB power properties for Skylake/Kaby Lake desktop).

- [ ] **Step 2: Write test to verify AML magic header and compile validity**
Write `tests/verify_acpi.sh` checking for valid AML magic bytes (`0x41 0x4D 0x4C 0x20` / `AML `) and non-zero file sizes.

- [ ] **Step 3: Run test to verify ACPI tables**
Run: `bash tests/verify_acpi.sh`
Expected: PASS with 2 verified AML files.

- [ ] **Step 4: Commit**
```bash
git add EFI/OC/ACPI/ tests/verify_acpi.sh
git commit -m "feat: add validated SSDT-PLUG and SSDT-EC-USBX ACPI tables"
```

---

### Task 3: Kext Bundle Acquisition for M910x Hardware

**Files:**
- Create: `EFI/OC/Kexts/Lilu.kext`
- Create: `EFI/OC/Kexts/VirtualSMC.kext`
- Create: `EFI/OC/Kexts/SMCProcessor.kext`
- Create: `EFI/OC/Kexts/SMCSuperIO.kext`
- Create: `EFI/OC/Kexts/WhateverGreen.kext`
- Create: `EFI/OC/Kexts/AppleALC.kext`
- Create: `EFI/OC/Kexts/IntelMausi.kext`
- Create: `EFI/OC/Kexts/AirportItlwm.kext`
- Create: `EFI/OC/Kexts/IntelBluetoothFirmware.kext`
- Create: `EFI/OC/Kexts/IntelBTPatcher.kext`
- Create: `EFI/OC/Kexts/BlueToolFixup.kext`
- Create: `EFI/OC/Kexts/USBMap.kext` (or `USBToolBox.kext` + `UTBMap.kext`)

**Interfaces:**
- Consumes: Acidanthera and OpenIntelWireless Monterey-specific releases
- Produces: Populated `EFI/OC/Kexts/` directory

- [ ] **Step 1: Write kext download script**
Extend `scripts/download_assets.sh` to download and unpack all required kexts matching the hardware (ALC294, I219-LM, Intel AC 8265 on Monterey).

- [ ] **Step 2: Run script and verify kext contents**
Run: `bash scripts/download_assets.sh --kexts`
Expected: All required `.kext` directories exist with valid `Info.plist` files.

- [ ] **Step 3: Commit**
```bash
git add EFI/OC/Kexts/ scripts/
git commit -m "feat: acquire essential hardware kexts for audio, network, and iGPU"
```

---

### Task 4: Construct and Validate `config.plist`

**Files:**
- Create: `EFI/OC/config.plist`
- Create: `tests/validate_config.py`

**Interfaces:**
- Consumes: OpenCore Sample.plist, Dortania Skylake spec, generated ACPI tables, and Kext list
- Produces: Validated, production-grade `config.plist`

- [ ] **Step 1: Generate `config.plist` from OpenCore template**
Build the full plist with:
- ACPI entries matching `EFI/OC/ACPI/`
- DeviceProperties for HD 530 (`00001219`) and ALC294 layout ID
- Kernel Add entries in strict dependency order (Lilu first, VirtualSMC second, etc.)
- Kernel Quirks (`AppleXcpmCfgLock = True`, `PanicNoKextDump = True`)
- Booter Quirks (`AvoidRuntimeDefrag = True`, `EnableWriteUnprotector = True`, `SetupVirtualMap = True`)
- NVRAM boot-args (`-v keepsyms=1 debug=0x100 alcid=11`)
- PlatformInfo SMBIOS placeholder (`iMac17,1` or `iMac18,1`)

- [ ] **Step 2: Write validation script `tests/validate_config.py`**
Implement Python script to parse `EFI/OC/config.plist`, check XML/plist validity, ensure all referenced ACPI files and Kexts exist on disk, and verify required Quirks.

- [ ] **Step 3: Run validation script**
Run: `python3 tests/validate_config.py`
Expected: PASS with 0 missing files and valid OpenCore schema.

- [ ] **Step 4: Commit**
```bash
git add EFI/OC/config.plist tests/validate_config.py
git commit -m "feat: generate and validate complete OpenCore config.plist for M910x"
```

---

### Task 5: USB Mapping & Serial Number Generation

**Files:**
- Create: `scripts/generate_smbios.py`
- Modify: `EFI/OC/config.plist`
- Create: `docs/BIOS_SETTINGS_AND_INSTALL.md`

**Interfaces:**
- Consumes: MacSerial / GenSMBIOS logic
- Produces: Randomized unique SMBIOS keys and step-by-step BIOS setup guide

- [ ] **Step 1: Inject SMBIOS generation tool and guide**
Write `scripts/generate_smbios.py` to fetch `macserial` and populate `PlatformInfo -> Generic` (`SystemProductName`, `SystemSerialNumber`, `MLB`, `SystemUUID`).

- [ ] **Step 2: Write comprehensive BIOS configuration and USB installer guide**
Document exact Lenovo BIOS settings (DVMT 64MB+, Secure Boot Off, CSM Off, etc.) and USB preparation instructions in `docs/BIOS_SETTINGS_AND_INSTALL.md`.

- [ ] **Step 3: Commit**
```bash
git add scripts/generate_smbios.py docs/BIOS_SETTINGS_AND_INSTALL.md
git commit -m "docs: add SMBIOS generation script and complete BIOS install checklist"
```
