#!/bin/bash
set -euo pipefail

WORKDIR="/mnt/d/m910x-hackintosh"
TMPDIR="/tmp/oc_build"
mkdir -p "$TMPDIR" "$WORKDIR/EFI/BOOT" "$WORKDIR/EFI/OC/Drivers" "$WORKDIR/EFI/OC/Kexts" "$WORKDIR/EFI/OC/ACPI" "$WORKDIR/EFI/OC/Tools"

echo "[1/3] Fetching OpenCorePkg RELEASE..."
OC_URL=$(curl -s https://api.github.com/repos/acidanthera/OpenCorePkg/releases/latest | grep "browser_download_url.*RELEASE.zip" | head -n1 | cut -d '"' -f 4)
if [ -z "$OC_URL" ]; then
    echo "Fallback to direct tag lookup"
    OC_URL="https://github.com/acidanthera/OpenCorePkg/releases/download/1.0.3/OpenCore-1.0.3-RELEASE.zip"
fi

echo "Downloading OpenCore from $OC_URL..."
curl -sL "$OC_URL" -o "$TMPDIR/OpenCore.zip"
unzip -q -o "$TMPDIR/OpenCore.zip" -d "$TMPDIR/OpenCore"

# Copy EFI base binaries
cp "$TMPDIR/OpenCore/X64/EFI/BOOT/BOOTx64.efi" "$WORKDIR/EFI/BOOT/"
cp "$TMPDIR/OpenCore/X64/EFI/OC/OpenCore.efi" "$WORKDIR/EFI/OC/"
cp "$TMPDIR/OpenCore/X64/EFI/OC/Drivers/OpenRuntime.efi" "$WORKDIR/EFI/OC/Drivers/"
cp "$TMPDIR/OpenCore/X64/EFI/OC/Drivers/ResetNvramEntry.efi" "$WORKDIR/EFI/OC/Drivers/"

echo "[2/3] Fetching OpenHfsPlus.efi..."
HFS_URL="https://github.com/acidanthera/OcBinaryData/raw/master/Drivers/OpenHfsPlus.efi"
curl -sL "$HFS_URL" -o "$WORKDIR/EFI/OC/Drivers/OpenHfsPlus.efi"

echo "[3/3] Base binaries deployed successfully."
