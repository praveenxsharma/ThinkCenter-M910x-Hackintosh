#!/bin/bash
set -euo pipefail

WORKDIR="/mnt/d/m910x-hackintosh"
KEXTDIR="$WORKDIR/EFI/OC/Kexts"
TMPDIR="/tmp/kext_build"
mkdir -p "$TMPDIR" "$KEXTDIR"

get_url() {
    local repo="$1"
    local pat="$2"
    curl -s "https://api.github.com/repos/$repo/releases/latest" | grep -o 'https://github.com/[^"]*RELEASE\.zip' | grep -i "$pat" | head -n1
}

fetch_zip() {
    local url="$1"
    local out="$2"
    echo "Downloading $out from $url..."
    curl -sL "$url" -o "$TMPDIR/$out"
    unzip -q -o "$TMPDIR/$out" -d "$TMPDIR/${out%.zip}"
}

echo "=== Downloading Kexts ==="

# Lilu
fetch_zip "https://github.com/acidanthera/Lilu/releases/download/1.7.2/Lilu-1.7.2-RELEASE.zip" "Lilu.zip"
cp -r "$TMPDIR/Lilu/Lilu.kext" "$KEXTDIR/"

# VirtualSMC
fetch_zip "https://github.com/acidanthera/VirtualSMC/releases/download/1.3.7/VirtualSMC-1.3.7-RELEASE.zip" "VirtualSMC.zip"
cp -r "$TMPDIR/VirtualSMC/Kexts/VirtualSMC.kext" "$KEXTDIR/"
cp -r "$TMPDIR/VirtualSMC/Kexts/SMCProcessor.kext" "$KEXTDIR/"
cp -r "$TMPDIR/VirtualSMC/Kexts/SMCSuperIO.kext" "$KEXTDIR/"

# WhateverGreen
fetch_zip "https://github.com/acidanthera/WhateverGreen/releases/download/1.7.1/WhateverGreen-1.7.1-RELEASE.zip" "WhateverGreen.zip"
cp -r "$TMPDIR/WhateverGreen/WhateverGreen.kext" "$KEXTDIR/"

# AppleALC
fetch_zip "https://github.com/acidanthera/AppleALC/releases/download/1.9.6/AppleALC-1.9.6-RELEASE.zip" "AppleALC.zip"
cp -r "$TMPDIR/AppleALC/AppleALC.kext" "$KEXTDIR/"

# IntelMausi
fetch_zip "https://github.com/acidanthera/IntelMausi/releases/download/1.0.8/IntelMausi-1.0.8-RELEASE.zip" "IntelMausi.zip"
cp -r "$TMPDIR/IntelMausi/IntelMausi.kext" "$KEXTDIR/"

# NVMeFix
fetch_zip "https://github.com/acidanthera/NVMeFix/releases/download/1.1.2/NVMeFix-1.1.2-RELEASE.zip" "NVMeFix.zip"
cp -r "$TMPDIR/NVMeFix/NVMeFix.kext" "$KEXTDIR/"

# BrcmPatchRAM (for BlueToolFixup)
fetch_zip "https://github.com/acidanthera/BrcmPatchRAM/releases/download/2.7.3/BrcmPatchRAM-2.7.3-RELEASE.zip" "BrcmPatchRAM.zip"
cp -r "$TMPDIR/BrcmPatchRAM/BlueToolFixup.kext" "$KEXTDIR/"

# AirportItlwm (Monterey)
fetch_zip "https://github.com/OpenIntelWireless/itlwm/releases/download/v2.3.0/AirportItlwm_v2.3.0_stable_Monterey.kext.zip" "AirportItlwm.zip"
cp -r "$TMPDIR/AirportItlwm/AirportItlwm.kext" "$KEXTDIR/"

# IntelBluetoothFirmware
fetch_zip "https://github.com/OpenIntelWireless/IntelBluetoothFirmware/releases/download/v2.5.0/IntelBluetoothFirmware-v2.5.0.zip" "IntelBluetoothFirmware.zip"
cp -r "$TMPDIR/IntelBluetoothFirmware/IntelBluetoothFirmware.kext" "$KEXTDIR/"
cp -r "$TMPDIR/IntelBluetoothFirmware/IntelBTPatcher.kext" "$KEXTDIR/"

