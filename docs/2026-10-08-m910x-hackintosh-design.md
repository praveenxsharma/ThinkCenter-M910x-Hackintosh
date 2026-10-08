# ThinkCentre M910x Hackintosh Design & Deployment Plan

## 1. System Specifications & Scope
- **Target Machine**: Lenovo ThinkCentre M910x Tiny
- **CPU**: Intel Core i5-6500T (Skylake Desktop, 4C/4T, 2.5 GHz base / 3.1 GHz turbo)
- **iGPU**: Intel HD Graphics 530 (Native in Monterey)
- **RAM**: 8GB DDR4 (SO-DIMM)
- **Storage**: 512GB SSD (NVMe / SATA)
- **Ethernet**: Intel I219-LM (Gigabit)
- **Audio**: Realtek ALC233 / ALC662 (typical M910x layout)
- **Target OS**: macOS 12 Monterey (12.7.x)
- **Bootloader**: OpenCore (Latest Release, 1.0.x)

---

## 2. OpenCore EFI Architecture

### 2.1 ACPI Tables (`EFI/OC/ACPI/`)
Prebuilt / SSDTTime compiled `.aml` tables according to Dortania Skylake Desktop spec:
1. `SSDT-PLUG.aml`: Native CPU power management (`PluginType = 1`).
2. `SSDT-EC-USBX.aml`: Embedded controller fake device (`EC`) + USB power delivery properties (`USBX`).

### 2.2 Drivers (`EFI/OC/Drivers/`)
1. `OpenRuntime.efi`: Essential memory fix and runtime services.
2. `OpenHfsPlus.efi` / `HfsPlus.efi`: Fast HFS+ filesystem support for macOS installers.
3. `ResetNvramEntry.efi`: Quick NVRAM reset utility in OpenCore boot picker.

### 2.3 Essential Kexts (`EFI/OC/Kexts/`)
1. **VirtualSMC.kext**: SMC emulator.
   - `SMCProcessor.kext`: CPU temp/frequency monitoring.
   - `SMCSuperIO.kext`: Fan and motherboard sensor monitoring.
2. **Lilu.kext**: Arbitrary kext and process patching engine.
3. **WhateverGreen.kext**: Graphics patching for HD 530.
4. **AppleALC.kext**: Audio patch engine (Layout ID for ALC233: typically `11` or `18`).
5. **IntelMausi.kext**: Native driver for Intel I219-LM Ethernet.
6. **NVMeFix.kext**: Power management and APST fixes for NVMe drives.
7. **USBToolBox.kext** / `UTBMap.kext` (or `USBMap.kext`): Custom port mapping to stay within the 15-port limit and fix sleep/wake.

---

## 3. Configuration (`config.plist`) Blueprint

### 3.1 SMBIOS & PlatformInfo
- **Model**: `iMac17,1` (Skylake Desktop with HD 530 native support) or `iMac18,1` (Kaby Lake Desktop, frequently used for Monterey stability).
- Serial generation via `GenSMBIOS`.

### 3.2 DeviceProperties (iGPU Framebuffer)
- `PciRoot(0x0)/Pci(0x2,0x0)`:
  - `AAPL,ig-platform-id`: `00001219` (Data: `<00 00 12 19>`) — Desktop HD 530 with display output.
  - `framebuffer-patch-enable`: `01000000` (Data: `<01 00 00 00>`).
  - `framebuffer-stolenmem`: `00003001` (19MB) or handled via 64MB BIOS pre-alloc.

### 3.3 Booter & Kernel Quirks
- **Booter**:
  - `AvoidRuntimeDefrag`: `True`
  - `EnableSafeModeSlide`: `True`
  - `EnableWriteUnprotector`: `True`
  - `ProvideCustomSlide`: `True`
  - `SetupVirtualMap`: `True`
  - `RebuildAppleMemoryMap`: `False` (for Skylake with EnableWriteUnprotector)
- **Kernel**:
  - `AppleCpuPmCfgLock`: `False` (if CFG Lock disabled in BIOS, else `True`)
  - `AppleXcpmCfgLock`: `True` (safe fallback for MSR 0xE2 lock on OEM Lenovo BIOS)
  - `PanicNoKextDump`: `True`
  - `PowerTimeoutKernelPanic`: `True`
  - `XhciPortLimit`: `False` (broken on Monterey 11.3+; custom map required)

---

## 4. ThinkCentre BIOS Configuration
- **Disable**:
  - Fast Boot / Fast Startup
  - Secure Boot
  - Serial / COM Port
  - Intel SGX (Software Guard Extensions)
  - CSM / Legacy Boot
  - Wake on LAN
- **Enable**:
  - VT-x (Virtualization)
  - Above 4G Decoding (if present)
  - SATA Mode: AHCI
  - Video Pre-Allocated / DVMT: 64MB or 128MB
  - Boot Mode: UEFI Only

---

## 5. Deployment Workflow & Milestones
1. **Milestone 1**: Build the complete, clean OpenCore EFI folder on Linux/WSL (download official release binaries, ACPI SSDTs, kexts, and construct standard `config.plist`).
2. **Milestone 2**: Generate unique SMBIOS identifiers with `GenSMBIOS`.
3. **Milestone 3**: Create bootable Monterey USB installer (macOS Recovery / Full installer creation guide for Windows/Linux).
4. **Milestone 4**: BIOS setup, installation, and post-install validation (Audio Layout, DisplayPort outputs, USB port mapping).
