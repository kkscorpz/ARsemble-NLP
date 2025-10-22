import unicodedata
import datetime
import sys
import contextlib
import io
import random
import textwrap
import json
import time
import re
import math
import difflib
from dotenv import load_dotenv

import os
import google.genai as genai

load_dotenv(encoding="utf-8-sig")

GENAI_API_KEY = os.getenv("GOOGLE_API_KEY") or os.getenv("GENAI_API_KEY")

if not GENAI_API_KEY:
    print("⚠️ GENAI API key not found. Set GOOGLE_API_KEY or GENAI_API_KEY in environment (.env or platform settings).")
    client = None
else:
    client = genai.Client(api_key=GENAI_API_KEY)


# -------------------------------
# 📚 Local Component Database (paste your dataset here)
# -------------------------------
data = {
    "gpu": {
        "integrated graphics": {
            "name": "Integrated Graphics (from CPU)",
            "type": "GPU",
                    "vram": "Shared system memory",
                    "clock": "Varies by CPU",
                    "power": "0W (included in CPU power)",
                    "slot": "None (integrated)",
                    "price": "₱0 (included with CPU)",
                    "compatibility": "Works with any compatible motherboard, no additional power required"
        },
        "gtx 750 ti": {
            "name": "NVIDIA GTX 750 Ti",
            "type": "GPU",
                    "vram": "2GB GDDR5",
                    "clock": "~1085 MHz (Boost)",
                    "power": "~60 Watts",
                    "slot": "PCIe 3.0 x16",
                    "price": "₱4,000",
                    "compatibility": "PCIe x16 slot, 300W PSU recommended"
        },
        "rtx 3050": {
            "name": "Gigabyte RTX 3050 EAGLE OC",
            "type": "GPU",
                    "vram": "8GB GDDR6",
                    "clock": "~1777 MHz (Boost)",
                    "power": "~130 Watts",
                    "slot": "PCIe 4.0 x16",
                    "price": "₱12,000",
                    "compatibility": "PCIe x16 slot, 550W PSU, 8-pin power connector"
        },
        "rtx 3060": {
            "name": "MSI RTX 3060",
            "type": "GPU",
                    "vram": "12GB GDDR6",
                    "clock": "~1777 MHz (Boost)",
                    "power": "~170 Watts",
                    "slot": "PCIe 4.0 x16",
                    "price": "₱16,000",
                    "compatibility": "PCIe x16 slot, 550W PSU, 8-pin power connector"
        },
        "rtx 4060": {
            "name": "MSI RTX 4060 GAMING X",
            "type": "GPU",
                    "vram": "8GB GDDR6",
                    "clock": "~2595 MHz (Boost)",
                    "power": "~115 Watts",
                    "slot": "PCIe 4.0 x8",
                    "price": "₱18,000",
                    "compatibility": "PCIe x16 slot, 550W PSU, 8-pin power connector"
        }
    },
    "cpu": {
        "amd ryzen 3 3200g": {
            "name": "AMD Ryzen 3 3200G",
                    "type": "CPU",
                    "socket": "AM4",
                    "cores": "4 Cores / 4 Threads",
                    "clock": "3.6 GHz / 4.0 GHz Boost",
                    "tdp": "65W",
                    "igpu": "Vega 8",
                    "price": "₱4,500",
                    "compatibility": "AM4 Motherboards, DDR4 RAM"
        },
        "amd ryzen 5 3600": {
            "name": "AMD Ryzen 5 3600",
                    "type": "CPU",
                    "socket": "AM4",
                    "cores": "6 Cores / 12 Threads",
                    "clock": "3.6 GHz / 4.2 GHz Boost",
                    "tdp": "65W",
                    "igpu": "None",
                    "price": "₱6,500",
                    "compatibility": "AM4 Motherboards, DDR4 RAM"
        },
        "amd ryzen 5 5600g": {
            "name": "AMD Ryzen 5 5600G",
                    "type": "CPU",
                    "socket": "AM4",
                    "cores": "6 Cores / 12 Threads",
                    "clock": "3.9 GHz / 4.4 GHz Boost",
                    "tdp": "65W",
                    "igpu": "Vega 7",
                    "price": "₱8,500",
                    "compatibility": "AM4 Motherboards, DDR4 RAM"
        },
        "amd ryzen 5 5600x": {
            "name": "AMD Ryzen 5 5600X",
                    "type": "CPU",
                    "socket": "AM4",
                    "cores": "6 Cores / 12 Threads",
                    "clock": "3.7 GHz / 4.6 GHz Boost",
                    "tdp": "65W",
                    "igpu": "None",
                    "price": "₱9,000",
                    "compatibility": "AM4 Motherboards, DDR4 RAM"
        },
        "amd ryzen 7 5700x": {
            "name": "AMD Ryzen 7 5700X",
                    "type": "CPU",
                    "socket": "AM4",
                    "cores": "8 Cores / 16 Threads",
                    "clock": "3.4 GHz / 4.6 GHz Boost",
                    "tdp": "65W",
                    "igpu": "None",
                    "price": "₱12,000",
                    "compatibility": "AM4 Motherboards, DDR4 RAM"
        },
        "amd ryzen 7 5800x": {
            "name": "AMD Ryzen 7 5800X",
                    "type": "CPU",
                    "socket": "AM4",
                    "cores": "8 Cores / 16 Threads",
                    "clock": "3.8 GHz / 4.7 GHz Boost",
                    "tdp": "105W",
                    "igpu": "None",
                    "price": "₱14,000",
                    "compatibility": "AM4 Motherboards, DDR4 RAM"
        },
        "amd ryzen 9 5900x": {
            "name": "AMD Ryzen 9 5900X",
                    "type": "CPU",
                    "socket": "AM4",
                    "cores": "12 Cores / 24 Threads",
                    "clock": "3.7 GHz / 4.8 GHz Boost",
                    "tdp": "105W",
                    "igpu": "None",
                    "price": "₱18,000",
                    "compatibility": "AM4 Motherboards, DDR4 RAM"
        },
        "amd ryzen 5 7600": {
            "name": "AMD Ryzen 5 7600",
                    "type": "CPU",
                    "socket": "AM5",
                    "cores": "6 Cores / 12 Threads",
                    "clock": "3.8 GHz / 5.1 GHz Boost",
                    "tdp": "65W",
                    "igpu": "Radeon Graphics",
                    "price": "₱13,500",
                    "compatibility": "AM5 Motherboards, DDR5 RAM"
        },
        "amd ryzen 7 7700x": {
            "name": "AMD Ryzen 7 7700X",
                    "type": "CPU",
                    "socket": "AM5",
                    "cores": "8 Cores / 16 Threads",
                    "clock": "4.5 GHz / 5.4 GHz Boost",
                    "tdp": "105W",
                    "igpu": "Radeon Graphics",
                    "price": "₱18,500",
                    "compatibility": "AM5 Motherboards, DDR5 RAM"
        },
        "amd ryzen 9 7900x": {
            "name": "AMD Ryzen 9 7900X",
                    "type": "CPU",
                    "socket": "AM5",
                    "cores": "12 Cores / 24 Threads",
                    "clock": "4.7 GHz / 5.6 GHz Boost",
                    "tdp": "170W",
                    "igpu": "Radeon Graphics",
                    "price": "₱25,000",
                    "compatibility": "AM5 Motherboards, DDR5 RAM"
        },
        "amd ryzen 9 7950x": {
            "name": "AMD Ryzen 9 7950X",
                    "type": "CPU",
                    "socket": "AM5",
                    "cores": "16 Cores / 32 Threads",
                    "clock": "4.5 GHz / 5.7 GHz Boost",
                    "tdp": "170W",
                    "igpu": "Radeon Graphics",
                    "price": "₱32,000",
                    "compatibility": "AM5 Motherboards, DDR5 RAM"
        },
        "amd ryzen 5 5600x": {
            "name": "AMD Ryzen 5 5600X",
            "type": "CPU",
            "socket": "AM4",
            "cores": "6 Cores / 12 Threads",
            "clock": "3.7 GHz / 4.6 GHz Boost",
            "tdp": "65W",
            "igpu": "None",
            "price": "₱9,000",
            "compatibility": "AM4 Motherboards, DDR4 RAM"
        },
        "intel core i5 13400": {
            "name": "Intel Core i5 13400",
            "type": "CPU",
            "socket": "LGA1700",
            "cores": "10 Cores / 16 Threads",
            "clock": "2.5 GHz / 4.6 GHz Boost",
            "tdp": "65W",
            "igpu": "UHD Graphics 730",
            "price": "₱12,000",
            "compatibility": "LGA1700 Motherboards, DDR4/DDR5"
        },
        "intel core i3 13100": {
            "name": "Intel Core i3 13100",
                    "type": "CPU",
                    "socket": "LGA1700",
                    "cores": "4 Cores / 8 Threads",
                    "clock": "3.4 GHz / 4.5 GHz Boost",
                    "tdp": "60W",
                    "igpu": "UHD Graphics 730",
                    "price": "₱6,000",
                    "compatibility": "LGA1700 Motherboards, DDR4/DDR5"
        },
        "intel core i3 14100": {
            "name": "Intel Core i3 14100",
                    "type": "CPU",
                    "socket": "LGA1700",
                    "cores": "4 Cores / 8 Threads",
                    "clock": "3.5 GHz / 4.7 GHz Boost",
                    "tdp": "60W",
                    "igpu": "UHD Graphics 730",
                    "price": "₱6,500",
                    "compatibility": "LGA1700 Motherboards, DDR4/DDR5"
        },
        "intel core i5 13400": {
            "name": "Intel Core i5 13400",
                    "type": "CPU",
                    "socket": "LGA1700",
                    "cores": "10 Cores / 16 Threads",
                    "clock": "2.5 GHz / 4.6 GHz Boost",
                    "tdp": "65W",
                    "igpu": "UHD Graphics 730",
                    "price": "₱12,000",
                    "compatibility": "LGA1700 Motherboards, DDR4/DDR5"
        },
        "intel core i5 14500": {
            "name": "Intel Core i5 14500",
                    "type": "CPU",
                    "socket": "LGA1700",
                    "cores": "14 Cores / 20 Threads",
                    "clock": "2.6 GHz / 4.8 GHz Boost",
                    "tdp": "65W",
                    "igpu": "UHD Graphics 730",
                    "price": "₱13,500",
                    "compatibility": "LGA1700 Motherboards, DDR4/DDR5"
        },
        "intel core i5 14600k": {
            "name": "Intel Core i5 14600K",
                    "type": "CPU",
                    "socket": "LGA1700",
                    "cores": "14 Cores / 20 Threads",
                    "clock": "3.5 GHz / 5.3 GHz Boost",
                    "tdp": "125W",
                    "igpu": "UHD Graphics 770",
                    "price": "₱16,000",
                    "compatibility": "LGA1700 Motherboards, DDR4/DDR5"
        },
        "intel core i7 13700k": {
            "name": "Intel Core i7 13700K",
                    "type": "CPU",
                    "socket": "LGA1700",
                    "cores": "16 Cores / 24 Threads",
                    "clock": "3.4 GHz / 5.4 GHz Boost",
                    "tdp": "125W",
                    "igpu": "UHD Graphics 770",
                    "price": "₱22,000",
                    "compatibility": "LGA1700 Motherboards, DDR4/DDR5"
        },
        "intel core i7 14700k": {
            "name": "Intel Core i7 14700K",
                    "type": "CPU",
                    "socket": "LGA1700",
                    "cores": "20 Cores / 28 Threads",
                    "clock": "3.4 GHz / 5.6 GHz Boost",
                    "tdp": "125W",
                    "igpu": "UHD Graphics 770",
                    "price": "₱24,000",
                    "compatibility": "LGA1700 Motherboards, DDR4/DDR5"
        },
        "intel core i9 14900k": {
            "name": "Intel Core i9 14900K",
                    "type": "CPU",
                    "socket": "LGA1700",
                    "cores": "24 Cores / 32 Threads",
                    "clock": "3.2 GHz / 6.0 GHz Boost",
                    "tdp": "125W",
                    "igpu": "UHD Graphics 770",
                    "price": "₱32,000",
                    "compatibility": "LGA1700 Motherboards, DDR4/DDR5"
        }
    },
    "motherboard": {
        "gigabyte h610m k ddr4": {
            "name": "GIGABYTE H610M K DDR4",
                    "type": "Motherboard",
                    "socket": "LGA1700",
                    "form_factor": "mATX",
                    "ram_slots": 2,
                    "max_ram": "64GB",
                    "ram_type": "DDR4",
                    "nvme_slots": 1,
                    "sata_ports": 4,
                    "price": "₱4,500",
                    "compatibility": "LGA1700 CPUs, DDR4 RAM, PCIe 4.0"
        },
        "msi pro h610m s ddr4": {
            "name": "MSI Pro H610M S DDR4",
                    "type": "Motherboard",
                    "socket": "LGA1700",
                    "form_factor": "mATX",
                    "ram_slots": 2,
                    "max_ram": "64GB",
                    "ram_type": "DDR4",
                    "nvme_slots": 1,
                    "sata_ports": 4,
                    "price": "₱4,800",
                    "compatibility": "LGA1700 CPUs, DDR4 RAM, PCIe 4.0"
        },
        "msi b450m-a pro max ii": {
            "name": "MSI B450M-A PRO MAX II",
                    "type": "Motherboard",
                    "socket": "AM4",
                    "form_factor": "mATX",
                    "ram_slots": 2,
                    "max_ram": "64GB",
                    "ram_type": "DDR4",
                    "nvme_slots": 1,
                    "sata_ports": 4,
                    "price": "₱4,200",
                    "compatibility": "AM4 CPUs, DDR4 RAM, PCIe 3.0"
        },
        "ramsta rs-b450mp": {
            "name": "RAMSTA RS-B450MP",
                    "type": "Motherboard",
                    "socket": "AM4",
                    "form_factor": "mATX",
                    "ram_slots": 2,
                    "max_ram": "64GB",
                    "ram_type": "DDR4",
                    "nvme_slots": 1,
                    "sata_ports": 4,
                    "price": "₱3,800",
                    "compatibility": "AM4 CPUs, DDR4 RAM, PCIe 3.0"
        },
        "asus tuf gaming b550-plus": {
            "name": "ASUS TUF GAMING B550-PLUS",
                    "type": "Motherboard",
                    "socket": "AM4",
                    "form_factor": "ATX",
                    "ram_slots": 4,
                    "max_ram": "128GB",
                    "ram_type": "DDR4",
                    "nvme_slots": 2,
                    "sata_ports": 6,
                    "price": "₱7,800",
                    "compatibility": "AM4 CPUs, DDR4 RAM, PCIe 4.0"
        },
        "asus prime b650-plus": {
            "name": "ASUS PRIME B650-PLUS",
                    "type": "Motherboard",
                    "socket": "AM5",
                    "form_factor": "ATX",
                    "ram_slots": 4,
                    "max_ram": "128GB",
                    "ram_type": "DDR5",
                    "nvme_slots": 3,
                    "sata_ports": 4,
                    "price": "₱9,500",
                    "compatibility": "AM5 CPUs, DDR5 RAM, PCIe 4.0"
        },
        "msi pro x670-p wifi": {
            "name": "MSI PRO X670-P WIFI",
                    "type": "Motherboard",
                    "socket": "AM5",
                    "form_factor": "ATX",
                    "ram_slots": 4,
                    "max_ram": "128GB",
                    "ram_type": "DDR5",
                    "nvme_slots": 4,
                    "sata_ports": 6,
                    "price": "₱14,000",
                    "compatibility": "AM5 CPUs, DDR5 RAM, PCIe 5.0"
        },
        "msi mpg z790 carbon wifi": {
            "name": "MSI MPG Z790 CARBON WIFI",
                    "type": "Motherboard",
                    "socket": "LGA1700",
                    "form_factor": "ATX",
                    "ram_slots": 4,
                    "max_ram": "128GB",
                    "ram_type": "DDR5",
                    "nvme_slots": 5,
                    "sata_ports": 6,
                    "price": "₱18,500",
                    "compatibility": "LGA1700 CPUs, DDR5 RAM, PCIe 5.0"
        }
    },
    "ram": {
        "kingston fury beast ddr4 8gb": {
            "name": "Kingston FURY Beast DDR4 8GB",
                    "type": "RAM",
                    "capacity": "8GB",
                    "speed": "3200MHz",
                    "ram_type": "DDR4",
                    "price": "₱1,500",
                    "compatibility": "DDR4 Motherboards (AM4, LGA1700 DDR4)"
        },
        "kingston fury beast ddr4 16gb": {
            "name": "Kingston FURY Beast DDR4 16GB",
                    "type": "RAM",
                    "capacity": "16GB",
                    "speed": "3200MHz",
                    "ram_type": "DDR4",
                    "price": "₱3,000",
                    "compatibility": "DDR4 Motherboards (AM4, LGA1700 DDR4)"
        },
        "hkcmemory hu40 ddr4 16gb": {
            "name": "HKCMEMORY HU40 DDR4 16GB",
                    "type": "RAM",
                    "capacity": "16GB",
                    "speed": "3200MHz",
                    "ram_type": "DDR4",
                    "price": "₱2,200",
                    "compatibility": "DDR4 Motherboards (AM4, LGA1700 DDR4)"
        },
        "kingston fury beast ddr4 32gb": {
            "name": "Kingston FURY Beast DDR4 32GB",
                    "type": "RAM",
                    "capacity": "32GB",
                    "speed": "3200MHz",
                    "ram_type": "DDR4",
                    "price": "₱3,800",
                    "compatibility": "DDR4 Motherboards (AM4, LGA1700 DDR4)"
        },
        "kingston fury beast ddr5 8gb": {
            "name": "Kingston FURY Beast DDR5 8GB",
                    "type": "RAM",
                    "capacity": "8GB",
                    "speed": "4800MHz",
                    "ram_type": "DDR5",
                    "price": "₱2,000",
                    "compatibility": "DDR5 Motherboards (AM5, LGA1700 DDR5)"
        },
        "kingston fury beast ddr5 16gb": {
            "name": "Kingston FURY Beast DDR5 16GB",
                    "type": "RAM",
                    "capacity": "16GB",
                    "speed": "4800MHz",
                    "ram_type": "DDR5",
                    "price": "₱3,000",
                    "compatibility": "DDR5 Motherboards (AM5, LGA1700 DDR5)"
        },
        "corsair vengeance ddr5 32gb": {
            "name": "Corsair Vengeance DDR5 32GB",
                    "type": "RAM",
                    "capacity": "32GB",
                    "speed": "5200MHz",
                    "ram_type": "DDR5",
                    "price": "₱5,500",
                    "compatibility": "DDR5 Motherboards (AM5, LGA1700 DDR5)"
        }
    },
    "storage": {
        "seagate video 3.5\" hdd 500gb": {
            "name": "Seagate Video 3.5\" HDD 500GB",
                    "type": "HDD",
                    "capacity": "500GB",
                    "interface": "SATA 6Gb/s",
                    "price": "₱1,200",
                    "compatibility": "Any motherboard with SATA port"
        },
        "seagate video 3.5\" hdd 1tb": {
            "name": "Seagate Video 3.5\" HDD 1TB",
                    "type": "HDD",
                    "capacity": "1TB",
                    "interface": "SATA 6Gb/s",
                    "price": "₱1,800",
                    "compatibility": "Any motherboard with SATA port"
        },
        "ramsta s800 128gb": {
            "name": "Ramsta S800 128GB SSD",
                    "type": "SATA SSD",
                    "capacity": "128GB",
                    "interface": "SATA 6Gb/s",
                    "price": "₱800",
                    "compatibility": "Any motherboard with SATA port"
        },
        "ramsta s800 256gb": {
            "name": "Ramsta S800 256GB SSD",
                    "type": "SATA SSD",
                    "capacity": "256GB",
                    "interface": "SATA 6Gb/s",
                    "price": "₱1,200",
                    "compatibility": "Any motherboard with SATA port"
        },
        "ramsta s800 512gb": {
            "name": "Ramsta S800 512GB SSD",
                    "type": "SATA SSD",
                    "capacity": "512GB",
                    "interface": "SATA 6Gb/s",
                    "price": "₱1,800",
                    "compatibility": "Any motherboard with SATA port"
        },
        "ramsta s800 1tb": {
            "name": "Ramsta S800 1TB SSD",
                    "type": "SATA SSD",
                    "capacity": "1TB",
                    "interface": "SATA 6Gb/s",
                    "price": "₱2,800",
                    "compatibility": "Any motherboard with SATA port"
        },
        "ramsta s800 2tb": {
            "name": "Ramsta S800 2TB SSD",
                    "type": "SATA SSD",
                    "capacity": "2TB",
                    "interface": "SATA 6Gb/s",
                    "price": "₱4,500",
                    "compatibility": "Any motherboard with SATA port"
        },
        "crucial mx500 500gb": {
            "name": "Crucial MX500 500GB SSD",
                    "type": "SATA SSD",
                    "capacity": "500GB",
                    "interface": "SATA 6Gb/s",
                    "price": "₱2,200",
                    "compatibility": "Any motherboard with SATA port"
        },
        "samsung 970 evo plus 250gb": {
            "name": "Samsung 970 EVO Plus 250GB",
                    "type": "NVMe SSD",
                    "capacity": "250GB",
                    "interface": "PCIe 3.0 x4",
                    "price": "₱1,800",
                    "compatibility": "Motherboard with M.2 NVMe slot"
        },
        "samsung 970 evo plus 500gb": {
            "name": "Samsung 970 EVO Plus 500GB",
                    "type": "NVMe SSD",
                    "capacity": "500GB",
                    "interface": "PCIe 3.0 x4",
                    "price": "₱2,500",
                    "compatibility": "Motherboard with M.2 NVMe slot"
        },
        "samsung 970 evo plus 1tb": {
            "name": "Samsung 970 EVO Plus 1TB",
                    "type": "NVMe SSD",
                    "capacity": "1TB",
                    "interface": "PCIe 3.0 x4",
                    "price": "₱4,000",
                    "compatibility": "Motherboard with M.2 NVMe slot"
        },
        "samsung 970 evo plus 2tb": {
            "name": "Samsung 970 EVO Plus 2TB",
                    "type": "NVMe SSD",
                    "capacity": "2TB",
                    "interface": "PCIe 3.0 x4",
                    "price": "₱7,000",
                    "compatibility": "Motherboard with M.2 NVMe slot"
        }
    },
    "psu": {
        "inplay ak400": {
            "name": "InPlay AK400",
                    "type": "PSU",
                    "wattage": "400W",
                    "efficiency": "80+",
                    "price": "₱1,200",
                    "compatibility": "Basic builds, low-power components"
        },
        "inplay gs 550": {
            "name": "InPlay GS 550",
                    "type": "PSU",
                    "wattage": "550W",
                    "efficiency": "80+ Bronze",
                    "price": "₱1,800",
                    "compatibility": "Mid-range builds, single GPU systems"
        },
        "corsair cx650": {
            "name": "Corsair CX650",
                    "type": "PSU",
                    "wattage": "650W",
                    "efficiency": "80+ Bronze",
                    "price": "₱3,500",
                    "compatibility": "Gaming builds, most single GPU configurations"
        },
        "inplay gs 750": {
            "name": "InPlay GS 750",
                    "type": "PSU",
                    "wattage": "750W",
                    "efficiency": "80+ Bronze",
                    "price": "₱2,500",
                    "compatibility": "High-end builds, powerful GPUs"
        },
        "cooler master mwe white 750w": {
            "name": "Cooler Master MWE White 750W",
                    "type": "PSU",
                    "wattage": "750W",
                    "efficiency": "80+ White",
                    "price": "₱3,800",
                    "compatibility": "High-end gaming builds, multiple components"
        },
        "corsair rm850x 850w": {
            "name": "Corsair RM850x 850W",
                    "type": "PSU",
                    "wattage": "850W",
                    "efficiency": "80+ Gold",
                    "price": "₱6,500",
                    "compatibility": "Premium builds, high-end GPUs, overclocking"
        }
    },
    "cpu_cooler": {
        "fantech polar lc240": {
            "name": "Fantech Polar LC240",
                    "type": "CPU Cooler",
                    "cooler_type": "Liquid Cooler",
                    "size": "240mm",
                    "socket": "AM4, AM5, LGA1700, LGA1200, LGA1151",
                    "price": "₱2,800",
                    "compatibility": "Most modern CPU sockets"
        },
        "inplay seaview 240 pro": {
            "name": "Inplay Seaview 240 Pro",
                    "type": "CPU Cooler",
                    "cooler_type": "Liquid Cooler",
                    "size": "240mm",
                    "socket": "AM4, AM5, LGA1700, LGA1200",
                    "price": "₱2,200",
                    "compatibility": "Modern CPU sockets"
        },
        "inplay seaview 360 pro": {
            "name": "Inplay Seaview 360 Pro",
                    "type": "CPU Cooler",
                    "cooler_type": "Liquid Cooler",
                    "size": "360mm",
                    "socket": "AM4, AM5, LGA1700, LGA1200",
                    "price": "₱2,800",
                    "compatibility": "Modern CPU sockets"
        },
        "inplay s20": {
            "name": "Inplay S20",
                    "type": "CPU Cooler",
                    "cooler_type": "Air Cooler",
                    "size": "120mm",
                    "socket": "AM4, LGA1700, LGA1200",
                    "price": "₱600",
                    "compatibility": "Basic cooling for low to mid-range CPUs"
        },
        "inplay s40": {
            "name": "Inplay S40",
                    "type": "CPU Cooler",
                    "cooler_type": "Air Cooler",
                    "size": "120mm",
                    "socket": "AM4, AM5, LGA1700, LGA1200",
                    "price": "₱800",
                    "compatibility": "Mid-range CPUs, good value cooling"
        },
        "cooler master hyper 212 black edition": {
            "name": "Cooler Master Hyper 212 Black Edition",
                    "type": "CPU Cooler",
                    "cooler_type": "Air Cooler",
                    "size": "120mm",
                    "socket": "AM4, AM5, LGA1700, LGA1200, LGA1151",
                    "price": "₱2,000",
                    "compatibility": "Excellent air cooling for mid to high-end CPUs"
        },
        "deepcool ls720 se 360": {
            "name": "DeepCool LS720 SE 360",
                    "type": "CPU Cooler",
                    "cooler_type": "Liquid Cooler",
                    "size": "360mm",
                    "socket": "AM4, AM5, LGA1700, LGA1200",
                    "price": "₱4,500",
                    "compatibility": "High-performance cooling"
        },
        "cooler master masterliquid ml360r rgb": {
            "name": "Cooler Master MasterLiquid ML360R RGB",
                    "type": "CPU Cooler",
                    "cooler_type": "Liquid Cooler",
                    "size": "360mm",
                    "socket": "AM4, AM5, LGA1700, LGA2066, LGA1200",
                    "price": "₱5,500",
                    "compatibility": "Premium cooling solution, high-end CPUs"
        }
    }
}


