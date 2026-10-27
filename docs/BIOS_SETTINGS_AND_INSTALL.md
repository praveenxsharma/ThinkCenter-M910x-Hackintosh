# Lenovo ThinkCentre M910x Hackintosh: BIOS Setup & Installation Guide

Complete field-tested setup and installation guide for the **Lenovo ThinkCentre M910x Tiny** running **macOS 12 Monterey (12.7.6)** with OpenCore 1.0.x.

---

## 1. Verified Hardware Specifications
- **Model**: Lenovo ThinkCentre M910x Tiny (Machine Type: 10MY / 10N0)
- **BIOS Tested**: `M1AKT5AA`
- **CPU**: Intel Core i5-6500T (Skylake, 4 Cores, 2.50GHz base / 3.10GHz turbo, 35W TDP)
- **iGPU**: Intel HD Graphics 530 (`[8086:1912]`, rev 06) — 1536 MB VRAM with Metal / QE-CI
- **Audio Codec**: Realtek ALC294 (`[10ec:0294]`) + Intel Skylake HDMI Audio
- **Ethernet**: Intel I219-LM Gigabit Ethernet (`[8086:15b7]`)
- **Wi-Fi / BT**: Intel Dual Band Wireless-AC 8265 (`[8086:24fd]`) / Bluetooth (`[8087:0a2b]`)
- **RAM**: 8GB DDR4 SO-DIMM (Expandable to 32GB)
- **Storage**: 512GB SATA / NVMe SSD

---

## 2. Comprehensive BIOS Configuration

Press **F1** repeatedly during system startup to enter the **Lenovo BIOS Setup Utility**.

### [Devices] Menu
| Setting | Recommended Value | Reason / Impact |
| :--- | :--- | :--- |
| **ATA Drive Setup -> SATA Controller** | `Enabled` | Allows internal SSD/HDD drives to function |
| **ATA Drive Setup -> Configure SATA as** | `AHCI` | **Mandatory**; macOS does not support IDE/RAID |
| **Video Setup -> Select Active Video** | `IGD` | Forces Intel HD 530 as primary display device |
| **Video Setup -> Pre-Allocated Memory (DVMT)** | `64MB` (or `128MB`) | **Mandatory**; required by WhateverGreen for hardware acceleration |
| **Audio Setup -> Internal Speaker** | `Enabled` | Enables the motherboard mono speaker |
| **Network Setup -> Onboard Ethernet Controller** | **`Enabled`** | **CRITICAL**; if disabled, the I219-LM chip receives no power, LEDs stay dark, and macOS detects no network card |
| **Network Setup -> Boot Agent** | `Disabled` | Prevents slow PXE network boot timeouts |
| **Serial Port Setup** *(if visible)* | `Disabled` | Prevents early macOS boot hangs (hidden if no COM bracket installed) |
| **USB Setup -> USB Support** | `Enabled` | Enables USB 3.0 / 2.0 controller |

### [Advanced] Menu -> [CPU Setup]
| Setting | Recommended Value | Reason / Impact |
| :--- | :--- | :--- |
| **Intel (R) Virtualization Technology (VT-x)** | `Enabled` | Required for macOS hypervisor, Docker, and virtualization |
| **VT-d** | **`Disabled`** | Prevents DMA / I/O mapper kernel panics (paired with `DisableIoMapper = True` in OpenCore) |
| **EIST Support** | `Enabled` | Enhanced Intel SpeedStep for CPU power management |
| **Turbo Mode** | `Enabled` | Allows CPU to boost up to 3.10GHz |
| **C State Support** | `Enabled` (`C1C3C6C7C8`) | Allows proper CPU idle sleep states |
| **Core Multi-Processing** | `Enabled` | Enables all 4 CPU physical cores |

### [Security] Menu
| Setting | Recommended Value | Reason / Impact |
| :--- | :--- | :--- |
| **Secure Boot** | **`Disabled`** | **Mandatory**; UEFI signature check blocks non-Apple bootloaders |
| **Intel SGX (Software Guard Extensions)** | `Disabled` | Not supported by macOS; causes sleep/wake issues |
| **Device Guard** | `Disabled` | Blocks custom boot partitions if enabled |
| **Smart USB Protection** | `Disabled` | If enabled, blocks USB storage devices |

### [Startup] Menu
| Setting | Recommended Value | Reason / Impact |
| :--- | :--- | :--- |
| **CSM (Compatibility Support Module)** | **`Disabled`** | **Mandatory**; forces clean pure UEFI GOP framebuffer |
| **Boot Mode** | `UEFI Only` | Blocks legacy MBR boot code |
| **Boot Up Num-Lock Status** | `On` / `Off` (User Preference) | No effect on macOS |
| **Startup Device Menu Prompt** | `Enabled` | Displays F12 boot option on startup |

Press **F10** to save settings and exit.

---

## 3. Display, Video Cable, and Port Requirements

> ⚠️ **IMPORTANT: Do NOT use an analog VGA cable!**  
> macOS removed analog VGA graphics acceleration years ago. If you connect using a VGA cable, macOS will only boot in unaccelerated VESA mode (5MB VRAM, severe stuttering/lag), and attempting to enable hardware acceleration will result in an instant black screen upon loading the desktop.

