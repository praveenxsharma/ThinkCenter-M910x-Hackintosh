#!/usr/bin/env python3
import os
import shutil
import urllib.request
import zipfile

TMPDIR = "/tmp/kext_build"
KEXTDIR = "/mnt/d/m910x-hackintosh/EFI/OC/Kexts"
os.makedirs(TMPDIR, exist_ok=True)
os.makedirs(KEXTDIR, exist_ok=True)

downloads = [
    ("https://github.com/acidanthera/Lilu/releases/download/1.7.2/Lilu-1.7.2-RELEASE.zip", "Lilu.zip", ["Lilu.kext"]),
    ("https://github.com/acidanthera/VirtualSMC/releases/download/1.3.7/VirtualSMC-1.3.7-RELEASE.zip", "VirtualSMC.zip", ["Kexts/VirtualSMC.kext", "Kexts/SMCProcessor.kext", "Kexts/SMCSuperIO.kext"]),
    ("https://github.com/acidanthera/WhateverGreen/releases/download/1.7.1/WhateverGreen-1.7.1-RELEASE.zip", "WhateverGreen.zip", ["WhateverGreen.kext"]),
    ("https://github.com/acidanthera/AppleALC/releases/download/1.9.6/AppleALC-1.9.6-RELEASE.zip", "AppleALC.zip", ["AppleALC.kext"]),
    ("https://github.com/acidanthera/IntelMausi/releases/download/1.0.8/IntelMausi-1.0.8-RELEASE.zip", "IntelMausi.zip", ["IntelMausi.kext"]),
    ("https://github.com/acidanthera/NVMeFix/releases/download/1.1.2/NVMeFix-1.1.2-RELEASE.zip", "NVMeFix.zip", ["NVMeFix.kext"]),
    ("https://github.com/acidanthera/BrcmPatchRAM/releases/download/2.7.2/BrcmPatchRAM-2.7.2-RELEASE.zip", "BrcmPatchRAM.zip", ["BlueToolFixup.kext"]),
    ("https://github.com/OpenIntelWireless/itlwm/releases/download/v2.3.0/AirportItlwm_v2.3.0_stable_Monterey.kext.zip", "AirportItlwm.zip", ["AirportItlwm.kext"]),
    ("https://github.com/OpenIntelWireless/IntelBluetoothFirmware/releases/download/v2.4.0/IntelBluetooth-v2.4.0.zip", "IntelBluetoothFirmware.zip", ["IntelBluetoothFirmware.kext", "IntelBTPatcher.kext"]),
    ("https://github.com/USBToolBox/kext/releases/download/1.1.1/USBToolBox-1.1.1-RELEASE.zip", "USBToolBox.zip", ["USBToolBox.kext"]),
]

headers = {"User-Agent": "Mozilla/5.0"}

for url, filename, targets in downloads:
    zip_path = os.path.join(TMPDIR, filename)
    extract_folder = os.path.join(TMPDIR, filename.replace(".zip", ""))
    
    if not os.path.exists(zip_path) or os.path.getsize(zip_path) == 0:
        print(f"Downloading {filename} from {url}...")
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = resp.read()
            with open(zip_path, "wb") as f:
                f.write(data)
        print(f"Downloaded {filename} ({len(data)} bytes)")
    else:
        print(f"Already cached: {filename}")

    if not os.path.exists(extract_folder):
        with zipfile.ZipFile(zip_path, "r") as zf:
            zf.extractall(extract_folder)

    for target in targets:
        src = os.path.join(extract_folder, target)
        dest = os.path.join(KEXTDIR, os.path.basename(target))
        if os.path.exists(src):
            if os.path.exists(dest):
                shutil.rmtree(dest)
            shutil.copytree(src, dest)
            print(f"Installed {os.path.basename(target)}")
        else:
            print(f"WARNING: {src} not found in {extract_folder}")

print("Python download and extraction complete!")
