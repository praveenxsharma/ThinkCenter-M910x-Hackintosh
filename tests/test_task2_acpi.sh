#!/bin/bash
set -e

ACPI_DIR="/mnt/d/m910x-hackintosh/EFI/OC/ACPI"

echo "Verifying Task 2: ACPI AML Tables..."

test -f "$ACPI_DIR/SSDT-PLUG.aml" || { echo "FAIL: SSDT-PLUG.aml missing"; exit 1; }
test -f "$ACPI_DIR/SSDT-EC-USBX.aml" || { echo "FAIL: SSDT-EC-USBX.aml missing"; exit 1; }

# Verify AML Magic Header: 'AML ' (0x41 0x4D 0x4C 0x20 in hex or AMLP / DSDT / SSDT)
for f in "$ACPI_DIR/SSDT-PLUG.aml" "$ACPI_DIR/SSDT-EC-USBX.aml"; do
    header=$(head -c 4 "$f")
    if [ "$header" != "SSDT" ] && [ "$header" != "DSDT" ]; then
        echo "FAIL: $f does not have valid ACPI AML header (found '$header')"
        exit 1
    fi
    echo "Verified $f (Header: $header, Size: $(stat -c%s "$f") bytes)"
done

echo "PASS: All ACPI SSDT tables are valid."
