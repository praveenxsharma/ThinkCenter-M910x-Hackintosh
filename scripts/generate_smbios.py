#!/usr/bin/env python3
import plistlib
import uuid
import random
import string
import os

CONFIG_PATH = "/mnt/d/m910x-hackintosh/EFI/OC/config.plist"

def random_string(length, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(length))

def generate_smbios():
    # Model: iMac17,1
    # Serial format: 12 chars: [Production Plant 3][Year/Week 2][Unique 3][Model ID 4] (e.g. C02SG0G5GG7L)
    serial = f"C02{random_string(2, '0123456789')}{random_string(3)}{'GG7L'}"
    # MLB: 17 chars: Serial + 5 chars
    mlb = f"C02{random_string(14)}"
    sys_uuid = str(uuid.uuid4()).upper()
    
    print(f"Generated SMBIOS (iMac17,1):")
    print(f"  SerialNumber: {serial}")
    print(f"  MLB:          {mlb}")
    print(f"  UUID:         {sys_uuid}")

    with open(CONFIG_PATH, "rb") as f:
        config = plistlib.load(f)

    config["PlatformInfo"]["Generic"]["SystemProductName"] = "iMac17,1"
    config["PlatformInfo"]["Generic"]["SystemSerialNumber"] = serial
    config["PlatformInfo"]["Generic"]["MLB"] = mlb
    config["PlatformInfo"]["Generic"]["SystemUUID"] = sys_uuid
    
    with open(CONFIG_PATH, "wb") as f:
        plistlib.dump(config, f)
    
    print("Updated config.plist with fresh SMBIOS!")

if __name__ == "__main__":
    generate_smbios()
