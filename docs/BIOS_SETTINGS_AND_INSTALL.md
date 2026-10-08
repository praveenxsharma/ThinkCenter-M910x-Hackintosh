# ThinkCentre M910x BIOS Setup & Installation Checklist

## 1. Lenovo ThinkCentre M910x BIOS Configuration

Press **F1** during startup to enter Lenovo BIOS Setup:

### Devices:
- **ATA Drive Setup**: SATA Controller = `Enabled`, Configure SATA as = `AHCI`
- **Video Setup**: Select Active Video = `IGD` (Integrated Graphics)
  - Pre-Allocated Memory (DVMT) = `64MB` (or `128MB`)
- **Audio Setup**: Internal Speaker = `Enabled`
- **Network Setup**: Boot Agent = `Disabled`
- **Serial Port**: COM1 = `Disabled` (Important to prevent macOS boot stalls)

### Security:
- **Secure Boot**: `Disabled` (MANDATORY)
- **Intel SGX (Software Guard Extensions)**: `Disabled`
- **Device Guard**: `Disabled`

### Startup:
- **CSM (Compatibility Support Module)**: `Disabled` (Pure UEFI Boot)
- **Boot Mode**: `UEFI Only`
- **Quick Boot / Fast Boot**: `Disabled`

---

## 2. Bootable Monterey USB Creation

You can prepare the USB stick directly on **Ubuntu** or **Windows**:

### Option A: From Ubuntu Linux (Recommended & Fast)
1. Format a USB flash drive (16GB+) as GPT with FAT32:
   ```bash
   sudo parted /dev/sdX --script mklabel gpt mkpart primary fat32 1MiB 100%
   sudo mkfs.vfat -F32 /dev/sdX1 -n "OPENCORE"
   ```
2. Mount the USB and copy the complete `EFI` folder to the root:
   ```bash
   sudo mount /dev/sdX1 /mnt/usb
   sudo cp -r /mnt/d/m910x-hackintosh/EFI /mnt/usb/
   ```
3. Fetch macOS 12 Monterey Recovery Image:
   ```bash
   mkdir -p /mnt/usb/com.apple.recovery.boot
   python3 /home/itachi/opencore-guide/OpenCore-Install-Guide/network-recovery/macrecovery.py -b Mac-FFE5EF870D7BA81A -m 00000000000000000 download
   cp BaseSystem.dmg BaseSystem.chunklist /mnt/usb/com.apple.recovery.boot/
   sudo umount /mnt/usb
   ```

### Option B: Windows (via Rufus or gibMacOS)
1. Copy `/mnt/d/m910x-hackintosh/EFI` to your Windows desktop (`D:\m910x-hackintosh\EFI`).
2. Copy the `EFI` folder to the EFI partition of your USB drive.

---

## 3. Installation Steps
1. Insert the USB drive into a rear USB port on the ThinkCentre M910x.
2. Power on and press **F12** to open the Boot Menu.
3. Select your UEFI USB drive.
4. OpenCore boot picker will appear:
   - Select **macOS Base System (External)** or **Install macOS Monterey**.
5. Once inside macOS Recovery:
   - Open **Disk Utility**.
   - Click *View* -> *Show All Devices*.
   - Select your internal 512GB SSD (`Matrix 512GB`) and click **Erase**:
     - Name: `Macintosh HD`
     - Format: `APFS`
     - Scheme: `GUID Partition Map`
   - Quit Disk Utility and select **Reinstall macOS Monterey**.
6. The system will reboot 3-4 times. Always select the `macOS Installer` or `Macintosh HD` entry in the OpenCore boot picker until setup assistant loads.

---

## 4. Post-Installation
1. Mount the internal drive's EFI partition using OpenCore Auxiliary Tools or `diskutil mount disk0s1`.
2. Copy the `EFI` folder from your USB drive to the internal drive's EFI partition.
3. Remove the USB stick and boot directly from the internal SSD!