# -------------------------------
# 🧰 Utilities
# -------------------------------


def normalize_text(s):
    """Lowercase & return alphanumeric tokens (keeps numbers like 5600g, i7)."""
    if not s:
        return []
    return re.findall(r'\w+', s.lower())


def parse_watts(value):
    """Extract integer watt value from strings like '65W', '~115 Watts', '170W'."""
    if not value:
        return None
    s = str(value)
    m = re.search(r'(\d{2,4})', s.replace(',', ''))
    return int(m.group(1)) if m else None


def parse_price(value):
    """Extract integer value from price string '₱1,800' or '₱ 1,800'."""
    if not value:
        return None
    s = str(value)
    m = re.search(r'(\d[\d,]*)', s)
    if not m:
        return None
    num = int(m.group(1).replace(',', ''))
    return num


def round_up_psu(w):
    """Round up to common PSU sizes: 450, 550, 650, 750, 850, 1000, 1200"""
    sizes = [450, 550, 650, 750, 850, 1000, 1200, 1500]
    for s in sizes:
        if w <= s:
            return s
    return sizes[-1]


def format_php(n):
    """Format integer to Philippine peso string with commas."""
    try:
        return f"₱{int(n):,}"
    except:
        return str(n)


def tokenize(text):
    """Return lowercased tokens (alphanumeric + dash) for robust matching."""
    if not text:
        return []
    # keep tokens like 'mini-itx', 'lga1700'
    tokens = re.findall(r"[a-z0-9\-]+", text.lower())
    return tokens


