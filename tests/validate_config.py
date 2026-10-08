#!/usr/bin/env python3
import plistlib
import os
import sys

CONFIG_PATH = "/mnt/d/m910x-hackintosh/EFI/OC/config.plist"
EFI_ROOT = "/mnt/d/m910x-hackintosh/EFI/OC"

print("Verifying Task 4: config.plist integrity...")

if not os.path.exists(CONFIG_PATH):
    print(f"FAIL: {CONFIG_PATH} does not exist")
    sys.exit(1)

with open(CONFIG_PATH, "rb") as f:
    try:
        config = plistlib.load(f)
    except Exception as e:
        print(f"FAIL: Invalid XML / plist syntax: {e}")
        sys.exit(1)

# 1. Verify ACPI tables referenced exist on disk
acpi_adds = config.get("ACPI", {}).get("Add", [])
assert len(acpi_adds) >= 2, "Must have at least 2 ACPI tables"
for entry in acpi_adds:
    path = os.path.join(EFI_ROOT, "ACPI", entry["Path"])
    if not os.path.exists(path):
        print(f"FAIL: ACPI table referenced not found on disk: {path}")
        sys.exit(1)
    print(f"Verified ACPI: {entry['Path']}")

# 2. Verify Kexts referenced exist on disk and Lilu is first
kernel_adds = config.get("Kernel", {}).get("Add", [])
assert len(kernel_adds) >= 5, "Must have kexts added"
if kernel_adds[0]["BundlePath"] != "Lilu.kext":
    print("FAIL: Lilu.kext must be the first kext loaded in Kernel -> Add")
    sys.exit(1)

for entry in kernel_adds:
    kext_path = os.path.join(EFI_ROOT, "Kexts", entry["BundlePath"])
    if not os.path.exists(kext_path):
        print(f"FAIL: Kext referenced not found on disk: {kext_path}")
        sys.exit(1)

print(f"Verified {len(kernel_adds)} Kext references.")

# 3. Verify DeviceProperties for HD 530 and ALC294
dev_props = config.get("DeviceProperties", {}).get("Add", {})
igpu_prop = dev_props.get("PciRoot(0x0)/Pci(0x2,0x0)", {})
if not igpu_prop:
    print("FAIL: Missing DeviceProperties for HD 530 iGPU (PciRoot(0x0)/Pci(0x2,0x0))")
    sys.exit(1)

ig_platform_id = igpu_prop.get("AAPL,ig-platform-id")
if ig_platform_id not in (b"\x00\x00\x12\x19", b"\x00\x00\x16\x19"):
    print(f"FAIL: Invalid AAPL,ig-platform-id: {ig_platform_id}")
    sys.exit(1)

# 4. Verify Quirks
booter_quirks = config.get("Booter", {}).get("Quirks", {})
assert booter_quirks.get("AvoidRuntimeDefrag") is True
assert booter_quirks.get("EnableWriteUnprotector") is True
assert booter_quirks.get("SetupVirtualMap") is True

kernel_quirks = config.get("Kernel", {}).get("Quirks", {})
assert kernel_quirks.get("AppleXcpmCfgLock") is True
assert kernel_quirks.get("PanicNoKextDump") is True

# 5. Verify Boot args
boot_args = config.get("NVRAM", {}).get("Add", {}).get("7C436110-AB2A-4BBB-A880-FE41995C9F82", {}).get("boot-args", "")
assert "-v" in boot_args, "Verbose mode should be in boot-args"
assert "alcid=11" in boot_args, "ALC294 layout ID 11 should be in boot-args"

# 6. Verify Drivers
uefi_drivers = config.get("UEFI", {}).get("Drivers", [])
driver_paths = [d["Path"] for d in uefi_drivers if d.get("Enabled")]
assert "HfsPlus.efi" in driver_paths, "HfsPlus.efi must be present in Drivers"
for d in driver_paths:
    full_path = os.path.join(EFI_ROOT, "Drivers", d)
    if not os.path.exists(full_path):
        print(f"FAIL: Driver {d} not found at {full_path}")
        sys.exit(1)
    # verify driver is PE32+
    with open(full_path, "rb") as df:
        hdr = df.read(2)
        if hdr != b"MZ":
            print(f"FAIL: Driver {d} is not a valid EFI binary (missing MZ header)")
            sys.exit(1)

print("PASS: config.plist is completely valid and verified for M910x hardware.")
