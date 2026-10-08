#!/usr/bin/env python3
import plistlib
import os

TEMPLATE_PATH = "/tmp/oc_build/OpenCore/Docs/Sample.plist"
DEST_PATH = "/mnt/d/m910x-hackintosh/EFI/OC/config.plist"

with open(TEMPLATE_PATH, "rb") as f:
    config = plistlib.load(f)

# === 1. ACPI ===
config["ACPI"]["Add"] = [
    {
        "Comment": "Native CPU Power Management for Skylake",
        "Enabled": True,
        "Path": "SSDT-PLUG.aml"
    },
    {
        "Comment": "Fake Embedded Controller & USB Power",
        "Enabled": True,
        "Path": "SSDT-EC-USBX.aml"
    }
]
config["ACPI"]["Delete"] = []
config["ACPI"]["Patch"] = []
for k in config["ACPI"]["Quirks"]:
    config["ACPI"]["Quirks"][k] = False

# === 2. Booter Quirks (Skylake Desktop) ===
bq = config["Booter"]["Quirks"]
for k in bq:
    bq[k] = False
bq["AvoidRuntimeDefrag"] = True
bq["EnableSafeModeSlide"] = True
bq["EnableWriteUnprotector"] = True
bq["ProvideCustomSlide"] = True
bq["SetupVirtualMap"] = True

# === 3. DeviceProperties ===
config["DeviceProperties"]["Add"] = {
    "PciRoot(0x0)/Pci(0x2,0x0)": {
        "AAPL,ig-platform-id": b"\x00\x00\x12\x19",
        "device-id": b"\x12\x19\x00\x00",
        "framebuffer-patch-enable": b"\x01\x00\x00\x00",
        "framebuffer-stolenmem": b"\x00\x00\x30\x01",
        "framebuffer-fbmem": b"\x00\x00\x90\x00",
        "hda-gfx": "onboard-1"
    },
    "PciRoot(0x0)/Pci(0x1f,0x3)": {
        "layout-id": b"\x0b\x00\x00\x00"  # ALC294 Layout ID 11 (0x0B)
    }
}
config["DeviceProperties"]["Delete"] = {}

# === 4. Kernel Add ===
kext_order = [
    ("Lilu.kext", "Contents/MacOS/Lilu", "Contents/Info.plist"),
    ("VirtualSMC.kext", "Contents/MacOS/VirtualSMC", "Contents/Info.plist"),
    ("SMCProcessor.kext", "Contents/MacOS/SMCProcessor", "Contents/Info.plist"),
    ("SMCSuperIO.kext", "Contents/MacOS/SMCSuperIO", "Contents/Info.plist"),
    ("WhateverGreen.kext", "Contents/MacOS/WhateverGreen", "Contents/Info.plist"),
    ("AppleALC.kext", "Contents/MacOS/AppleALC", "Contents/Info.plist"),
    ("IntelMausi.kext", "Contents/MacOS/IntelMausi", "Contents/Info.plist"),
    ("NVMeFix.kext", "Contents/MacOS/NVMeFix", "Contents/Info.plist"),
    ("AirportItlwm.kext", "Contents/MacOS/AirportItlwm", "Contents/Info.plist"),
    ("IntelBluetoothFirmware.kext", "Contents/MacOS/IntelBluetoothFirmware", "Contents/Info.plist"),
    ("IntelBTPatcher.kext", "Contents/MacOS/IntelBTPatcher", "Contents/Info.plist"),
    ("BlueToolFixup.kext", "Contents/MacOS/BlueToolFixup", "Contents/Info.plist"),
    ("USBToolBox.kext", "Contents/MacOS/USBToolBox", "Contents/Info.plist"),
    ("UTBMap.kext", "", "Contents/Info.plist")
]

config["Kernel"]["Add"] = []
for bundle, exec_path, plist_path in kext_order:
    config["Kernel"]["Add"].append({
        "Arch": "x86_64",
        "BundlePath": bundle,
        "Comment": bundle.replace(".kext", ""),
        "Enabled": True,
        "ExecutablePath": exec_path,
        "MaxKernel": "",
        "MinKernel": "",
        "PlistPath": plist_path
    })

# Kernel Quirks
kq = config["Kernel"]["Quirks"]
for k in kq:
    kq[k] = False
kq["AppleXcpmCfgLock"] = True
kq["PanicNoKextDump"] = True
kq["PowerTimeoutKernelPanic"] = True
kq["ProvideCurrentCpuInfo"] = False

# === 5. Misc ===
config["Misc"]["Boot"]["ShowPicker"] = True
config["Misc"]["Boot"]["Timeout"] = 5
config["Misc"]["Boot"]["PickerMode"] = "Builtin"
config["Misc"]["Security"]["Vault"] = "Optional"
config["Misc"]["Security"]["ScanPolicy"] = 0
config["Misc"]["Security"]["SecureBootModel"] = "Default"

# === 6. NVRAM ===
nvram_7c = config["NVRAM"]["Add"]["7C436110-AB2A-4BBB-A880-FE41995C9F82"]
nvram_7c["boot-args"] = "-v keepsyms=1 debug=0x100 alcid=11 -igfxvesa=0"
nvram_7c["prev-lang:kbd"] = b"en-US:0"

# === 7. PlatformInfo ===
config["PlatformInfo"]["Generic"]["SystemProductName"] = "iMac17,1"
config["PlatformInfo"]["Generic"]["SystemSerialNumber"] = "C02SG0G5GG7L"
config["PlatformInfo"]["Generic"]["MLB"] = "C02641300GUF6511M"
config["PlatformInfo"]["Generic"]["SystemUUID"] = "6D4C63E4-0E7C-4C8E-98BF-78D7AC283B41"
config["PlatformInfo"]["Generic"]["ROM"] = b"\x17\xaa\x31\x0c\x80\x86"

# === 8. Drivers ===
config["UEFI"]["Drivers"] = [
    {
        "Arguments": "",
        "Comment": "Runtime Memory Driver",
        "Enabled": True,
        "LoadEarly": False,
        "Path": "OpenRuntime.efi"
    },
    {
        "Arguments": "",
        "Comment": "HFS+ Filesystem Driver",
        "Enabled": True,
        "LoadEarly": False,
        "Path": "OpenHfsPlus.efi"
    },
    {
        "Arguments": "",
        "Comment": "NVRAM Reset",
        "Enabled": True,
        "LoadEarly": False,
        "Path": "ResetNvramEntry.efi"
    }
]

# Write out config.plist
with open(DEST_PATH, "wb") as f:
    plistlib.dump(config, f)

print(f"Generated {DEST_PATH} successfully!")