# -------------------------------
# 📚 Educational Features
# -------------------------------


EDU_EXPLANATIONS = {
    "pcie": {
        "title": "Understanding PCIe Slots",
        "short": (
            "PCI Express (PCIe) connects GPUs, SSDs, and network cards to the motherboard. "
            "Each new generation doubles the data bandwidth. "
            "Higher versions (4.0, 5.0) are faster but backward compatible."
        ),
        "notes": [
            "PCIe 3.0 ≈ 1 GB/s per lane; PCIe 4.0 doubles that.",
            "A PCIe 4.0 GPU works fine in a PCIe 3.0 slot (just slightly slower)."
        ]
    },
    "ddr4 vs ddr5": {
        "title": "DDR4 vs DDR5 Memory",
        "short": (
            "DDR5 is newer than DDR4, providing faster speeds, higher capacity per stick, "
            "and better power efficiency. But it requires a DDR5-compatible motherboard."
        ),
        "notes": [
            "DDR4 and DDR5 are not interchangeable.",
            "DDR5 usually starts at 4800 MHz; DDR4 commonly around 3200–3600 MHz."
        ]
    },
    "sockets": {
        "title": "CPU Sockets Explained",
        "short": (
            "A CPU socket is the connector that holds your CPU on the motherboard. "
            "Each CPU family supports only certain sockets."
        ),
        "notes": [
            "AMD Ryzen 3000–5000 use AM4; Ryzen 7000 uses AM5.",
            "Intel 12th–14th Gen CPUs use LGA1700 sockets."
        ]
    },
    "psu efficiency": {
        "title": "PSU Efficiency Ratings (80 Plus)",
        "short": (
            "PSUs have 80 Plus ratings like Bronze, Gold, or Platinum. "
            "These indicate efficiency—how much power turns into usable energy instead of heat."
        ),
        "notes": [
            "Bronze ≈ 85% efficient; Gold ≈ 90%; Platinum ≈ 92–94%.",
            "Higher efficiency means less heat and slightly lower electricity use."
        ]
    }
}


def explain_concept(user_text):
    """
    Match a user query to an explanation in EDU_EXPLANATIONS.
    Returns a formatted string or None if no concept matched.
    """
    q = (user_text or "").lower()
    # Simple keyword matching for concept keys and synonyms
    concept_map = {
        "pcie": ["pcie", "pci-e", "pci express", "pcie 3.0", "pcie 4.0", "pcie 5.0"],
        "ddr4 vs ddr5": ["ddr4", "ddr5", "ddr4 vs ddr5", "memory generations"],
        "sockets": ["socket", "am4", "am5", "lga1700", "cpu socket"],
        "psu efficiency": ["psu", "efficiency", "80+", "80 plus", "bronze", "gold", "platinum", "psu rating"]
    }
    for key, keys in concept_map.items():
        if any(k in q for k in keys):
            e = EDU_EXPLANATIONS.get(key)
            if not e:
                return None
            out = []
            out.append(f"🔎 {e['title']}\n")
            # short paragraph, wrapped
            out.append(textwrap.fill(e["short"], width=80))
            if e.get("notes"):
                out.append("\n\nKey notes:")
                for n in e["notes"]:
                    out.append("• " + n)
            return "\n".join(out)
    return None


def list_components_by_category(user_text):
    """
    If user asked to 'list GPUs' or 'show CPU list', return all items in that category.
    Recognizes plural and singular keywords.
    """
    q = (user_text or "").lower()
    cat_map = {
        "cpu": ["cpu", "cpus", "processor", "processors", "intel", "amd"],
        "gpu": ["gpu", "gpus", "graphics", "video card", "video cards", "rtx", "gtx"],
        "motherboard": ["motherboard", "motherboards", "mobo", "mobos"],
        "ram": ["ram", "memory", "memories", "ddr4", "ddr5"],
        "storage": ["storage", "ssd", "nvme", "hdd"],
        "psu": ["psu", "power supply", "power supplies"],
        "cpu_cooler": ["cooler", "cpu cooler", "coolers", "liquid cooler", "air cooler"]
    }
    for cat, triggers in cat_map.items():
        if any(t in q for t in triggers):
            items = data.get(cat, {})
            if not items:
                return f"No components found for category '{cat}'."
            lines = [f"📦 Available {cat.upper()}s ({len(items)}):", "-" * 60]
            # sort by name for stable output
            for key in sorted(items.keys()):
                info = items[key]
                name = info.get("name", key)
                price = info.get("price", "N/A")
                short = []
                if cat == "cpu":
                    short.append(info.get("socket", ""))
                    short.append(info.get("cores", ""))
                if cat == "gpu":
                    short.append(info.get("vram", ""))
                if cat == "ram":
                    short.append(info.get("capacity", ""))
                    short.append(info.get("ram_type", ""))
                # compact short spec
                short_spec = " • ".join([s for s in short if s])
                lines.append(f"- {name} — {short_spec} — {price}")
            return "\n".join(lines)
    return None


# Intent detector for educational queries
EDU_KEYWORDS = [
    "explain", "what is", "how does", "list", "show",
    "pcie", "ddr4", "ddr5", "socket", "am4", "am5", "lga1700",
    "80+", "psu", "nvme", "sata", "tdp", "form factor", "overclock"
]


def is_education_request(user_text):
    t = (user_text or "").lower()
    # Only treat as education if clear educational keywords present (avoid compare/versus)
    for kw in EDU_KEYWORDS:
        if re.search(r'\b' + re.escape(kw) + r'\b', t):
            return True
    # explicitly exclude compare-like words here
    if re.search(r'\b(explain|what is|how does)\b', t):
        return True
    return False


def handle_education_request(user_text):
    # Try concept explanation first
    explanation = explain_concept(user_text)
    if explanation:
        print("\n🤖 ARIA — Educational Explanation:\n")
        print(explanation)
        print("\n" + "-" * 60 + "\n")
        return

    # Then try listing components
    listing = list_components_by_category(user_text)
    if listing:
        print("\n🤖 ARIA — Component List:\n")
        print(listing)
        print("\n" + "-" * 60 + "\n")
        return

    # Fallback: brief help about available educational topics
    topics = ", ".join([v["title"] for v in EDU_EXPLANATIONS.values()])
    print("\n🤖 ARIA — Educational Help:\n")
    print("I can explain topics such as: " + topics + ".")
    print("Try: 'Explain PCIe 4.0', 'What is DDR5?', 'What is an AM4 socket?', or 'List GPUs'.")
    print("\n" + "-" * 60 + "\n")


# -------------------------------
# 🛠️ Build Planning Features
# -------------------------------
# Budget tiers (bounds inclusive)
BUILD_TIERS = {
    "budget": (15000, 20000),
    "entry": (25000, 35000),
    "mid": (40000, 60000),
    "high": (70000, 10**9),
}

# -------------------------------
# . Build Planning / Budget Logic
# -------------------------------


def parse_budget_from_text(text):
    """
    Robust budget parser:
    - Normalizes unicode (handles NBSP etc.)
    - Accepts currency markers (₱ / php / peso)
    - Accepts numbers with commas/spaces (e.g., '₱20,000', '₱ 20 000')
    - Accepts 'k' shorthand when context implies budget
    Returns integer PHP amount or None.
    """
    if not text:
        return None
    t = str(text)

    # Normalize unicode (turn NBSP into normal space, normalize composed chars)
    t = unicodedata.normalize("NFKC", t)
    t = t.replace("\u00A0", " ")  # NBSP -> space
    lower = t.lower()

    # If explicit currency marker present, try to extract first numeric token
    if "₱" in lower or "php" in lower or "peso" in lower:
        # remove currency words, keep digits, ., k, commas, spaces
        s = re.sub(r'(₱|php|peso)', ' ', lower)
        # find number with optional k
        m = re.search(
            r'(\d{1,3}(?:[,\s]\d{3})*(?:\.\d+)?|\d+(?:\.\d+)?)(\s*[kK])?', s)
        if m:
            num_s = m.group(1).replace(",", "").replace(" ", "")
            try:
                num = float(num_s)
                if m.group(2):  # has 'k'
                    return int(num * 1000)
                return int(num)
            except:
                pass

    # If no explicit currency words, accept '25k' when there's build/budget context
    if re.search(r'\b(budget|buy|price|cost|php|₱|peso|recommend|suggest|for)\b', lower):
        # match forms like '25k', '25 k', '25000'
        m = re.search(r'(\d+(?:[\.,]\d+)?)[\s]*([kK])\b', lower)
        if m:
            try:
                val = float(m.group(1).replace(',', '.'))
                if 0 < val <= 2000:  # sanity cap
                    return int(val * 1000)
            except:
                pass
        # fallback to plain number with commas
        m2 = re.search(r'(\d{1,3}(?:[,\s]\d{3})+|\d+)', lower)
        if m2:
            num_s = m2.group(1).replace(",", "").replace(" ", "")
            try:
                return int(float(num_s))
            except:
                pass

    # Last-resort: accept any small 'k' token alone (e.g., '25k')
    m = re.search(r'(\d+(?:\.\d+)?)\s*[kK]\b', lower)
    if m:
        try:
            val = float(m.group(1))
            if val <= 2000:
                return int(val * 1000)
        except:
            pass

    return None


def price_list_for_category(cat):
    """Return list of tuples (key, info, price_int) for a category with numeric prices."""
    out = []
    items = data.get(cat, {})
    for k, info in items.items():
        p = parse_price(info.get("price"))
        if p:
            out.append((k, info, p))
    # sort ascending price
    out.sort(key=lambda x: x[2])
    return out


def pick_motherboard_for_cpu(cpu_info, mobo_list):
    """Return a motherboard from mobo_list compatible with cpu_info (socket match)."""
    cpu_socket = (cpu_info.get("socket") or "").lower()
    for k, m, p in mobo_list:
        m_socket = (m.get("socket") or "").lower()
        if cpu_socket and m_socket and cpu_socket == m_socket:
            return (k, m, p)
    # fallback: pick the cheapest if nothing matches
    return mobo_list[0] if mobo_list else None


def pick_ram_for_mobo(mobo_info, ram_list):
    """Pick RAM compatible with motherboard ram_type if possible, else cheapest."""
    mobo_ram_type = (mobo_info.get("ram_type") or "").lower()
    for k, r, p in ram_list:
        r_type = (r.get("ram_type") or "").lower()
        if mobo_ram_type and r_type and mobo_ram_type in r_type:
            return (k, r, p)
    return ram_list[0] if ram_list else None


def estimate_psu_requirement(cpu_info, gpu_info):
    """Estimate PSU requirement using TDP/power plus base overhead and headroom."""
    cpu_tdp = parse_watts(cpu_info.get("tdp")) or 0
    gpu_power = parse_watts(gpu_info.get("power")) or 0
    base_system = 120
    total = cpu_tdp + gpu_power + base_system
    recommended = math.ceil(total * 1.25)  # Adding 25% buffer for safety
    # Ensure we get an appropriate PSU size
    suggested_psu_size = round_up_psu(recommended)
    return recommended, suggested_psu_size