# USBToolBox
fetch_zip "https://github.com/USBToolBox/kext/releases/download/1.1.1/USBToolBox-1.1.1-RELEASE.zip" "USBToolBox.zip"
cp -r "$TMPDIR/USBToolBox/USBToolBox.kext" "$KEXTDIR/"

echo "Generating standard ThinkCentre M910x UTBMap.kext..."
mkdir -p "$KEXTDIR/UTBMap.kext/Contents"
cat << 'PLIST' > "$KEXTDIR/UTBMap.kext/Contents/Info.plist"
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
	<key>CFBundleIdentifier</key>
	<string>com.USBToolBox.UTBMap</string>
	<key>CFBundleInfoDictionaryVersion</key>
	<string>6.0</string>
	<key>CFBundleName</key>
	<string>UTBMap</string>
	<key>CFBundlePackageType</key>
	<string>KEXT</string>
	<key>CFBundleShortVersionString</key>
	<string>1.0.0</string>
	<key>CFBundleSignature</key>
	<string>????</string>
	<key>CFBundleVersion</key>
	<string>1.0.0</string>
	<key>IOKitPersonalities</key>
	<dict>
		<key>XHC</key>
		<dict>
			<key>CFBundleIdentifier</key>
			<string>com.USBToolBox.USBToolBox</string>
			<key>IOClass</key>
			<string>UTBMap</string>
			<key>IOMatchCategory</key>
			<string>UTBMap</string>
			<key>IONameMatch</key>
			<string>XHC</string>
			<key>IOProviderClass</key>
			<string>AppleUSBXHCIPCI</string>
			<key>IOResourceMatch</key>
			<string>IOKit</string>
			<key>ports</key>
			<dict>
				<key>HS01</key>
				<dict>
					<key>name</key>
					<string>HS01</string>
					<key>port</key>
					<data>AQAAAA==</data>
					<key>type</key>
					<integer>3</integer>
				</dict>
				<key>HS02</key>
				<dict>
					<key>name</key>
					<string>HS02</string>
					<key>port</key>
					<data>AgAAAA==</data>
					<key>type</key>
					<integer>3</integer>
				</dict>
				<key>HS03</key>
				<dict>
					<key>name</key>
					<string>HS03</string>
					<key>port</key>
					<data>AwAAAA==</data>
					<key>type</key>
					<integer>3</integer>
				</dict>
				<key>HS04</key>
				<dict>
					<key>name</key>
					<string>HS04</string>
					<key>port</key>
					<data>BAAAAA==</data>
					<key>type</key>
					<integer>3</integer>
				</dict>
				<key>HS05</key>
				<dict>
					<key>name</key>
					<string>HS05</string>
					<key>port</key>
					<data>BQAAAA==</data>
					<key>type</key>
					<integer>3</integer>
				</dict>
				<key>HS06</key>
				<dict>
					<key>name</key>
					<string>HS06</string>
					<key>port</key>
					<data>BgAAAA==</data>
					<key>type</key>
					<integer>3</integer>
				</dict>
				<key>HS07</key>
				<dict>
					<key>name</key>
					<string>HS07</string>
					<key>port</key>
					<data>BwAAAA==</data>
					<key>type</key>
					<integer>255</integer>
				</dict>
				<key>SS01</key>
				<dict>
					<key>name</key>
					<string>SS01</string>
					<key>port</key>
					<data>EQAAAA==</data>
					<key>type</key>
					<integer>3</integer>
				</dict>
				<key>SS02</key>
				<dict>
					<key>name</key>
					<string>SS02</string>
					<key>port</key>
					<data>EgAAAA==</data>
					<key>type</key>
					<integer>3</integer>
				</dict>
				<key>SS03</key>
				<dict>
					<key>name</key>
					<string>SS03</string>
					<key>port</key>
					<data>EwAAAA==</data>
					<key>type</key>
					<integer>3</integer>
				</dict>
				<key>SS04</key>
				<dict>
					<key>name</key>
					<string>SS04</string>
					<key>port</key>
					<data>FAAAAA==</data>
					<key>type</key>
					<integer>3</integer>
				</dict>
			</dict>
		</dict>
	</dict>
	<key>OSBundleLibraries</key>
	<dict>
		<key>com.USBToolBox.USBToolBox</key>
		<string>1.0.0</string>
	</dict>
	<key>OSBundleRequired</key>
	<string>Root</string>
</dict>
</plist>
PLIST

echo "SUCCESS: All kexts installed."
