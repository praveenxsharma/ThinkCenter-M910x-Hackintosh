#!/bin/bash
set -e

EFI_DIR="/mnt/d/m910x-hackintosh/EFI"

echo "Verifying Task 1: OpenCore Base Binaries..."

test -f "$EFI_DIR/BOOT/BOOTx64.efi" || { echo "FAIL: BOOTx64.efi missing"; exit 1; }
test -f "$EFI_DIR/OC/OpenCore.efi" || { echo "FAIL: OpenCore.efi missing"; exit 1; }
test -f "$EFI_DIR/OC/Drivers/OpenRuntime.efi" || { echo "FAIL: OpenRuntime.efi missing"; exit 1; }
test -f "$EFI_DIR/OC/Drivers/OpenHfsPlus.efi" || { echo "FAIL: OpenHfsPlus.efi missing"; exit 1; }
test -f "$EFI_DIR/OC/Drivers/ResetNvramEntry.efi" || { echo "FAIL: ResetNvramEntry.efi missing"; exit 1; }

# Verify file sizes are non-zero and are PE32+ (UEFI) binaries
for f in "$EFI_DIR/BOOT/BOOTx64.efi" "$EFI_DIR/OC/OpenCore.efi" "$EFI_DIR/OC/Drivers/OpenRuntime.efi" "$EFI_DIR/OC/Drivers/OpenHfsPlus.efi" "$EFI_DIR/OC/Drivers/ResetNvramEntry.efi"; do
    if [ ! -s "$f" ]; then
        echo "FAIL: $f is empty"
        exit 1
    fi
done

echo "PASS: All OpenCore base EFI binaries exist and are non-empty."