def handle_psu_request(user_query):
    """
    Handle PSU / wattage questions. Finds components in query, estimates power, and prints recommendation.
    """
    found = extract_components_from_text(user_query)
    if not found:
        print("\n🤖 ARIA says:\n\nI couldn't find the components you mentioned. Try names like 'RTX 3060' or 'Ryzen 5 5600X'.\n")
        return

    # prefer CPU + GPU pair if both present
    cpu = None
    gpu = None
    others = []
    for cat, info, key in found:
        if cat == "cpu" and cpu is None:
            cpu = (cat, info, key)
        elif cat == "gpu" and gpu is None:
            gpu = (cat, info, key)
        else:
            others.append((cat, info, key))

    # If no explicit CPU+GPU found, take the top two matched components
    if not cpu or not gpu:
        combined = []
        if cpu:
            combined.append(cpu)
        if gpu:
            combined.append(gpu)
        for item in others:
            if len(combined) >= 2:
                break
            combined.append(item)
        if len(combined) >= 2:
            # assign from combined
            cpu = combined[0] if combined[0][0] == "cpu" else cpu or combined[0]
            gpu = combined[1] if combined[1][0] == "gpu" else gpu or combined[1]
        else:
            # only one component present
            comp = combined[0] if combined else found[0]
            cat, info, key = comp
            print(
                f"\n🤖 ARIA says:\n\nI only found one component ({info.get('name')}). To calculate PSU wattage I need at least a CPU and a GPU (or two parts). Please mention both (e.g., 'GTX 750 Ti and Ryzen 5 5600X').\n")
            return

    # Fallback: if cpu/gpu are still None, pick first two found
    if not cpu or not gpu:
        a = found[0]
        b = found[1] if len(found) > 1 else None
        if not b:
            print(
                "\n🤖 ARIA says:\n\nPlease mention two components to estimate PSU wattage.\n")
            return
        cpu, gpu = a, b

    # Extract infos for estimation
    a_cat, a_info, a_key = cpu
    b_cat, b_info, b_key = gpu

    # Use your existing estimate function (ensure order doesn't matter)
    rec_watt, suggested_size = estimate_psu_requirement(
        a_info if a_cat == "cpu" else b_info,
        b_info if b_cat == "gpu" else a_info
    )

    # Print a helpful explanation
    cpu_name = (a_info.get("name") if a_cat == "cpu" else b_info.get("name"))
    gpu_name = (b_info.get("name") if b_cat == "gpu" else a_info.get("name"))

    print("\n🤖 ARIA — PSU Recommendation:\n")
    print(f"For {cpu_name} + {gpu_name}:")
    print(f"• Estimated continuous system draw (approx): {rec_watt} W")
    print(f"• Recommended PSU size (with headroom): {suggested_size} W")
    print("\nNotes:")
    print("• This is a conservative estimate based on TDPs and a base system overhead.")
    print("• If you plan to overclock, add ~100W extra. If you have many drives or accessories, add 50–100W.")
    print("• Choose a quality PSU (80+ Bronze or better) and the correct connectors for your GPU.\n")


def handle_store_request(user_query: str):
    """
    Handle user queries about PC stores or locations.
    """
    store_name = "SMFP Computer"
    store_address = "594 J. Nepomuceno St, Quiapo, Manila, 1001 Metro Manila"

    q = user_query.lower()

    # Simple detection for store/location-related questions
    store_triggers = [
        "store", "shop", "buy", "purchase", "where can i buy",
        "pc store", "computer store", "smfp", "location", "branch"
    ]

    if any(word in q for word in store_triggers):
        print(f"\n🏬 SMFP COMPUTER — STORE INFORMATION\n")
        print(f"📍 Name: {store_name}")
        print(f"📫 Address: {store_address}")
        print("\n🕓 Store Hours: Usually 10:00 AM – 6:00 PM (verify before visiting).")
        print("☎️ You can visit or contact the shop directly for part availability.\n")
        print("-" * 60 + "\n")

        # (Optional) Add to chat history
        try:
            add_to_history(
                "assistant", f"Shared store info: {store_name}, {store_address}")
        except Exception:
            pass
        return True

    return False


def check_compatibility(user_query):
    """
    Try to answer compatibility questions. Returns True if we printed an answer,
    False if we couldn't handle (e.g., fewer than 2 components found).
    """
    found = extract_components_from_text(user_query)
    if not found:
        print("\n🤖 ARIA says:\n\nI couldn't find the components you mentioned. Try names like 'RTX 3060' or 'Ryzen 5 5600X'.\n")
        return False

    # Keep unique components (category+key) preserving order
    seen = set()
    comps = []
    for cat, info, key in found:
        iden = (cat, key)
        if iden not in seen:
            seen.add(iden)
            comps.append((cat, info, key))
        if len(comps) >= 2:
            break

    if len(comps) < 2:
        # Not enough components to check compatibility
        print("\n🤖 ARIA says:\n\nI need at least two components to check compatibility (for example: 'Will Ryzen 5 5600X work with B550?').\n")
        return False

    a_cat, a_info, a_key = comps[0]
    b_cat, b_info, b_key = comps[1]

    a_name = a_info.get("name", a_key)
    b_name = b_info.get("name", b_key)

    # CPU <-> Motherboard check
    if (a_cat == "cpu" and b_cat == "motherboard") or (a_cat == "motherboard" and b_cat == "cpu"):
        cpu_info = a_info if a_cat == "cpu" else b_info
        mobo_info = b_info if b_cat == "motherboard" else a_info

        cpu_socket = (cpu_info.get("socket") or "").lower()
        mobo_socket = (mobo_info.get("socket") or "").lower()
        mobo_ram = (mobo_info.get("ram_type") or "").lower()
        cpu_ram_req = None
        # some CPUs include compatibility text listing ram type
        if cpu_info.get("compatibility"):
            cpu_compat = cpu_info.get("compatibility").lower()
            if "ddr5" in cpu_compat:
                cpu_ram_req = "ddr5"
            elif "ddr4" in cpu_compat:
                cpu_ram_req = "ddr4"

        print(f"\n🤖 ARIA — Compatibility Check:\n")
        print(f"{cpu_info.get('name')}  ↔  {mobo_info.get('name')}")
        print("-" * 60)

        # socket check
        if cpu_socket and mobo_socket:
            if cpu_socket == mobo_socket:
                print(f"• Socket: OK — both use {cpu_socket.upper()}.")
            else:
                print(
                    f"• Socket: NOT COMPATIBLE — CPU uses {cpu_socket.upper()} while motherboard uses {mobo_socket.upper()}.")
        else:
            print("• Socket: Missing data for one or both components.")

        # RAM type check (mobo.ram_type vs cpu.compatibility)
        if mobo_ram:
            if cpu_ram_req:
                if cpu_ram_req in mobo_ram:
                    print(
                        f"• RAM type: OK — motherboard supports {mobo_ram.upper()} and CPU is compatible with {cpu_ram_req.upper()}.")
                else:
                    print(
                        f"• RAM type: POSSIBLE ISSUE — motherboard supports {mobo_ram.upper()} but CPU looks to prefer {cpu_ram_req.upper()}.")
            else:
                print(
                    f"• RAM type: Motherboard supports {mobo_ram.upper()}. Confirm CPU memory compatibility if needed.")
        else:
            print("• RAM type: No motherboard RAM-type info available.")

        print("\nNotes:\n• Check BIOS updates for older CPUs on newer motherboards (some combos require BIOS updates).\n• Confirm physical CPU cooler mounting for the socket.\n")
        return True

    # CPU <-> RAM check
    if (a_cat == "cpu" and b_cat == "ram") or (a_cat == "ram" and b_cat == "cpu"):
        cpu_info = a_info if a_cat == "cpu" else b_info
        ram_info = b_info if b_cat == "ram" else a_info
        cpu_name = cpu_info.get("name")
        ram_type = ram_info.get("ram_type") or ram_info.get("type") or ""
        print(f"\n🤖 ARIA — Compatibility Check:\n")
        print(f"{cpu_name}  ↔  {ram_info.get('name')}")
        print("-" * 60)
        # best-effort: check CPU compatibility field or compatibility text
        cpu_compat = (cpu_info.get("compatibility") or "").lower()
        if ram_type and (ram_type.lower() in cpu_compat or ram_type.lower() in (cpu_info.get("socket") or "")):
            print(
                f"• RAM type: Looks compatible (RAM: {ram_type}, CPU compatibility: {cpu_compat}).")
        else:
            if ram_type:
                print(
                    f"• RAM type: Motherboard/CPU compatibility unclear — RAM is {ram_type}. Check motherboard RAM support.")
            else:
                print("• RAM type: No RAM-type info available.")
        print()
        return True

    # GPU <-> Motherboard check (basic)
    if (a_cat == "gpu" and b_cat == "motherboard") or (a_cat == "motherboard" and b_cat == "gpu"):
        gpu_info = a_info if a_cat == "gpu" else b_info
        mobo_info = b_info if b_cat == "motherboard" else a_info

        print(f"\n🤖 ARIA — Compatibility Check:\n")
        print(f"{gpu_info.get('name')}  ↔  {mobo_info.get('name')}")
        print("-" * 60)

        # GPU slot check: look for 'slot' on gpu and assume motherboards with any PCIe support are fine
        gpu_slot = (gpu_info.get("slot") or "").lower()
        mobo_nvme = mobo_info.get("nvme_slots")
        mobo_pci_note = mobo_info.get("compatibility", "").lower()

        if gpu_slot:
            # basic check: mention PCIe and slot width if present
            print(f"• GPU slot: {gpu_slot}.")
            # check motherboard compatibility note for PCIe support
            if "pcie" in mobo_pci_note or mobo_nvme is not None or "pci" in mobo_pci_note:
                print(
                    "• Motherboard: Appears to have PCIe support — GPU should fit physically (check full-length slot and BIOS).")
            else:
                print(
                    "• Motherboard: PCIe slot info not explicit — please verify the motherboard has a full-length PCIe x16 slot.")
        else:
            print("• GPU slot: No slot info available for GPU. Most modern motherboards have at least one PCIe x16 slot — verify motherboard specs.")
        # power/connectors note
        if gpu_info.get("power"):
            print(
                f"• GPU power: {gpu_info.get('power')} — ensure PSU has required connectors.")
        print("\nNotes:\n• Confirm card length and clearance for your case and verify PSU connectors and wattage.\n")
        return True

    # If both components are the same category (e.g., two CPUs or two GPUs), give a short comparison hint
    if a_cat == b_cat:
        print(
            f"\n🤖 ARIA says:\n\nYou mentioned two {a_cat.upper()}s: {a_name} and {b_name}.\nI can compare specs (cores, clocks, price). Try 'compare {a_key} and {b_key}'.\n")
        return True

    # Generic fallback: different categories — print their key specs and say manual check may be required
    print(f"\n🤖 ARIA — Compatibility (best-effort):\n")
    print(f"{a_name}  ↔  {b_name}")
    print("-" * 60)
    # print some key fields for manual inspection

    def short_specs(info):
        keys = []
        for k in ("socket", "vram", "cores", "clock", "tdp", "capacity", "ram_type", "wattage"):
            if k in info:
                keys.append(f"{k}: {info[k]}")
        return " • ".join(keys) if keys else "No quick specs available."

    print(f"{a_name}: {short_specs(a_info)}")
    print(f"{b_name}: {short_specs(b_info)}")
    print("\nI couldn't identify a direct compatibility rule for these two parts. Check the detailed specs above for socket, RAM type, PCIe slot, and power connectors.\n")
    return True


