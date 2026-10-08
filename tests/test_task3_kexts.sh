#!/bin/bash
set -e

KEXT_DIR="/mnt/d/m910x-hackintosh/EFI/OC/Kexts"

echo "Verifying Task 3: Kext Bundles..."

REQUIRED_KEXTS=(
    "Lilu.kext"
    "VirtualSMC.kext"
    "SMCProcessor.kext"
    "SMCSuperIO.kext"
    "WhateverGreen.kext"
    "AppleALC.kext"
    "IntelMausi.kext"
    "NVMeFix.kext"
    "AirportItlwm.kext"
    "IntelBluetoothFirmware.kext"
    "IntelBTPatcher.kext"
    "BlueToolFixup.kext"
    "USBToolBox.kext"
    "UTBMap.kext"
)

for k in "${REQUIRED_KEXTS[@]}"; do
    if [ ! -d "$KEXT_DIR/$k" ]; then
        echo "FAIL: Missing kext directory $k"
        exit 1
    fi
    if [ ! -f "$KEXT_DIR/$k/Contents/Info.plist" ]; then
        echo "FAIL: Missing Info.plist inside $k"
        exit 1
    fi
    echo "Verified $k"
done

echo "PASS: All required hardware kexts exist with valid Info.plist files."