- **Recommended Cable**: Use a **DisplayPort to HDMI cable** (or active DP-to-HDMI adapter) plugged into your monitor's HDMI port.
- **Alternative**: Direct **DisplayPort to DisplayPort cable** if your monitor has a DP port.
- **OpenCore Framebuffer Mapping**: In `config.plist`, `PciRoot(0x0)/Pci(0x2,0x0)` is patched with:
  - `AAPL,ig-platform-id`: `00001219` (Data: `<00 00 12 19>`)
  - `device-id`: `12190000` (Data: `<12 19 00 00>`)
  - `framebuffer-con0-type`, `con1-type`, `con2-type`: `<00 08 00 00>` (Forces HDMI signaling through DisplayPort adapters)
  - `enable-hdmi20`: `<01 00 00 00>`
  - Boot-arg: `igfxonln=1` (Forces display signals to stay awake)

---

## 4. Audio Configuration (ALC294)

The ThinkCentre M910x Tiny features the **Realtek ALC294** codec.
- **Working Layout ID**: **`12`** (`alcid=12` / hex `<0c 00 00 00>`).
  - *Why not Layout 11?* Layout 11 detects jack insertion ("Headphones" appears in Sound settings), but its DAC/amplifier route is disconnected on Lenovo Tiny boards, producing no audio.
  - Layout 12 correctly routes both the **internal motherboard speaker** and the **front 3.5mm combo headphone/headset jack**.
- **Physical Connection**: Plug external speakers or headphones into the **front headphone jack** (headphone icon), not the microphone jack. If the speaker is USB-powered, ensure its USB cable is plugged into a USB port for 5V power.

---

## 5. Network Configuration

### Ethernet (Intel I219-LM)
- Driven by `IntelMausi.kext` (v1.0.8+).
- Requires `DisableIoMapper = True` in `config.plist` (and `VT-d = Disabled` in BIOS).
- Marked with `built-in = <01>` in `DeviceProperties -> PciRoot(0x0)/Pci(0x1f,0x6)`.
- If the interface order is scrambled on first boot, reset network interfaces in macOS Terminal:
  ```bash
  sudo rm -f /Library/Preferences/SystemConfiguration/NetworkInterfaces.plist
  sudo rm -f /Library/Preferences/SystemConfiguration/preferences.plist
  ```

### Wi-Fi & Bluetooth (Intel AC 8265)
- **Wi-Fi**: Driven by `AirportItlwm.kext` (Monterey build v2.3.0). Native Apple Wi-Fi menu bar integration, no external helper apps needed.
- **Bluetooth**: Driven by `IntelBluetoothFirmware.kext` + `IntelBTPatcher.kext` + `BlueToolFixup.kext`.

---

## 6. Creating the Bootable USB Installer

### Option A: From Linux / Ubuntu
1. Format a USB flash drive (16GB+) as GPT with FAT32:
   ```bash
   sudo parted /dev/sdX --script mklabel gpt mkpart primary fat32 1MiB 100%
   sudo mkfs.vfat -F32 /dev/sdX1 -n "OPENCORE"
   ```
2. Mount the USB drive and copy the repository `EFI` directory to the root of the USB:
   ```bash
   sudo mount /dev/sdX1 /mnt/usb
   sudo cp -r /path/to/m910x-hackintosh/EFI /mnt/usb/
   ```
3. Fetch the official macOS 12 Monterey Recovery Image:
   ```bash
   mkdir -p /mnt/usb/com.apple.recovery.boot
   python3 /path/to/m910x-hackintosh/tools/macrecovery.py -b Mac-FFE5EF870D7BA81A -m 00000000000000000 download
   cp BaseSystem.dmg BaseSystem.chunklist /mnt/usb/com.apple.recovery.boot/
   sudo umount /mnt/usb
   ```

### Option B: From Windows
1. Format a USB drive as FAT32 named `OPENCORE`.
2. Copy the `EFI` folder to the root of the USB drive (`E:\EFI`).
3. Download the recovery files using `tools/macrecovery.py` and place them in `E:\com.apple.recovery.boot\`:
   - `BaseSystem.dmg` (~623 MB)
   - `BaseSystem.chunklist`

---

## 7. macOS Installation Walkthrough

1. Insert the USB drive into a **rear USB port** on the ThinkCentre M910x.
2. Power on and press **F12** to open the Boot Device Menu.
3. Select your USB drive (`UEFI: <USB Brand>`).
4. In the OpenCore Boot Menu:
   - Select **`OPENCORE (external) (dmg)`** (or `macOS Base System`).
5. In macOS Recovery:
   - Open **Disk Utility**.
   - Click **View** -> **Show All Devices**.
   - Select the internal SSD (`Matrix 512GB` or your NVMe/SATA SSD) and click **Erase**:
     - **Name**: `Macintosh HD`
     - **Format**: `APFS`
     - **Scheme**: `GUID Partition Map`
   - Close Disk Utility.
6. Click **Reinstall macOS Monterey** and select `Macintosh HD`.
7. The installer will download the full 12.4 GB macOS Monterey system files and restart automatically 2–3 times.
   - At every reboot, select **Macintosh HD** in the OpenCore boot picker until the macOS Welcome / Setup Assistant screen appears.

---

## 8. Post-Installation: Boot from SSD without USB

Once macOS setup is complete:

1. Open **Terminal** in macOS (`Cmd + Space` -> type `Terminal`).
2. Mount the internal SSD's hidden EFI partition:
   ```bash
   sudo diskutil mount disk0s1
   ```
3. Copy the verified EFI folder from your USB drive to the internal SSD:
   ```bash
   sudo cp -r /Volumes/OPENCORE/EFI /Volumes/EFI/
   ```
4. Unmount the EFI partition:
   ```bash
   sudo diskutil unmount /Volumes/EFI
   ```
5. Remove the USB flash drive.
6. Reboot (` Menu -> Restart`).

Your ThinkCentre M910x Tiny will now boot macOS Monterey completely standalone from the internal SSD with full graphics acceleration, Ethernet, Wi-Fi, and audio!