def assemble_build_for_budget(budget):
    """
    Greedy assembly strategy:
    - Allocate portions of budget to categories (CPU, GPU, MB, RAM, Storage, PSU, Cooler)
    - Choose best-priced items from data within allocation while ensuring compat.
    This is heuristic and uses only local data.
    Returns dict with chosen components and totals or None if cannot assemble.
    """
    # if budget is small, budget allocations more towards CPU+GPU; else balanced
    # allocation percentages (sum <=1, leave small margin)
    # We'll attempt several allocation profiles; choose the first valid build
    allocation_profiles = [
        # budget-oriented (more GPU/CPU)
        {"cpu": 0.28, "gpu": 0.32, "motherboard": 0.12, "ram": 0.08,
            "storage": 0.08, "psu": 0.06, "cooler": 0.06},
        # balanced
        {"cpu": 0.25, "gpu": 0.30, "motherboard": 0.12, "ram": 0.10,
            "storage": 0.10, "psu": 0.07, "cooler": 0.06},
        # CPU-focused (for productivity)
        {"cpu": 0.32, "gpu": 0.24, "motherboard": 0.12, "ram": 0.12,
            "storage": 0.10, "psu": 0.06, "cooler": 0.04},
    ]

    cpus = price_list_for_category("cpu")
    gpus = price_list_for_category("gpu")
    mobos = price_list_for_category("motherboard")
    rams = price_list_for_category("ram")
    storages = price_list_for_category("storage")
    psus = price_list_for_category("psu")
    coolers = price_list_for_category("cpu_cooler")

    if not cpus or not mobos or not rams:
        return None  # missing essential categories in DB

    for profile in allocation_profiles:
        budget_cpu = int(budget * profile["cpu"])
        budget_gpu = int(budget * profile["gpu"])
        budget_mobo = int(budget * profile["motherboard"])
        budget_ram = int(budget * profile["ram"])
        budget_storage = int(budget * profile["storage"])
        budget_psu = int(budget * profile["psu"])
        budget_cooler = int(budget * profile["cooler"])

        # pick CPU: choose the most expensive CPU <= budget_cpu (or if none, pick cheapest)
        cpu_choice = None
        for k, info, p in reversed(cpus):
            if p <= budget_cpu:
                cpu_choice = (k, info, p)
                break
        if not cpu_choice:
            cpu_choice = cpus[0]  # fallback to cheapest

        # pick motherboard compatible with chosen cpu
        mobo_choice = pick_motherboard_for_cpu(cpu_choice[1], mobos)
        # avoid wildly expensive mobos
        if mobo_choice and mobo_choice[2] > (budget_mobo * 2):
            # if mobo is much more than allocation, try to pick cheaper mobo of same socket
            socket = (cpu_choice[1].get("socket") or "").lower()
            candidate = None
            for k, m, p in mobos:
                if (m.get("socket") or "").lower() == socket:
                    candidate = (k, m, p)
                    break
            mobo_choice = candidate or mobo_choice

        # pick RAM that matches mobo
        ram_choice = pick_ram_for_mobo(
            mobo_choice[1], rams) if mobo_choice else rams[0]

        # pick GPU: the best GPU <= budget_gpu
        gpu_choice = None
        if gpus:
            for k, info, p in reversed(gpus):
                if p <= budget_gpu:
                    gpu_choice = (k, info, p)
                    break
            if not gpu_choice:
                # if budget too small, consider integrated (if cpu has igpu)
                if cpu_choice[1].get("igpu"):
                    gpu_choice = ("integrated graphics", {
                                  "name": "Integrated Graphics (from CPU)", "type": "GPU", "price": "₱0"}, 0)
                else:
                    gpu_choice = gpus[0]  # fallback cheapest discrete GPU

        # pick storage: cheapest NVMe or SATA within allocation
        storage_choice = None
        for k, info, p in reversed(storages):
            if p <= budget_storage:
                storage_choice = (k, info, p)
                break
        if not storage_choice and storages:
            storage_choice = storages[0]

        # pick PSU: smallest PSU >= estimated requirement if available, else cheapest adequate
        recommended_watt, suggested_psu_size = estimate_psu_requirement(
            cpu_choice[1], gpu_choice[1])
        # find a PSU >= suggested_psu_size and within budget_psu*3 (allow flexibility)
        psu_choice = None
        for k, info, p in psus:
            watt = parse_watts(info.get("wattage"))
            if watt and watt >= suggested_psu_size and p <= max(budget_psu * 3, budget * 0.15):
                psu_choice = (k, info, p)
                break
        if not psu_choice and psus:
            # fallback to most powerful available within entire budget or cheapest
            for k, info, p in reversed(psus):
                watt = parse_watts(info.get("wattage"))
                if watt and p <= budget:
                    psu_choice = (k, info, p)
                    break
            if not psu_choice:
                psu_choice = psus[0]

        # pick cooler if CPU TDP high or budget allows
        cooler_choice = None
        cpu_tdp = parse_watts(cpu_choice[1].get("tdp"))
        if coolers:
            if cpu_tdp and cpu_tdp > 95:
                # prefer 240/360 liquid if available and within budget_cooler*3
                for k, info, p in coolers:
                    size = info.get("size", "")
                    if "240" in str(size) or "360" in str(size):
                        cooler_choice = (k, info, p)
                        break
            if not cooler_choice:
                # pick cheapest cooler
                cooler_choice = coolers[0]

        # compute totals and verify total <= budget (allow small margin)
        choices = [cpu_choice, gpu_choice, mobo_choice,
                   ram_choice, storage_choice, psu_choice, cooler_choice]
        # ensure none are None
        if any(c is None for c in choices):
            continue

        total_price = sum(int(c[2]) for c in choices if c and c[2] is not None)
        # allow up to 5% over budget to get better fit
        if total_price <= budget * 1.05:
            # assemble result dict
            build = {
                "cpu": cpu_choice,
                "gpu": gpu_choice,
                "motherboard": mobo_choice,
                "ram": ram_choice,
                "storage": storage_choice,
                "psu": psu_choice,
                "cooler": cooler_choice,
                "total": total_price,
                "recommended_psu_watt": recommended_watt,
                "suggested_psu_size": suggested_psu_size,
            }
            return build

    # if no profile produced a valid build, return None
    return None


def format_build_output(build, budget=None):
    """Return a short readable string describing the assembled build, with only overall price."""
    if not build:
        return "I couldn't find a compatible build within that budget using the local data."

    def mk(name_tup):
        k, info, p = name_tup
        price_str = format_php(p) if p is not None else "N/A"
        return f"{info.get('name', k)} ({price_str})"

    total = build.get("total", 0)
    suggested_psu = build.get("suggested_psu_size")

    lines = []
    lines.append("\n🤖 ARIA — PC Build Recommendation:\n")
    if budget:
        lines.append(f"Budget target: {format_php(budget)}\n")
    lines.append(f"Overall price: {format_php(total)}")
    lines.append("\n" + "-" * 60)
    lines.append(f"CPU: {mk(build['cpu'])}")
    lines.append(f"Motherboard: {mk(build['motherboard'])}")
    lines.append(f"GPU: {mk(build['gpu'])}")
    lines.append(f"RAM: {mk(build['ram'])}")
    lines.append(f"Storage: {mk(build['storage'])}")
    lines.append(
        f"PSU: {mk(build['psu'])}  • Recommended PSU size: {suggested_psu}W")
    if build.get("cooler"):
        lines.append(f"CPU Cooler: {mk(build['cooler'])}")
    lines.append("-" * 60)
    lines.append("Short rationale:")
    lines.append(
        "• Components chosen from local DB to maximize performance while matching sockets and RAM type.")
    lines.append("• PSU suggested based on CPU/GPU TDPs + headroom.")
    return "\n".join(lines) + "\n\n"


def handle_build_request(user_query):
    """
    Entry point for build planning:
    - If user gives explicit budget, use it.
    - If user asks 'budget build' or 'entry-level', map to tier ranges and propose a budget midpoint.
    """
    low = user_query.lower()
    budget = parse_budget_from_text(user_query)

    # if user mentions tier words, map to tier midpoint
    if budget is None:
        if any(w in low for w in ["budget build", "budget", "₱15k", "15k", "15,000"]):
            low_tier = BUILD_TIERS["budget"]
            budget = (low_tier[0] + low_tier[1]) // 2
        elif any(w in low for w in ["entry-level", "entry level", "entry", "25k", "30k", "35k"]):
            low_tier = BUILD_TIERS["entry"]
            budget = (low_tier[0] + low_tier[1]) // 2
        elif any(w in low for w in ["mid", "mid-range", "mid range", "40k", "50k", "60k"]):
            low_tier = BUILD_TIERS["mid"]
            budget = (low_tier[0] + low_tier[1]) // 2
        elif any(w in low for w in ["high", "high-end", "70k", "80k", "100k"]):
            low_tier = BUILD_TIERS["high"]
            budget = max(70000, low_tier[0])

        if budget is None:
            msg = "Please specify a budget (e.g., '₱25k' or 'Recommend a build for ₱40,000')."
            print("\n🤖 ARIA — Build Planner:\n" + msg + "\n\n" + "-"*60 + "\n")
            return

    # assemble build
    build = assemble_build_for_budget(budget)
    output = format_build_output(build, budget)
    print(output)


# -------------------------------
# 🔍 find_component (robust, explained)
# -------------------------------

def find_component(query):
    """
    Match the user query against components using token overlap + difflib fuzzy matching.
    Debug-print tokens and best matches to help diagnose matching problems.
    Returns list of (category, info, key).
    """
    if not query:
        return []

    q = query.lower().strip()
    # ensure tokens defined before any debug prints
    q_tokens = normalize_text(q)

    # DEBUG: show tokens produced from user query
    # print(f"[DEBUG] find_component tokens: {q_tokens}")

    # small noise filter (keeps important tokens like '5600x', 'i7', 'rtx')
    noise = {"tell", "me", "about", "the", "details", "specs", "information", "show",
             "is", "are", "with", "for", "what", "which", "of", "in", "how", "many",
             "give", "can", "you", "please", "a", "an"}

    query_tokens_filtered = [t for t in q_tokens if t not in noise]
    if not query_tokens_filtered:
        # still return empty and debug
       # print(f"[DEBUG] find_component: no significant tokens after filtering.")
        return []

    candidates = []
    for category, items in data.items():
        for key, info in items.items():
            key_normalized = key.lower()
            name_normalized = (info.get("name") or "").lower()

            # token overlap score (simple)
            key_tokens = normalize_text(key_normalized)
            name_tokens = normalize_text(name_normalized)
            combined = set(key_tokens + name_tokens)
            overlap = sum(1 for t in query_tokens_filtered if t in combined)
            token_score = overlap / max(1, len(set(query_tokens_filtered)))

            # fuzzy ratio fallback
            key_ratio = difflib.SequenceMatcher(
                None, q, key_normalized).ratio()
            name_ratio = difflib.SequenceMatcher(
                None, q, name_normalized).ratio()
            fuzzy_score = max(key_ratio, name_ratio)

            # composite score (weights can be tuned)
            score = (token_score * 0.7) + (fuzzy_score * 0.3)

            if score > 0.18:
                candidates.append((score, category, info, key))

    candidates.sort(key=lambda x: x[0], reverse=True)
    matches = [(cat, inf, k) for _, cat, inf, k in candidates]

    # DEBUG: show the keys matched (in order)
    # show up to first 6
    # print(f"[DEBUG] find_component matches: {[m[2] for m in matches[:6]]}")

    return matches

# -------------------------------
# 🔎 Local single-field response
# -------------------------------


def respond_from_local(component_key, info, user_query):
    """
    Return single-field answers from local JSON when user requests a specific attribute.
    Prints the answer and returns True if handled, else returns False.

    Important behavior:
    - If the user asks for "details", "specs", "information", etc. we return False
      so the caller can show full specs (ask_gemini or local fallback).
    """
    if not user_query or not info:
        return False

    q = user_query.lower()
    comp_name_lc = (info.get("name") or component_key).lower()

    # If user explicitly asks for details/specs/full info, treat as NOT a single-field request.
    detail_triggers = [
        r'\bdetails?\b', r'\bspecs?\b', r'\binformation\b', r'\btell me about\b',
        r'\bshow me\b', r'\bwhat are\b.*\bdetails?\b', r'\bwhat are\b.*\bspecs?\b'
    ]
    if any(re.search(pat, q) for pat in detail_triggers):
        # Let the higher-level flow handle full details (ask_gemini or local fallback)
        return False

    # helper: word-boundary search so 'price' doesn't match 'surprise'
    def contains_word(text, word):
        return re.search(rf"\b{re.escape(word)}\b", text, flags=re.I) is not None

    # canonical field -> list of possible keys / query keywords
    field_aliases = {
        "socket": ["socket", "socket type"],
        "price": ["price", "cost", "how much", "how much is", "₱", "php", "peso"],
        "tdp": ["tdp", "tdp:", "thermal design power", "thermal"],
        "power": ["power", "wattage", "power draw", "power consumption"],
        "clock": ["clock", "boost", "boost clock", "clock speed", "ghz"],
        "cores": ["core", "cores", "threads"],
        "igpu": ["igpu", "integrated graphics", "integrated gpu"],
        "compatibility": ["compatibility", "compatible"],
        "ram": ["ram", "ram_type", "memory speed"],
        "capacity": ["capacity", "storage", "gb", "tb"],
        "slot": ["slot", "pcie", "pci-e"],
        "interface": ["interface", "sata", "nvme", "m.2"],
        "vram": ["vram", "video memory", "gpu memory"],
        "wattage": ["wattage", "watt"],
        "speed": ["speed", "mhz"],
    }

    pretty_label = {
        "socket": "Socket",
        "price": "Price",
        "tdp": "TDP",
        "power": "Power / Wattage",
        "clock": "Clock",
        "cores": "Cores / Threads",
        "igpu": "Integrated Graphics",
        "compatibility": "Compatibility",
        "ram": "RAM",
        "capacity": "Capacity",
        "slot": "Slot",
        "interface": "Interface",
        "vram": "VRAM",
        "wattage": "Wattage",
        "speed": "Speed"
    }

    # 1) Detect requested field from query with safer heuristics
    requested_field = None

    # Context indicators that raise confidence (user really asking about the field)
    context_indicators = [
        r"how many", r"how much", r"\bwhat is\b", r"\bwhat's\b", r"\bwhat are\b",
        r"\?", r":", r"\bvalue\b", r"\bsize\b", r"\bcount\b", r"\bnumber of\b"
    ]
    context_re = re.compile("|".join(context_indicators), flags=re.I)

    for field, keywords in field_aliases.items():
        for kw in keywords:
            if contains_word(q, kw):
                # If the keyword appears inside the component name (e.g., "Core i7"),
                # don't treat it as a field request unless there is extra context indicating a question.
                if kw in comp_name_lc and not context_re.search(q):
                    # skip this match because it's likely part of the model name
                    continue
                requested_field = field
                break
        if requested_field:
            break

    # Extra heuristic: if user includes currency symbol or words, assume price
    if not requested_field and ("₱" in q or "php" in q or "peso" in q or "how much" in q):
        requested_field = "price"

    component_name = info.get("name", component_key)

    if not requested_field:
        return False  # not a single-field local intent

    # 2) Try direct aliases (preferred order)
    for field_key in field_aliases.get(requested_field, []):
        # look for exact DB key matches first
        if field_key in info and info[field_key] not in (None, ""):
            val = info[field_key]
            label = pretty_label.get(requested_field, field_key.capitalize())
            output = f"\n🤖 ARIA says:\n\n{component_name}\n• {label}: {val}\n\n" + \
                "-" * 60 + "\n"
            print(output)
            try:
                add_to_history(
                    "assistant", f"{component_name} • {label}: {val}")
            except Exception:
                pass
        return True

    # 3) Try common DB keys (if alias keys differ)
    for alt in [requested_field, requested_field + "_type", requested_field + "_size"]:
        if alt in info and info[alt] not in (None, ""):
            val = info[alt]
            label = pretty_label.get(requested_field, alt.capitalize())
            output = f"\n🤖 ARIA says:\n\n{component_name}\n• {label}: {val}\n\n" + \
                "-" * 60 + "\n"
            print(output)
            try:
                add_to_history(
                    "assistant", f"{component_name} • {label}: {val}")
            except Exception:
                pass
            return True

    # 4) Fallback: look for matching keys by substring
    for k, v in info.items():
        if requested_field in k and v not in (None, ""):
            label = pretty_label.get(requested_field, k.capitalize())
            output = f"\n🤖 ARIA says:\n\n{component_name}\n• {label}: {v}\n\n" + \
                "-" * 60 + "\n"
            print(output)
            try:
                add_to_history("assistant", f"{component_name} • {label}: {v}")
            except Exception:
                pass
            return True

    # 5) Value-scan fallback for TDP/power/wattage
    if requested_field in ("tdp", "power", "wattage"):
        wpat = re.compile(r'(\d{2,4})\s*[Ww]\b')
        for k, v in info.items():
            if isinstance(v, str):
                m = wpat.search(v)
                if m:
                    val = m.group(0)
                    label = pretty_label.get(requested_field, "Wattage")
                    output = f"\n🤖 ARIA says:\n\n{component_name}\n• {label}: {val}\n\n" + \
                        "-" * 60 + "\n"
                    print(output)
                    try:
                        add_to_history(
                            "assistant", f"{component_name} • {label}: {val}")
                    except Exception:
                        pass
                    return True
        label = pretty_label.get(requested_field, requested_field.capitalize())
        output = f"\n🤖 ARIA says:\n\n{component_name}\n• {label}: This information is missing in the local database.\n\n" + "-" * 60 + "\n"
        print(output)
        try:
            add_to_history("assistant", f"{component_name} • {label}: Missing")
        except Exception:
            pass
        return True

    # 6) Numeric hints for vram/capacity/price/speed
    if requested_field in ("vram", "capacity", "price", "speed"):
        for k, v in info.items():
            if isinstance(v, str):
                if requested_field == "price":
                    pv = parse_price(v)
                    if pv:
                        output = f"\n🤖 ARIA says:\n\n{component_name}\n• Price: {format_php(pv)}\n\n" + \
                            "-" * 60 + "\n"
                        print(output)
                        try:
                            add_to_history(
                                "assistant", f"{component_name} • Price: {format_php(pv)}")
                        except Exception:
                            pass
                        return True
                if requested_field in ("vram", "capacity") and re.search(r'\b\d+\s*(GB|TB)\b', v, flags=re.I):
                    found = re.search(r'\b\d+\s*(GB|TB)\b',
                                      v, flags=re.I).group(0)
                    label = pretty_label.get(
                        requested_field, requested_field.capitalize())
                    output = f"\n🤖 ARIA says:\n\n{component_name}\n• {label}: {found}\n\n" + "-" * 60 + "\n"
                    print(output)
                    try:
                        add_to_history(
                            "assistant", f"{component_name} • {label}: {found}")
                    except Exception:
                        pass
                    return True
                if requested_field == "speed" and re.search(r'\b\d+\s*(MHz|GHz)\b', v, flags=re.I):
                    found = re.search(r'\b\d+\s*(MHz|GHz)\b',
                                      v, flags=re.I).group(0)
                    label = pretty_label.get(requested_field, "Speed")
                    output = f"\n🤖 ARIA says:\n\n{component_name}\n• {label}: {found}\n\n" + "-" * 60 + "\n"
                    print(output)
                    try:
                        add_to_history(
                            "assistant", f"{component_name} • {label}: {found}")
                    except Exception:
                        pass
                    return True

    # 7) Nothing matched
    label = pretty_label.get(requested_field, requested_field.capitalize())
    output = (f"\n🤖 ARIA says:\n\n{component_name}\n"
              f"• {label}: This information is missing in the local database.\n\n"
              + "-" * 60 + "\n")
    print(output)
    try:
        add_to_history("assistant", f"{component_name} • {label}: Missing")
    except Exception:
        pass
    return True


def respond_from_local(component_key, info, user_query):
    """
    Return single-field answers from local JSON when user requests a specific attribute.
    Prints the answer and returns True if handled, else returns False.

    Important behavior:
    - If the user asks for "details", "specs", "information", etc. we return False
      so the caller can show full specs (ask_gemini or local fallback).
    """
    if not user_query or not info:
        return False

    q = user_query.lower()
    comp_name_lc = (info.get("name") or component_key).lower()

    # If user explicitly asks for details/specs/full info, treat as NOT a single-field request.
    detail_triggers = [
        r'\bdetails?\b', r'\bspecs?\b', r'\binformation\b', r'\btell me about\b',
        r'\bshow me\b', r'\bwhat are\b.*\bdetails?\b', r'\bwhat are\b.*\bspecs?\b'
    ]
    if any(re.search(pat, q) for pat in detail_triggers):
        # Let the higher-level flow handle full details (ask_gemini or local fallback)
        return False

    # helper: word-boundary search so 'price' doesn't match 'surprise'
    def contains_word(text, word):
        return re.search(rf"\b{re.escape(word)}\b", text, flags=re.I) is not None

    # canonical field -> list of possible keys / query keywords
    field_aliases = {
        "socket": ["socket", "socket type"],
        "price": ["price", "cost", "how much", "how much is", "₱", "php", "peso"],
        "tdp": ["tdp", "tdp:", "thermal design power", "thermal"],
        "power": ["power", "wattage", "power draw", "power consumption"],
        "clock": ["clock", "boost", "boost clock", "clock speed", "ghz"],
        "cores": ["core", "cores", "threads"],
        "igpu": ["igpu", "integrated graphics", "integrated gpu"],
        "compatibility": ["compatibility", "compatible"],
        "ram": ["ram", "ram_type", "memory speed"],
        "capacity": ["capacity", "storage", "gb", "tb"],
        "slot": ["slot", "pcie", "pci-e"],
        "interface": ["interface", "sata", "nvme", "m.2"],
        "vram": ["vram", "video memory", "gpu memory"],
        "wattage": ["wattage", "watt"],
        "speed": ["speed", "mhz"],
    }

    pretty_label = {
        "socket": "Socket",
        "price": "Price",
        "tdp": "TDP",
        "power": "Power / Wattage",
        "clock": "Clock",
        "cores": "Cores / Threads",
        "igpu": "Integrated Graphics",
        "compatibility": "Compatibility",
        "ram": "RAM",
        "capacity": "Capacity",
        "slot": "Slot",
        "interface": "Interface",
        "vram": "VRAM",
        "wattage": "Wattage",
        "speed": "Speed"
    }

    # 1) Detect requested field from query with safer heuristics
    requested_field = None

    # Context indicators that raise confidence (user really asking about the field)
    context_indicators = [
        r"how many", r"how much", r"\bwhat is\b", r"\bwhat's\b", r"\bwhat are\b",
        r"\?", r":", r"\bvalue\b", r"\bsize\b", r"\bcount\b", r"\bnumber of\b"
    ]
    context_re = re.compile("|".join(context_indicators), flags=re.I)

    for field, keywords in field_aliases.items():
        for kw in keywords:
            if contains_word(q, kw):
                # If the keyword appears inside the component name (e.g., "Core i7"),
                # don't treat it as a field request unless there is extra context indicating a question.
                if kw in comp_name_lc and not context_re.search(q):
                    # skip this match because it's likely part of the model name
                    continue
                requested_field = field
                break
        if requested_field:
            break

    # Extra heuristic: if user includes currency symbol or words, assume price
    if not requested_field and ("₱" in q or "php" in q or "peso" in q or "how much" in q):
        requested_field = "price"

    component_name = info.get("name", component_key)

    if not requested_field:
        return False  # not a single-field local intent

    # 2) Try direct aliases (preferred order)
    for field_key in field_aliases.get(requested_field, []):
        # look for exact DB key matches first
        if field_key in info and info[field_key] not in (None, ""):
            val = info[field_key]
            label = pretty_label.get(requested_field, field_key.capitalize())
            output = f"\n🤖 ARIA says:\n\n{component_name}\n• {label}: {val}\n\n" + \
                "-" * 60 + "\n"
            print(output)
            try:
                add_to_history(
                    "assistant", f"{component_name} • {label}: {val}")
            except Exception:
                pass
            return True

    # 3) Try common DB keys (if alias keys differ)
    for alt in [requested_field, requested_field + "_type", requested_field + "_size"]:
        if alt in info and info[alt] not in (None, ""):
            val = info[alt]
            label = pretty_label.get(requested_field, alt.capitalize())
            output = f"\n🤖 ARIA says:\n\n{component_name}\n• {label}: {val}\n\n" + \
                "-" * 60 + "\n"
            print(output)
            try:
                add_to_history(
                    "assistant", f"{component_name} • {label}: {val}")
            except Exception:
                pass
            return True

    # 4) Fallback: look for matching keys by substring
    for k, v in info.items():
        if requested_field in k and v not in (None, ""):
            label = pretty_label.get(requested_field, k.capitalize())
            output = f"\n🤖 ARIA says:\n\n{component_name}\n• {label}: {v}\n\n" + \
                "-" * 60 + "\n"
            print(output)
            try:
                add_to_history("assistant", f"{component_name} • {label}: {v}")
            except Exception:
                pass
            return True

    # 5) Value-scan fallback for TDP/power/wattage
    if requested_field in ("tdp", "power", "wattage"):
        wpat = re.compile(r'(\d{2,4})\s*[Ww]\b')
        for k, v in info.items():
            if isinstance(v, str):
                m = wpat.search(v)
                if m:
                    val = m.group(0)
                    label = pretty_label.get(requested_field, "Wattage")
                    output = f"\n🤖 ARIA says:\n\n{component_name}\n• {label}: {val}\n\n" + \
                        "-" * 60 + "\n"
                    print(output)
                    try:
                        add_to_history(
                            "assistant", f"{component_name} • {label}: {val}")
                    except Exception:
                        pass
                    return True
        label = pretty_label.get(requested_field, requested_field.capitalize())
        output = f"\n🤖 ARIA says:\n\n{component_name}\n• {label}: This information is missing in the local database.\n\n" + "-" * 60 + "\n"
        print(output)
        try:
            add_to_history("assistant", f"{component_name} • {label}: Missing")
        except Exception:
            pass
        return True

    # 6) Numeric hints for vram/capacity/price/speed
    if requested_field in ("vram", "capacity", "price", "speed"):
        for k, v in info.items():
            if isinstance(v, str):
                if requested_field == "price":
                    pv = parse_price(v)
                    if pv:
                        output = f"\n🤖 ARIA says:\n\n{component_name}\n• Price: {format_php(pv)}\n\n" + \
                            "-" * 60 + "\n"
                        print(output)
                        try:
                            add_to_history(
                                "assistant", f"{component_name} • Price: {format_php(pv)}")
                        except Exception:
                            pass
                        return True
                if requested_field in ("vram", "capacity") and re.search(r'\b\d+\s*(GB|TB)\b', v, flags=re.I):
                    found = re.search(r'\b\d+\s*(GB|TB)\b',
                                      v, flags=re.I).group(0)
                    label = pretty_label.get(
                        requested_field, requested_field.capitalize())
                    output = f"\n🤖 ARIA says:\n\n{component_name}\n• {label}: {found}\n\n" + "-" * 60 + "\n"
                    print(output)
                    try:
                        add_to_history(
                            "assistant", f"{component_name} • {label}: {found}")
                    except Exception:
                        pass
                    return True
                if requested_field == "speed" and re.search(r'\b\d+\s*(MHz|GHz)\b', v, flags=re.I):
                    found = re.search(r'\b\d+\s*(MHz|GHz)\b',
                                      v, flags=re.I).group(0)
                    label = pretty_label.get(requested_field, "Speed")
                    output = f"\n🤖 ARIA says:\n\n{component_name}\n• {label}: {found}\n\n" + "-" * 60 + "\n"
                    print(output)
                    try:
                        add_to_history(
                            "assistant", f"{component_name} • {label}: {found}")
                    except Exception:
                        pass
                    return True

    # 7) Nothing matched
    label = pretty_label.get(requested_field, requested_field.capitalize())
    output = (f"\n🤖 ARIA says:\n\n{component_name}\n"
              f"• {label}: This information is missing in the local database.\n\n"
              + "-" * 60 + "\n")
    print(output)
    try:
        add_to_history("assistant", f"{component_name} • {label}: Missing")
    except Exception:
        pass
    return True


# Compatibility / Comparison Tools

def extract_components_from_text(query):
    q_tokens = normalize_text(query)
    matches = []
    print(f"Extracting components from query: {query}")  # Debugging line
    for category, items in data.items():
        for key, info in items.items():
            key_tokens = normalize_text(key)
            name_tokens = normalize_text(info.get("name", ""))
            combined = set(key_tokens + name_tokens)
            if not combined:
                continue
            overlap = sum(1 for t in q_tokens if t in combined)
            if overlap > 0:
                score = overlap / max(1, len(set(q_tokens)))
                matches.append((score, category, info, key))

    matches.sort(key=lambda x: x[0], reverse=True)
    return [(c, it, k) for _, c, it, k in matches]


def compare_components(user_query):
    """
    Improved compare: chooses relevant fields by category, uses aliases,
    and prints N/A for missing values instead of aborting.
    """
    found = extract_components_from_text(user_query)
    comps = []
    for cat, info, key in found:
        comps.append((cat, info, key))

    if len(comps) < 2:
        print("\n🤖 ARIA says:\n\nPlease mention two components to compare (e.g. 'compare rtx 3060 and rtx 4060').\n")
        return

    a_cat, a_info, a_key = comps[0]
    b_cat, b_info, b_key = comps[1]

    # If you still want to forbid cross-category compare, keep this:
    if a_cat != b_cat:
        print("\n🤖 ARIA says:\n\nYou cannot compare a CPU with a GPU. Please specify two CPUs or two GPUs to compare.\n")
        return

    # Relevant fields and aliases per category
    category_fields = {
        "cpu": [
            ("socket", ["socket"]),
            ("cores/threads", ["cores", "threads"]),
            ("clock", ["clock", "boost", "boost clock", "clock speed"]),
            ("tdp", ["tdp", "power", "wattage"]),
            ("igpu", ["igpu", "integrated graphics"]),
            ("price", ["price", "cost"]),
            ("compatibility", ["compatibility"])
        ],
        "gpu": [
            ("vram", ["vram", "memory"]),
            ("clock", ["clock", "boost", "boost clock"]),
            ("power", ["power", "tdp", "wattage"]),
            ("slot", ["slot"]),
            ("price", ["price", "cost"]),
            ("compatibility", ["compatibility"])
        ],
        "ram": [
            ("capacity", ["capacity"]),
            ("speed", ["speed"]),
            ("type", ["ram_type", "ram type", "ram"]),
            ("price", ["price", "cost"]),
            ("compatibility", ["compatibility"])
        ],
        "motherboard": [
            ("socket", ["socket"]),
            ("form_factor", ["form_factor", "form factor"]),
            ("ram_slots", ["ram_slots"]),
            ("ram_type", ["ram_type", "ram type"]),
            ("nvme_slots", ["nvme_slots"]),
            ("price", ["price", "cost"]),
            ("compatibility", ["compatibility"])
        ],
        "storage": [
            ("capacity", ["capacity"]),
            ("interface", ["interface"]),
            ("price", ["price", "cost"]),
            ("compatibility", ["compatibility"])
        ],
        "psu": [
            ("wattage", ["wattage", "wattage"]),
            ("efficiency", ["efficiency"]),
            ("price", ["price", "cost"]),
            ("compatibility", ["compatibility"])
        ],
        "cpu_cooler": [
            ("cooler_type", ["cooler_type", "cooler type"]),
            ("size", ["size"]),
            ("socket", ["socket"]),
            ("price", ["price", "cost"]),
            ("compatibility", ["compatibility"])
        ]
    }

    # default fallback fields if category unknown
    default_fields = [
        ("type", ["type"]), ("price", ["price", "cost"]
                             ), ("compatibility", ["compatibility"])
    ]

    fields_spec = category_fields.get(a_cat, default_fields)

    # helper to get first present alias value or None
    def get_alias_value(info_dict, aliases):
        for a in aliases:
            if a in info_dict and info_dict[a] not in (None, ""):
                return info_dict[a]
        return None

    # build header & print
    print("\n🤖 ARIA — Component Comparison:\n")
    print(f"{a_info.get('name')}  VS  {b_info.get('name')}")
    print("-" * 60)

    # print each chosen field
    for pretty_name, aliases in fields_spec:
        a_val = get_alias_value(a_info, aliases) or "N/A"
        b_val = get_alias_value(b_info, aliases) or "N/A"

        # For price, try to normalize numbers for nicer alignment
        if pretty_name in ("price",):
            a_num = parse_price(a_val) if isinstance(a_val, str) else None
            b_num = parse_price(b_val) if isinstance(b_val, str) else None
            if isinstance(a_num, int):
                a_val = format_php(a_num)
            if isinstance(b_num, int):
                b_val = format_php(b_num)

        # For cores/threads try to preserve the string; otherwise show N/A
        print(f"{pretty_name.capitalize():18} | {str(a_val):35} | {str(b_val)}")

    print("\n" + "-" * 60 + "\n")


def add_to_history(role, text, meta=None):
    """Append a new turn to the history and trim to max turns."""
    history.append({"role": role, "text": text, "meta": meta or {}})
    # keep only last N turns
    if len(history) > HISTORY_MAX_TURNS:
        del history[0: len(history) - HISTORY_MAX_TURNS]


def get_context_snippet(max_chars=1500):
    """Return a short context snippet composed from recent history (safe length)."""
    if not history:
        return ""
    # Compose recent turns (user + assistant) until reaching char limit
    out = []
    total = 0
    for turn in history[-HISTORY_MAX_TURNS:]:
        t = f"{turn['role'].upper()}: {turn['text']}\n"
        if total + len(t) > max_chars:
            break
        out.append(t)
        total += len(t)
    return "\n".join(out)


# Local / Fallback Template Helpers

def local_reply_template(kind, **kwargs):
    t = random.choice(LOCAL_TEMPLATES.get(kind, ["{text}"]))
    return t.format(**kwargs)


# -----------------------------------
# 💡 Build-request trigger phrases
# -----------------------------------
BUILD_KEYWORDS = [
    "recommend a build", "recommend build", "suggest a build", "suggest build",
    "pc build", "budget build", "build for", "entry-level build", "gaming build"
]
# Intent & Follow-up Detection


def is_build_request(user_text):
    t = (user_text or "").lower()
    # If user explicitly types a numeric budget, that's a build request too
    if parse_budget_from_text(t):
        return True
    # check for any build keyword phrase
    for kw in BUILD_KEYWORDS:
        if kw in t:
            return True
    return False


# Follow-up triggers used by needs_followup()
FOLLOWUP_TRIGGERS = [
    "compatible",
    "compatibility",
    "is it compatible",
    "is compatible",
    "compatible with",
    "fit with",
    "fit",
    "works with",
    "will it work"
]


def needs_followup(user_text):
    """Return a followup question text if request is ambiguous, else None."""
    q = (user_text or "").lower()
    # If user asks about compatibility but only mentions one item, ask which other part to compare
    if any(w in q for w in FOLLOWUP_TRIGGERS):
        # crude check: count how many component-like tokens present (model numbers, known keys)
        found_count = 0
        for cat, items in data.items():
            for key, info in items.items():
                keytok = key.lower()
                if keytok in q or (info.get("name") or "").lower() in q:
                    found_count += 1
        if found_count < 2:
            # ask which other component they mean
            return "Which other component do you want to check compatibility with? (e.g., a motherboard or GPU name)"
    # For build requests without budget, ask budget
    if is_build_request(q) and not parse_budget_from_text(q):
        # only ask if they didn't already mention a tier
        if not any(t in q for t in ["budget", "entry", "mid", "high", "₱", "php", "k"]):
            return "What's your budget or which tier do you want? (e.g., ₱25k, entry-level, mid-range)"
    return None


# Gemini API Wrapper
# -------------------------------
# 💬 Ask Gemini
# -------------------------------


def ask_gemini(user_query, found_data):
    """
    Send user question to Gemini and intelligently limit the response to relevant specs.

    - If the user asks for specific fields (socket, price, tdp, etc.) only those values are requested.
    - Otherwise ask for full structured specs.
    - Retries up to 3 times on transient failures.
    - Sanitizes, deduplicates, and formats Gemini's reply into simple bullets.
    - Prints the final formatted text and returns it (or None on failure).
    """
    # guard: ensure client exists
    try:
        _ = client
    except NameError:
        raise RuntimeError(
            "Gemini client not found. Make sure `client = genai.Client(...)` is defined.")

    context = json.dumps(found_data or {}, indent=2, ensure_ascii=False)

    # keywords that indicate the user only wants a specific detail
    keywords = [
        "socket", "price", "tdp", "power", "clock", "speed", "cores",
        "threads", "igpu", "graphics", "compatibility", "ram type",
        "form factor", "wattage", "efficiency", "capacity", "interface", "vram"
    ]
    matched_keywords = [
        kw for kw in keywords if kw in (user_query or "").lower()]

    if matched_keywords:
        focus = ", ".join(matched_keywords)
        query_mode = f"""The user only wants information about: {focus}.
Check the provided JSON and extract the exact value(s) for those attributes.
If a key exists, return only its value(s).
If a key doesn't exist, respond exactly: "This information is missing in the local database."""

    else:
        query_mode = "The user wants full details about the component. Provide full structured specs."

    # Build prompt
    system_header = (
        "You are ARIA, a helpful PC component assistant. ONLY use the JSON data provided below. "
        "Do not invent or guess values. If a requested key is missing, respond exactly: "
        "\"This information is missing in the local database.\""
    )

    prompt = f"""{system_header}

Available Data:
{context}

User Question: {user_query}

Instructions:
{query_mode}

Rules:
- Respond ONCE only.
- Do NOT repeat sentences or duplicate lines.
- Do NOT use Markdown syntax (no #, **, ``` etc.).
- Use short, simple bullet formatting (use '•' or '-' for bullets).
- If returning full details, use this structure:

Component Name
Key Specs:
• Spec: Value
Price:
• ₱value
Compatibility:
• description
Summary:
• short friendly explanation

If returning specific detail(s), return:

Component Name
• Requested Detail: Value

End response.
"""

    max_attempts = 3
    backoff = 2
    last_error = None

    for attempt in range(1, max_attempts + 1):
        try:
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt
            )

            # Try to access text attribute robustly
            text = None
            if hasattr(response, "text") and response.text:
                text = response.text
            elif hasattr(response, "output") and getattr(response, "output"):
                # some SDKs may store content in .output; try to extract
                out = getattr(response, "output")
                # naive extraction for safety:
                if isinstance(out, str):
                    text = out
                elif isinstance(out, (list, tuple)) and len(out) > 0:
                    # join textual pieces
                    text = " ".join(map(str, out))
                else:
                    text = str(out)

            if not text:
                raise ValueError("Empty response from Gemini")

            # Basic sanitization
            text = text.strip()

            # Remove excessive markdown characters or triple repeats
            text = re.sub(r'[`*_]{1,}', '', text)               # remove ` * _
            # collapse multiple blank lines
            text = re.sub(r'\n{3,}', '\n\n', text)
            # collapse multi-space
            text = re.sub(r'[ \t]{2,}', ' ', text)

            # Split to lines and normalize bullets
            raw_lines = [ln.strip() for ln in text.splitlines() if ln.strip()]

            # Convert lines like "Key: Value" into "• Key: Value" and keep existing bullets
            normalized = []
            for ln in raw_lines:
                # standardize existing bullets
                if re.match(r'^[\-\u2022]\s+', ln):
                    content = re.sub(r'^[\-\u2022]\s+', '', ln)
                    normalized.append(f"• {content}")
                elif ':' in ln and len(ln.split(':', 1)[0].split()) < 6:
                    # treat "Label: Value" lines as bullets
                    parts = ln.split(':', 1)
                    label = parts[0].strip()
                    val = parts[1].strip()
                    normalized.append(f"• {label}: {val}")
                else:
                    # keep as-is (likely a header or short sentence)
                    normalized.append(ln)

            # Deduplicate adjacent repeated lines (common model repetition bug)
            deduped = []
            prev = None
            for ln in normalized:
                if ln == prev:
                    continue
                deduped.append(ln)
                prev = ln

            # Further de-duplicate by collapsing repeated blocks (if the entire block repeats)
            # simple approach: join and remove consecutive duplicate paragraphs
            final_lines = []
            seen_blocks = set()
            # group by blank-line separated paragraphs
            para = []
            for ln in deduped + [""]:  # sentinel to flush last paragraph
                if ln == "":
                    if para:
                        block = "\n".join(para)
                        if block not in seen_blocks:
                            final_lines.extend(para)
                            final_lines.append("")  # paragraph separator
                            seen_blocks.add(block)
                        para = []
                else:
                    para.append(ln)
            # remove trailing blank if present
            if final_lines and final_lines[-1] == "":
                final_lines = final_lines[:-1]

            formatted_text = "\n".join(final_lines)

            # Final small cleanup: ensure header lines (like component name) are not prefixed with bullet
            # If first line starts with '• ' and next lines contain ':', assume bulletized header — convert back
            # (But keep simple: leave as-is if uncertain)

            # Print and return
            print("\n🤖 ARIA says:\n")
            print(formatted_text + "\n")
            print("-" * 60 + "\n")
            return formatted_text

        except Exception as e:
            last_error = e
            # transient server overload message commonly contains 503 or 'overloaded'
            err_str = str(e).lower()
            if "503" in err_str or "overload" in err_str or "busy" in err_str:
                if attempt < max_attempts:
                    print(
                        f"⚠️ Gemini server busy (attempt {attempt}/{max_attempts}). Retrying in {backoff}s...")
                    time.sleep(backoff)
                    backoff *= 2
                    continue
                else:
                    print(
                        "❌ Gemini is currently overloaded. Attempting local fallback...\n")
                    break
            else:
                # non-transient error — show and return
                print(f"⚠️ Error while calling Gemini: {e}\n")
                return None

    # If we get here, all attempts failed — provide a respectful fallback using found_data
    try:
        if found_data:
            # Pretty-print the provided local data succinctly
            out_lines = [
                "⚠️ Gemini unavailable — showing local data instead:", "-" * 40]
            for cat, info in (found_data.items() if isinstance(found_data, dict) else []):
                # info may be a dict with a single component or multiple; iterate safely
                if isinstance(info, dict):
                    # if this dict looks like a single component (has 'name'), print it
                    if "name" in info:
                        name = info.get("name")
                        price = info.get("price", "N/A")
                        keys = [k for k in (
                            "socket", "vram", "cores", "clock", "tdp", "capacity", "wattage") if k in info]
                        specs = " • ".join([f"{k}: {info[k]}" for k in keys])
                        out_lines.append(f"- {name} — {specs} — {price}")
                    else:
                        # iterate inner keys
                        for subk, subinfo in info.items():
                            name = subinfo.get("name", subk)
                            price = subinfo.get("price", "N/A")
                            keys = [k for k in (
                                "socket", "vram", "cores", "clock", "tdp", "capacity", "wattage") if k in subinfo]
                            specs = " • ".join(
                                [f"{k}: {subinfo[k]}" for k in keys])
                            out_lines.append(f"- {name} — {specs} — {price}")
            out_lines.append("-" * 40)
            final = "\n".join(out_lines)
            print(final + "\n")
            return final
        else:
            print("❌ Gemini is unavailable and no local data to show.\n")
            return None
    except Exception as final_exc:
        print(f"⚠️ Unexpected fallback error: {final_exc}\n")
        return None


# Word Matching Utilities (used across intents)
def contains_word(haystack, word):
    """Safe word-boundary check (case-insensitive)."""
    return re.search(rf"\b{re.escape(word)}\b", haystack, flags=re.I) is not None


def contains_any(haystack, words):
    return any(contains_word(haystack, w) for w in words)


# Main Program Loop (Interactive Chat)
if __name__ == "__main__":
    print("🤖 ARIA YOUR ASSISTANT ")
    print("Ask about any component (e.g. 'Ryzen 5 5600X', 'RTX 4060', 'MSI PRO X670-P WIFI').")
    print("Type 'exit' to quit.\n")

    # Trigger lists used throughout the loop (defined once)
    comp_triggers = ["compatible", "compatibility", "is compatible", "compatible with",
                     "fit with", "works with", "work with", "will work", "will it work", "will"]
    psu_triggers_quick = ["psu", "power supply", "power recommendation", "watt",
                          "wattage", "power draw", "how much watt", "how much wattage"]
    compare_triggers = [" vs ", " vs. ",
                        " versus ", " compare ", " compare to "]
    recommend_triggers = ["recommend a build", "build for", "suggest a build",
                          "pc build", "budget build", "recommend build", "suggest build"]

    while True:
        try:
            user_input = input("You: ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\n👋 Goodbye!")
            break

        if not user_input:
            continue

        low = user_input.lower().strip()

        # exit
        if low in ["exit", "quit", "bye"]:
            print("👋 Goodbye!")
            break

        # store user turn in history if available
        try:
            add_to_history("user", user_input)
        except Exception:
            pass

        # ----- 1) Try component lookup (local-first) -----
        matches = find_component(user_input)
        if matches:
            print(f"[DEBUG] find_component matches: {[m[2] for m in matches]}")
            # if the query looks like a compatibility question and we found components,
            # handle compatibility immediately
            if contains_any(low, comp_triggers):
                try:
                    if re.search(r'\b(work|works|will)\b.*\bwith\b', low) or contains_any(low, comp_triggers):
                        handled = check_compatibility(user_input)
                    if handled:
                        continue
                except Exception as e:
                    print(f"⚠️ Compatibility handler error: {e}\n")
                    # fall through to normal handling

            # pick best match (first)
            category, info, component_key = matches[0]

            # respond from local DB for single-field intents (price/socket/tdp etc.)
            try:
                handled = respond_from_local(component_key, info, user_input)
            except Exception as e:
                handled = False
                print(f"⚠️ Local response error: {e}")

            if handled:
                continue

            # otherwise try Gemini (or local fallback)
            try:
                ask_gemini(user_input, {category: info})
            except Exception as e:
                # graceful fallback to local summary
                print(f"⚠️ Error while querying Gemini: {e}\n")
                try:
                    name = info.get("name", component_key)
                    price = info.get("price", "N/A")
                    keys = [k for k in (
                        "socket", "vram", "cores", "clock", "tdp", "capacity", "wattage") if k in info]
                    specs = " • ".join([f"{k}: {info[k]}" for k in keys])
                    print(
                        f"\n🤖 ARIA says (local fallback):\n{name}\n{specs}\nPrice: {price}\n\n" + "-" * 60 + "\n")
                except Exception:
                    print("⚠️ Unable to show local fallback data.\n")
            continue

        # ----- 2) Quick PSU/wattage handler (before education/build) -----
        if contains_any(low, psu_triggers_quick):
            follow = needs_followup(user_input)
            if follow:
                try:
                    add_to_history("assistant", follow)
                except Exception:
                    pass
                print("\n🤖 ARIA — Quick question:\n" + follow + "\n")
                continue
            try:
                handle_psu_request(user_input)
            except Exception as e:
                print(f"⚠️ PSU handler error: {e}\n")
            continue

        # ----- 3) Permissive component detection to avoid mis-classifying educational queries -----
        permissive_found = extract_components_from_text(user_input)
        if not permissive_found:
            # only treat as education if there are no component-like tokens
            if is_education_request(user_input):
                handle_education_request(user_input)
                continue

        # ----- 4) Build / budget requests -----
        if is_build_request(user_input):
            follow = needs_followup(user_input)
            if follow:
                try:
                    add_to_history("assistant", follow)
                except Exception:
                    pass
                print("\n🤖 ARIA — Quick question:\n" + follow + "\n")
                continue
            try:
                handle_build_request(user_input)
            except Exception as e:
                print(f"⚠️ Build recommendation error: {e}\n")
            continue

        # ----- 5) Compatibility / PSU / Compare / Recommend (token-aware) -----
        if contains_any(low, comp_triggers + psu_triggers_quick):
            follow = needs_followup(user_input)
            if follow:
                try:
                    add_to_history("assistant", follow)
                except Exception:
                    pass
                print("\n🤖 ARIA — Quick question:\n" + follow + "\n")
                continue
            # no follow-up needed: do compatibility check (may include PSU calc)
            try:
                check_compatibility(user_input)
            except Exception as e:
                print(f"⚠️ Compatibility check error: {e}\n")
            continue

        # ----- 6) Compare detection -----
        if any(kw in low for kw in compare_triggers) or contains_any(low, ["compare", "compare to"]):
            try:
                compare_components(user_input)
            except Exception as e:
                print(f"⚠️ Compare error: {e}\n")
            continue

        # ----- 7) Recommend/build triggers (fallback) -----
        if contains_any(low, recommend_triggers):
            follow = needs_followup(user_input)
            if follow:
                try:
                    add_to_history("assistant", follow)
                except Exception:
                    pass
                print("\n🤖 ARIA — Quick question:\n" + follow + "\n")
                continue
            try:
                handle_build_request(user_input)
            except Exception as e:
                print(f"⚠️ Build recommendation error: {e}\n")
            continue

        if handle_store_request(user_input):
            continue

        # ----- 8) Final fallback: no matches found -----
        print("⚠️ No matching component found in the database.\n")
        print("Tip: Try searching by model number or brand (e.g., '5600X', 'RTX 4060', 'MSI PRO X670').")
        try:
            add_to_history(
                "assistant", "No matching component found; suggested user try model numbers or ask to list categories.")
        except Exception:
            pass
        continue


# =============================
# 🧠 Flask Integration Function
# =============================

# near end of ARsemble_ai.py — add this
# At end of ARSEMBLE_AI.py (after all functions)

def handle_query(user_input):
    """Return a full textual reply string. Adds debug logging to stderr."""
    debug_prefix = f"[{datetime.datetime.now().isoformat()}] [handle_query] "
    # small debug to stderr (visible in server logs)
    print(debug_prefix + "Received input: " +
          repr(user_input), file=sys.stderr)

    if not user_input or not str(user_input).strip():
        return "Please enter a question."

    # capture printed output
    buf = io.StringIO()
    old_stdout = sys.stdout
    try:
        sys.stdout = buf
        # reuse your existing flow — this is same logic as CLI but returns string
        low = user_input.lower().strip()

        # component lookup (local-first)
        matches = find_component(user_input)
        if matches:
            # if compatibility wording present, check compatibility first
            comp_triggers_local = [" compatible ", "compatibility", "is compatible",
                                   "compatible with", "fit with", "works with", "is it compatible"]
            if contains_any(low, comp_triggers_local):
                try:
                    handled = check_compatibility(user_input)
                    if handled:
                        return buf.getvalue()
                except Exception as e:
                    print(f"⚠️ Compatibility handler error: {e}\n")

            category, info, component_key = matches[0]
            try:
                handled = respond_from_local(component_key, info, user_input)
            except Exception as e:
                handled = False
                print(f"⚠️ Local response error: {e}")

            if handled:
                return buf.getvalue()

            try:
                ask_gemini(user_input, {category: info})
            except Exception as e:
                print(f"⚠️ Error while querying Gemini: {e}\n")
                try:
                    name = info.get("name", component_key)
                    price = info.get("price", "N/A")
                    keys = [k for k in (
                        "socket", "vram", "cores", "clock", "tdp", "capacity", "wattage") if k in info]
                    specs = " • ".join([f"{k}: {info[k]}" for k in keys])
                    print(
                        f"\n🤖 ARIA says (local fallback):\n{name}\n{specs}\nPrice: {price}\n\n" + "-" * 60 + "\n")
                except Exception:
                    print("⚠️ Unable to show local fallback data.\n")
            return buf.getvalue()

        # Quick PSU handler
        psu_triggers_quick = ["psu", "power supply", "power recommendation", "watt",
                              "wattage", "power draw", "how much watt", "how much wattage"]
        if contains_any(low, psu_triggers_quick):
            follow = needs_followup(user_input)
            if follow:
                print("\n🤖 ARIA — Quick question:\n" + follow + "\n")
                return buf.getvalue()
            try:
                handle_psu_request(user_input)
            except Exception as e:
                print(f"⚠️ PSU handler error: {e}\n")
            return buf.getvalue()

        # Education
        permissive_found = extract_components_from_text(user_input)
        if not permissive_found:
            if is_education_request(user_input):
                handle_education_request(user_input)
                return buf.getvalue()

        # Build
        if is_build_request(user_input):
            follow = needs_followup(user_input)
            if follow:
                print("\n🤖 ARIA — Quick question:\n" + follow + "\n")
                return buf.getvalue()
            handle_build_request(user_input)
            return buf.getvalue()

        # Compatibility / compare
        comp_triggers = [" compatible ", "compatibility", "is compatible",
                         "compatible with", "fit with", "works with", "is it compatible"]
        if contains_any(low, comp_triggers + psu_triggers_quick):
            follow = needs_followup(user_input)
            if follow:
                print("\n🤖 ARIA — Quick question:\n" + follow + "\n")
                return buf.getvalue()
            try:
                check_compatibility(user_input)
            except Exception as e:
                print(f"⚠️ Compatibility check error: {e}\n")
            return buf.getvalue()

        # Compare
        if any(kw in low for kw in [" vs ", " vs. ", " versus "]) or contains_any(low, ["compare", "compare to"]):
            try:
                compare_components(user_input)
            except Exception as e:
                print(f"⚠️ Compare error: {e}\n")
            return buf.getvalue()

        # Recommend/build
        recommend_triggers = ["recommend a build", "build for", "suggest a build",
                              "pc build", "budget build", "recommend build", "suggest build"]
        if contains_any(low, recommend_triggers):
            follow = needs_followup(user_input)
            if follow:
                print("\n🤖 ARIA — Quick question:\n" + follow + "\n")
                return buf.getvalue()
            try:
                handle_build_request(user_input)
            except Exception as e:
                print(f"⚠️ Build recommendation error: {e}\n")
            return buf.getvalue()

        # fallback
        print("⚠️ No matching component found in the database.\n")
        print("Tip: Try searching by model number or brand (e.g., '5600X', 'RTX 4060', 'MSI PRO X670').")
        return buf.getvalue()

    finally:
        sys.stdout = old_stdout
