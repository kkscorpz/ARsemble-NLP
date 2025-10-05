from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet

# =====================================================================
# GPU Database (NEW)
# =====================================================================
gpus = {
    "rtx 3050": {
        "name": "Gigabyte RTX 3050 EAGLE OC",
        "vram": "8GB GDDR6",
        "clockSpeed": "~1777 MHz (Boost)",
        "powerConsumption": "~130 Watts",
        "slotType": "PCIe 4.0 x16",
        "compatibility": "Requires a motherboard with an available PCIe x16 slot (compatible with PCIe 3.0/4.0/5.0). Needs a PSU with sufficient wattage (450W-550W recommended total system power) and at least one 8-pin PCIe power connector. Ensure your case has enough physical clearance."
    },
    "rtx 4060": {
        "name": "MSI RTX 4060 GAMING X",
        "vram": "8GB GDDR6",
        "clockSpeed": "~2595 MHz (Boost)",
        "powerConsumption": "~115 Watts",
        "slotType": "PCIe 4.0 x8",
        "compatibility": "Requires a motherboard with an available PCIe x16 slot. Needs a 550W+ PSU with one 8-pin PCIe power connector. Compatible with modern cases."
    },
    "rx 9060 xt 8gb": {
        "name": "Gigabyte RX 9060 XT Gaming OC",
        "vram": "8GB GDDR6",
        "clockSpeed": "~2200 MHz (Boost)",
        "powerConsumption": "~180 Watts",
        "slotType": "PCIe 4.0 x16",
        "compatibility": "Requires PCIe x16 slot. Recommended 600W PSU with 2x 8-pin PCIe connectors. Ensure your case supports full-length GPUs."
    },
    "gtx 750 ti": {
        "name": "NVIDIA GTX 750 Ti",
        "vram": "4GB GDDR5",
        "clockSpeed": "~1085 MHz (Boost)",
        "powerConsumption": "~60 Watts",
        "slotType": "PCIe 3.0 x16",
        "compatibility": "Very low power draw (300W PSU recommended). Single 6-pin PCIe power connector or none depending on model. Fits in most cases due to compact size."
    },
    "rtx 3060": {
        "name": "MSI RTX 3060",
        "vram": "12GB GDDR6",
        "clockSpeed": "~1777 MHz (Boost)",
        "powerConsumption": "~170 Watts",
        "slotType": "PCIe 4.0 x16",
        "compatibility": "Needs PCIe x16 slot and 550W+ PSU. Requires 1x 8-pin PCIe power connector. Ensure case has enough clearance."
    },
    "rx 9060 xt 16gb": {
        "name": "Sapphire RX 9060 XT",
        "vram": "16GB GDDR6",
        "clockSpeed": "~2400 MHz (Boost)",
        "powerConsumption": "~220 Watts",
        "slotType": "PCIe 4.0 x16",
        "compatibility": "Requires PCIe x16 slot, 650W+ PSU with 2x 8-pin PCIe connectors. Ensure case supports large GPUs with proper cooling."
    }
}

gpuModelMap = {
    # RTX 3050
    "gigabyte rtx 3050 eagle oc": "rtx 3050",
    "rtx 3050 eagle oc": "rtx 3050",
    "gigabyte 3050": "rtx 3050",
    "rtx 3050": "rtx 3050",
    "3050 eagle oc": "rtx 3050",
    "3050": "rtx 3050",

    # RTX 4060
    "msi rtx 4060 gaming x": "rtx 4060",
    "rtx 4060 gaming x": "rtx 4060",
    "msi 4060": "rtx 4060",
    "rtx 4060": "rtx 4060",
    "4060 gaming x": "rtx 4060",
    "4060": "rtx 4060",

    # RX 9060 XT 8GB
    "gigabyte rx 9060 xt gaming oc": "rx 9060 xt 8gb",
    "rx 9060 xt gaming oc": "rx 9060 xt 8gb",
    "gigabyte rx 9060": "rx 9060 xt 8gb",
    "rx 9060 xt 8gb": "rx 9060 xt 8gb",
    "rx 9060 xt": "rx 9060 xt 8gb",

    # GTX 750 Ti
    "gtx 750 ti": "gtx 750 ti",
    "nvidia gtx 750 ti": "gtx 750 ti",
    "750 ti": "gtx 750 ti",

    # RTX 3060
    "msi rtx 3060": "rtx 3060",
    "rtx 3060": "rtx 3060",
    "3060": "rtx 3060",

    # RX 9060 XT 16GB
    "sapphire rx 9060 xt": "rx 9060 xt 16gb",
    "rx 9060 xt 16gb": "rx 9060 xt 16gb",
    "rx 9060 xt sapphire": "rx 9060 xt 16gb",
    "rx 9060 xt": "rx 9060 xt 16gb" 
}


# =====================================================================
# CPU Database (Carried over)
# =====================================================================
cpus = {
    "intel core i9-14900k": {
        "name": "Intel Core i9-14900K",
        "price": "₱39,000",
        "socket": "LGA 1700",
        "baseClock": "3.2 GHz (P), 2.4 GHz (E)",
        "coresThreads": "24 cores (8P + 16E), 32 threads",
        "tdp": "125W TDP / 253W max",
        "compatibility": "Intel 600/700 series chipsets, BIOS update may be needed, Z790 recommended, requires strong cooling (240mm+), 750W+ PSU"
    },
    "intel core i7-14700k": {
        "name": "Intel Core i7-14700K",
        "price": "₱29,000",
        "socket": "LGA 1700",
        "baseClock": "3.4 GHz (P), 2.5 GHz (E)",
        "coresThreads": "20 cores (8P + 12E), 28 threads",
        "tdp": "125W TDP / 253W max",
        "compatibility": "Z790 or B760, high-performance cooling, 750W+ PSU"
    },
    "intel core i7-13700k": {
        "name": "Intel Core i7-13700K",
        "price": "₱25,000",
        "socket": "LGA 1700",
        "baseClock": "~3.4 GHz (P), ~2.5 GHz (E)",
        "coresThreads": "16 cores (8P + 8E), 24 threads",
        "tdp": "125W TDP / 253W max",
        "compatibility": "Z790 or B760, strong cooling, 700W+ PSU"
    },
    "intel core i5-14600k": {
        "name": "Intel Core i5-14600K",
        "price": "₱19,000",
        "socket": "LGA 1700",
        "baseClock": "3.5 GHz (P), 2.6 GHz (E)",
        "coresThreads": "14 cores (6P + 8E), 20 threads",
        "tdp": "125W TDP / 181W max",
        "compatibility": "B760 or Z790, mid to high-end cooling, 650W+ PSU"
    },
    "intel core i5-14500": {
        "name": "Intel Core i5-14500",
        "price": "₱15,000",
        "socket": "LGA 1700",
        "baseClock": "2.6 GHz (P), 1.9 GHz (E)",
        "coresThreads": "14 cores (6P + 8E), 20 threads",
        "tdp": "65W TDP / 154W max",
        "compatibility": "B760 or H610, basic cooling, 550W+ PSU"
    },
    "intel core i5-13400": {
        "name": "Intel Core i5-13400",
        "price": "₱13,000",
        "socket": "LGA 1700",
        "baseClock": "2.5 GHz (P), 1.8 GHz (E)",
        "coresThreads": "10 cores (6P + 4E), 16 threads",
        "tdp": "65W TDP / 148W max",
        "compatibility": "H610 or B760, basic cooling, 500W+ PSU"
    },
    "intel core i3-14100": {
        "name": "Intel Core i3-14100",
        "price": "₱8,000",
        "socket": "LGA 1700",
        "baseClock": "3.5 GHz (P)",
        "coresThreads": "4 cores (P only), 8 threads",
        "tdp": "60W TDP / 110W max",
        "compatibility": "H610 or B760, stock or basic cooling, 450W+ PSU"
    },
    "intel core i3-13100": {
        "name": "Intel Core i3-13100",
        "price": "₱7,500",
        "socket": "LGA 1700",
        "baseClock": "3.4 GHz (P)",
        "coresThreads": "4 cores, 8 threads",
        "tdp": "60W TDP / ~89W max",
        "compatibility": "H610 or B760, stock or basic cooling, 450W+ PSU"
    },
    "amd ryzen 9 7950x": {
        "name": "AMD Ryzen 9 7950X",
        "price": "₱34,000",
        "socket": "AM5",
        "baseClock": "4.5 GHz",
        "coresThreads": "16 cores / 32 threads",
        "tdp": "170W TDP / 230W max",
        "compatibility": "AM5 boards (X670E/X670/B650E), DDR5 only, 360mm+ AIO, 850W+ PSU"
    },
    "amd ryzen 9 9900x": {
        "name": "AMD Ryzen 9 9900X",
        "price": "TBD",
        "socket": "AM5 (expected)",
        "baseClock": "TBD",
        "coresThreads": "TBD",
        "tdp": "TBD",
        "compatibility": "Expected AM5 + DDR5 + high cooling"
    },
    "amd ryzen 9 9900x3d": {
        "name": "AMD Ryzen 9 9900X3D",
        "price": "TBD",
        "socket": "AM5 (expected)",
        "baseClock": "TBD",
        "coresThreads": "TBD",
        "tdp": "TBD",
        "compatibility": "Expected AM5, DDR5, advanced cooling due to 3D V-Cache"
    },
    "amd ryzen 7 7700x": {
        "name": "AMD Ryzen 7 7700X",
        "price": "₱21,000",
        "socket": "AM5",
        "baseClock": "4.5 GHz",
        "coresThreads": "8 cores / 16 threads",
        "tdp": "105W TDP",
        "compatibility": "AM5 only, DDR5 only, 240mm AIO or mid-high air cooling, 650W+ PSU"
    },
    "amd ryzen 7 5700x": {
        "name": "AMD Ryzen 7 5700X",
        "price": "₱14,000",
        "socket": "AM4",
        "baseClock": "3.4 GHz",
        "coresThreads": "8 cores / 16 threads",
        "tdp": "65W TDP",
        "compatibility": "AM4 boards (B550, X570), DDR4, BIOS update may be needed, 550W+ PSU"
    },
    "amd ryzen 5 5600x": {
        "name": "AMD Ryzen 5 5600X",
        "price": "₱11,000",
        "socket": "AM4",
        "baseClock": "3.7 GHz",
        "coresThreads": "6 cores / 12 threads",
        "tdp": "65W TDP",
        "compatibility": "AM4 DDR4, B550/X570, basic to mid-air cooling, 550W+ PSU"
    },
    "amd ryzen 5 5600g": {
        "name": "AMD Ryzen 5 5600G",
        "price": "₱9,000",
        "socket": "AM4",
        "baseClock": "3.9 GHz",
        "coresThreads": "6 cores / 12 threads",
        "tdp": "65W TDP",
        "compatibility": "AM4 DDR4, integrated GPU, stock cooling OK, 450W+ PSU"
    },
    "amd ryzen 3 3200g": {
        "name": "AMD Ryzen 3 3200G",
        "price": "₱5,000",
        "socket": "AM4",
        "baseClock": "3.6 GHz",
        "coresThreads": "4 cores / 4 threads",
        "tdp": "65W TDP",
        "compatibility": "AM4, Vega graphics, stock cooler OK, 400W+ PSU"
    }
}

cpuModelMap = {
    "intel core i9-14900k": "intel core i9-14900k", "core i9-14900k": "intel core i9-14900k", "i9-14900k": "intel core i9-14900k", "intel i9-14900k": "intel core i9-14900k", "14900k": "intel core i9-14900k", "intel core i9 14900k": "intel core i9-14900k", "core i9 14900k": "intel core i9-14900k", "i9 14900k": "intel core i9-14900k",
    "intel core i7-14700k": "intel core i7-14700k", "core i7-14700k": "intel core i7-14700k", "i7-14700k": "intel core i7-14700k", "intel i7-14700k": "intel core i7-14700k", "14700k": "intel core i7-14700k", "intel core i7 14700k": "intel core i7-14700k", "core i7 14700k": "intel core i7-14700k", "i7 14700k": "intel core i7-14700k",
    "intel core i7-13700k": "intel core i7-13700k", "core i7-13700k": "intel core i7-13700k", "i7-13700k": "intel core i7-13700k", "intel i7-13700k": "intel core i7-13700k", "13700k": "intel core i7-13700k", "intel core i7 13700k": "intel core i7-13700k", "core i7 13700k": "intel core i7-13700k", "i7 13700k": "intel core i7-13700k",
    "intel core i5-14600k": "intel core i5-14600k", "core i5-14600k": "intel core i5-14600k", "i5-14600k": "intel core i5-14600k", "intel i5-14600k": "intel core i5-14600k", "14600k": "intel core i5-14600k", "intel core i5 14600k": "intel core i5-14600k", "core i5 14600k": "intel core i5-14600k", "i5 14600k": "intel core i5-14600k",
    "intel core i5-14500": "intel core i5-14500", "core i5-14500": "intel core i5-14500", "i5-14500": "intel core i5-14500", "intel i5-14500": "intel core i5-14500", "14500": "intel core i5-14500", "intel core i5 14500": "intel core i5-14500", "core i5 14500": "intel core i5-14500", "i5 14500": "intel core i5-14500",
    "intel core i5-13400": "intel core i5-13400", "core i5-13400": "intel core i5-13400", "i5-13400": "intel core i5-13400", "intel i5-13400": "intel core i5-13400", "13400": "intel core i5-13400", "intel core i5 13400": "intel core i5-13400", "core i5 13400": "intel core i5-13400", "i5 13400": "intel core i5-13400",
    "intel core i3-14100": "intel core i3-14100", "core i3-14100": "intel core i3-14100", "i3-14100": "intel core i3-14100", "intel i3-14100": "intel core i3-14100", "14100": "intel core i3-14100", "intel core i3 14100": "intel core i3-14100", "core i3 14100": "intel core i3-14100", "i3 14100": "intel core i3-14100",
    "intel core i3-13100": "intel core i3-13100", "core i3-13100": "intel core i3-13100", "i3-13100": "intel core i3-13100", "intel i3-13100": "intel core i3-13100", "13100": "intel core i3-13100", "intel core i3 13100": "intel core i3-13100", "core i3 13100": "intel core i3-13100", "i3 13100": "intel core i3-13100",
    "amd ryzen 9 7950x": "amd ryzen 9 7950x", "ryzen 9 7950x": "amd ryzen 9 7950x", "7950x": "amd ryzen 9 7950x", "amd 7950x": "amd ryzen 9 7950x", "ryzen9 7950x": "amd ryzen 9 7950x", "ryzen 9 7950 x": "amd ryzen 9 7950x",
    "amd ryzen 9 9900x": "amd ryzen 9 9900x", "ryzen 9 9900x": "amd ryzen 9 9900x", "9900x": "amd ryzen 9 9900x", "amd 9900x": "amd ryzen 9 9900x", "ryzen9 9900x": "amd ryzen 9 9900x", "ryzen 9 9900 x": "amd ryzen 9 9900x",
    "amd ryzen 9 9900x3d": "amd ryzen 9 9900x3d", "ryzen 9 9900x3d": "amd ryzen 9 9900x3d", "9900x3d": "amd ryzen 9 9900x3d", "amd 9900x3d": "amd ryzen 9 9900x3d", "ryzen9 9900x3d": "amd ryzen 9 9900x3d", "ryzen 9 9900 x3d": "amd ryzen 9 9900x3d",
    "amd ryzen 7 7700x": "amd ryzen 7 7700x", "ryzen 7 7700x": "amd ryzen 7 7700x", "7700x": "amd ryzen 7 7700x", "amd 7700x": "amd ryzen 7 7700x", "ryzen7 7700x": "amd ryzen 7 7700x", "ryzen 7 7700 x": "amd ryzen 7 7700x",
    "amd ryzen 7 5700x": "amd ryzen 7 5700x", "ryzen 7 5700x": "amd ryzen 7 5700x", "5700x": "amd ryzen 7 5700x", "amd 5700x": "amd ryzen 7 5700x", "ryzen7 5700x": "amd ryzen 7 5700x", "ryzen 7 5700 x": "amd ryzen 7 5700x",
    "amd ryzen 5 5600x": "amd ryzen 5 5600x", "ryzen 5 5600x": "amd ryzen 5 5600x", "5600x": "amd ryzen 5 5600x", "amd 5600x": "amd ryzen 5 5600x", "ryzen5 5600x": "amd ryzen 5 5600x", "ryzen 5 5600 x": "amd ryzen 5 5600x",
    "amd ryzen 5 5600g": "amd ryzen 5 5600g", "ryzen 5 5600g": "amd ryzen 5 5600g", "5600g": "amd ryzen 5 5600g", "amd 5600g": "amd ryzen 5 5600g", "ryzen5 5600g": "amd ryzen 5 5600g", "ryzen 5 5600 g": "amd ryzen 5 5600g",
    "amd ryzen 3 3200g": "amd ryzen 3 3200g", "ryzen 3 3200g": "amd ryzen 3 3200g", "3200g": "amd ryzen 3 3200g", "amd 3200g": "amd ryzen 3 3200g", "ryzen3 3200g": "amd ryzen 3 3200g", "ryzen 3 3200 g": "amd ryzen 3 3200g",
}


# =====================================================================
# Motherboard Database (Carried over)
# =====================================================================
motherboards = {
    "asus prime b550m-k": {
        "name": "ASUS PRIME B550M-K",
        "socket": "AM4",
        "chipset": "B550",
        "formFactor": "Micro-ATX",
        "ram": "DDR4, up to 128GB",
        "features": "PCIe 4.0, HDMI, DVI-D, Realtek audio, 1Gb LAN",
        "compatibility": "Ryzen 3000/5000 series (excluding 3200G/3400G without BIOS update)",
        "price": "₱6,500"
    },
    "msi b450m a pro max ii": {
        "name": "MSI B450M A PRO MAX II",
        "socket": "AM4",
        "chipset": "B450",
        "formFactor": "Micro-ATX",
        "ram": "DDR4, up to 64GB",
        "features": "PCIe 3.0, HDMI, DVI, USB 3.2 Gen1, basic VRM",
        "compatibility": "Supports Ryzen 1000 to 5000 series with BIOS update",
        "price": "₱4,500"
    },
    "msi pro h610m s ddr4": {
        "name": "MSI PRO H610M-S DDR4",
        "socket": "LGA 1700",
        "chipset": "H610",
        "formFactor": "Micro-ATX",
        "ram": "DDR4, up to 64GB",
        "features": "Basic IO, 1x PCIe x16, HDMI, VGA, 1Gb LAN",
        "compatibility": "Supports 12th/13th/14th Gen Intel CPUs",
        "price": "₱5,000"
    },
    "ramsta rs-b450mp": {
        "name": "RAMSTA RS-B450MP",
        "socket": "AM4",
        "chipset": "B450",
        "formFactor": "Micro-ATX",
        "ram": "DDR4, up to 64GB",
        "features": "Entry-level, basic IO ports",
        "compatibility": "Supports Ryzen 1000 to 5000 series (BIOS update may be needed)",
        "price": "₱3,800"
    },
    "ramsta rs-h311d4": {
        "name": "RAMSTA RS-H311D4",
        "socket": "LGA 1151",
        "chipset": "H310",
        "formFactor": "Micro-ATX",
        "ram": "DDR4, up to 32GB",
        "features": "Legacy board, VGA/HDMI, USB 3.0",
        "compatibility": "Supports Intel 8th/9th Gen CPUs (Coffee Lake)",
        "price": "₱2,900"
    },
    "msi b650m gaming plus wifi": {
        "name": "MSI B650M Gaming Plus WiFi",
        "socket": "AM5",
        "chipset": "B650",
        "formFactor": "Micro-ATX",
        "ram": "DDR5, up to 128GB",
        "features": "WiFi 6E, PCIe 4.0, 2.5Gb LAN, USB-C",
        "compatibility": "Supports Ryzen 7000/8000 series",
        "price": "₱12,500"
    },
    "msi b760m gaming plus wifi ddr4": {
        "name": "MSI B760M Gaming Plus WiFi DDR4",
        "socket": "LGA 1700",
        "chipset": "B760",
        "formFactor": "Micro-ATX",
        "ram": "DDR4, up to 128GB",
        "features": "PCIe 5.0, WiFi 6, HDMI/DP, 2.5Gb LAN",
        "compatibility": "Supports Intel 12th/13th/14th Gen CPUs",
        "price": "₱8,000"
    },
    "gigabyte h610m k ddr4": {
        "name": "GIGABYTE H610M K DDR4",
        "socket": "LGA 1700",
        "chipset": "H610",
        "formFactor": "Micro-ATX",
        "ram": "DDR4, up to 64GB",
        "features": "HDMI, VGA, Realtek audio, PCIe 4.0",
        "compatibility": "Supports Intel 12th/13th/14th Gen CPUs",
        "price": "₱4,800"
    }
}

motherboardModelMap = {
    "asus prime b550m-k": "asus prime b550m-k", "prime b550m-k": "asus prime b550m-k", "b550m-k": "asus prime b550m-k", "asus b550m-k": "asus prime b550m-k",
    "msi b450m a pro max ii": "msi b450m a pro max ii", "b450m a pro max ii": "msi b450m a pro max ii", "msi b450m-a pro max ii": "msi b450m a pro max ii", "b450m-a pro max ii": "msi b450m a pro max ii", "msi b450m-a": "msi b450m a pro max ii",
    "msi pro h610m s ddr4": "msi pro h610m s ddr4", "pro h610m s ddr4": "msi pro h610m s ddr4", "h610m s ddr4": "msi pro h610m s ddr4", "msi h610m-s ddr4": "msi pro h610m s ddr4",
    "ramsta rs-b450mp": "ramsta rs-b450mp", "rs-b450mp": "ramsta rs-b450mp", "ramsta b450mp": "ramsta rs-b450mp",
    "ramsta rs-h311d4": "ramsta rs-h311d4", "rs-h311d4": "ramsta rs-h311d4", "ramsta h311d4": "ramsta rs-h311d4", "rs h311d4": "ramsta rs-h311d4",
    "msi b650m gaming plus wifi": "msi b650m gaming plus wifi", "b650m gaming plus wifi": "msi b650m gaming plus wifi", "msi b650m wifi": "msi b650m gaming plus wifi",
    "msi b760m gaming plus wifi ddr4": "msi b760m gaming plus wifi ddr4", "b760m gaming plus wifi ddr4": "msi b760m gaming plus wifi ddr4", "msi b760m wifi ddr4": "msi b760m gaming plus wifi ddr4", "b760m gaming plus": "msi b760m gaming plus wifi ddr4",
    "gigabyte h610m k ddr4": "gigabyte h610m k ddr4", "h610m k ddr4": "gigabyte h610m k ddr4", "gigabyte h610m ddr4": "gigabyte h610m k ddr4", "h610m k": "gigabyte h610m k ddr4"
}


# =====================================================================
# Case Fan Database (Carried over)
# =====================================================================
case_fans = {
    "coolmoon yx120": {
        "name": "COOLMOON YX120",
        "size": "120mm",
        "rpm": "1200 RPM",
        "airflow": "38 CFM",
        "noise": "20 dBA",
        "rgb": "Addressable RGB",
        "price": "₱250"
    },
    "cooler master sickleflow 120 argb": {
        "name": "Cooler Master SickleFlow 120 ARGB",
        "size": "120mm",
        "rpm": "650-1800 RPM",
        "airflow": "62 CFM",
        "noise": "8-27 dBA",
        "rgb": "Addressable RGB",
        "price": "₱600"
    },
    "arctic p12 pwm pst": {
        "name": "Arctic P12 PWM PST",
        "size": "120mm",
        "rpm": "200-1800 RPM",
        "airflow": "56.3 CFM",
        "noise": "0.3 Sone",
        "rgb": "No RGB",
        "price": "₱450"
    }
}

caseFanModelMap = {
    "coolmoon yx120": "coolmoon yx120", "yx120": "coolmoon yx120", "coolmoon fan": "coolmoon yx120", "coolmoon yx120 fan": "coolmoon yx120",
    "cooler master sickleflow 120 argb": "cooler master sickleflow 120 argb", "sickleflow 120 argb": "cooler master sickleflow 120 argb", "cooler master sickleflow": "cooler master sickleflow 120 argb", "sickleflow argb": "cooler master sickleflow 120 argb", "sickleflow 120": "cooler master sickleflow 120 argb",
    "arctic p12 pwm pst": "arctic p12 pwm pst", "p12 pwm pst": "arctic p12 pwm pst", "arctic p12": "arctic p12 pwm pst", "p12 pst": "arctic p12 pwm pst", "arctic p12 fan": "arctic p12 pwm pst"
}


# =====================================================================
# CPU Cooler Database (Carried over)
# =====================================================================
cpu_coolers = {
    "coolmoon aosor s400": {
        "name": "COOLMOON AOSOR S400",
        "type": "Air Cooler",
        "fanSize": "120mm",
        "tdp": "Up to 130W",
        "rgb": "Addressable RGB",
        "price": "₱1,200",
        "sockets": "Intel LGA 1700/1200/115X, AMD AM4"
    },
    "cooler master hyper 212 black edition": {
        "name": "Cooler Master Hyper 212 Black Edition",
        "type": "Air Cooler",
        "fanSize": "120mm",
        "tdp": "Up to 150W",
        "rgb": "No integrated RGB",
        "price": "₱2,500",
        "sockets": "Intel LGA 1700/1200/115X, AMD AM4/AM5"
    },
    "thermalright peerless assassin 120 se": {
        "name": "Thermalright Peerless Assassin 120 SE",
        "type": "Dual-Tower Air Cooler",
        "fanSize": "2x 120mm",
        "tdp": "Up to 245W",
        "rgb": "No RGB",
        "price": "₱3,000",
        "sockets": "Intel LGA 1700/1200/115X, AMD AM4/AM5"
    },
    "deepcool le500 marrs": {
        "name": "Deepcool LE500 MARRS",
        "type": "AIO Liquid Cooler (240mm)",
        "fanSize": "2x 120mm",
        "tdp": "Up to 220W",
        "rgb": "No RGB (has blue LED pump)",
        "price": "₱4,500",
        "sockets": "Intel LGA 1700/1200/115X, AMD AM4/AM5"
    }
}

cpuCoolerModelMap = {
    "coolmoon aosor s400": "coolmoon aosor s400", "aosor s400": "coolmoon aosor s400", "coolmoon s400": "coolmoon aosor s400",
    "hyper 212 black edition": "cooler master hyper 212 black edition", "hyper 212": "cooler master hyper 212 black edition", "cooler master 212": "cooler master hyper 212 black edition",
    "thermalright peerless assassin 120 se": "thermalright peerless assassin 120 se", "pa 120 se": "thermalright peerless assassin 120 se", "thermalright pa 120": "thermalright peerless assassin 120 se",
    "deepcool le500 marrs": "deepcool le500 marrs", "le500 marrs": "deepcool le500 marrs", "deepcool le500": "deepcool le500 marrs", "le500": "deepcool le500 marrs"
}

# =====================================================================
# PSU Database (UPDATED WITH NEW DATA)
# =====================================================================
psus = {
    "corsair rm850x": {
        "name": "Corsair RM850x",
        "wattage": "850W",
        "efficiencyRating": "80 Plus Gold",
        "modularity": "Fully Modular",
        "cables": "ATX 24-pin, EPS 4+4-pin, PCIe 6+2-pin, SATA, Molex",
        "compatibility": "Great for high-performance gaming PCs (RTX 30/40, RX 6000/7000).",
        "price": "₱8,000"
    },
    "cooler master mwe white 750w": {
        "name": "Cooler Master MWE White 750W",
        "wattage": "750W",
        "efficiencyRating": "80 Plus White",
        "modularity": "Non-Modular",
        "cables": "ATX 24-pin, EPS 4+4-pin, PCIe 6+2-pin, SATA, Molex",
        "compatibility": "Best for mid-range PCs. Ensure your GPU’s PCIe connectors match. Non-modular = harder cable management.",
        "price": "₱3,500"
    },
    "corsair cx650": {
        "name": "Corsair CX650",
        "wattage": "650W",
        "efficiencyRating": "80 Plus Bronze",
        "modularity": "Non-Modular",
        "cables": "ATX 24-pin, EPS 4+4-pin, PCIe 6+2-pin, SATA, Molex",
        "compatibility": "Good for Ryzen 5/i5 builds with GPUs like RTX 3050/3060 or RX 6600. Watch for cable clutter (non-modular).",
        "price": "₱4,000"
    },
    "cougar gx-f 750w": {
        "name": "Cougar GX-F 750W",
        "wattage": "750W",
        "efficiencyRating": "80 Plus Gold",
        "modularity": "Fully Modular",
        "cables": "ATX 24-pin, EPS 4+4-pin, PCIe 6+2-pin, SATA, Molex",
        "compatibility": "Great for mid to high-end builds. Fully modular makes cable management easier.",
        "price": "₱5,500"
    },
    "seasonic focus plus gold 550w": {
        "name": "Seasonic Focus Plus Gold 550W",
        "wattage": "550W",
        "efficiencyRating": "80 Plus Gold",
        "modularity": "Fully Modular",
        "cables": "ATX 24-pin, EPS 4+4-pin, PCIe 6+2-pin, SATA, Molex",
        "compatibility": "Ideal for entry-level to mid-range builds with RTX 3050/3060, RX 6600. Fully modular = neat builds.",
        "price": "₱6,000"
    }
}

# PSU Model Variants (mapping user inputs to database keys)
psuModelMap = {
    # Corsair RM850x
    "corsair rm850x": "corsair rm850x",
    "rm850x": "corsair rm850x",
    "corsair 850w psu": "corsair rm850x",
    "850w rm850x": "corsair rm850x",
    "rm850x psu": "corsair rm850x",

    # Cooler Master MWE White 750W
    "cooler master mwe white 750w": "cooler master mwe white 750w",
    "mwe white 750w": "cooler master mwe white 750w",
    "cooler master 750w psu": "cooler master mwe white 750w",
    "750w mwe white": "cooler master mwe white 750w",
    "mwe white psu": "cooler master mwe white 750w",

    # Corsair CX650
    "corsair cx650": "corsair cx650",
    "cx650": "corsair cx650",
    "corsair 650w psu": "corsair cx650",
    "650w cx650": "corsair cx650",
    "cx650 psu": "corsair cx650",

    # Cougar GX-F 750W
    "cougar gx-f 750w": "cougar gx-f 750w",
    "gx-f 750w": "cougar gx-f 750w",
    "cougar 750w psu": "cougar gx-f 750w",
    "750w gx-f": "cougar gx-f 750w",
    "gx-f psu": "cougar gx-f 750w",

    # Seasonic Focus Plus Gold 550W
    "seasonic focus plus gold 550w": "seasonic focus plus gold 550w",
    "focus plus gold 550w": "seasonic focus plus gold 550w",
    "seasonic 550w psu": "seasonic focus plus gold 550w",
    "550w focus plus": "seasonic focus plus gold 550w",
    "focus plus psu": "seasonic focus plus gold 550w"
}

# =====================================================================
# RAM Database (NEW)
# =====================================================================
rams = {
    "kingston fury beast ddr4": {
        "name": "Kingston FURY Beast DDR4",
        "capacity": "8GB, 16GB, or 32GB",
        "type": "DDR4",
        "speed": "3200 MHz",
        "voltage": "1.35 V",
        "compatibility": "Requires motherboard with DDR4 DIMM slots (288-pin) supporting 1.35V and 3200 MHz. Check motherboard QVL (Qualified Vendor List) for guaranteed compatibility.",
        "price": "₱2,000"
    },
    "kingston hyperx fury ddr3": {
        "name": "Kingston HyperX FURY DDR3",
        "capacity": "8GB",
        "type": "DDR3",
        "speed": "1600 MHz",
        "voltage": "1.5 V",
        "compatibility": "For older systems only. Requires a DDR3 (240-pin) motherboard. Incompatible with modern DDR4/DDR5 systems.",
        "price": "₱1,200"
    },
    "hkc pc ddr4-3200 dimm": {
        "name": "HKC PC DDR4-3200 DIMM",
        "capacity": "8GB",
        "type": "DDR4",
        "speed": "3200 MHz",
        "voltage": "1.2 V",
        "compatibility": "Works with DDR4 (288-pin) motherboards supporting 1.2V and 3200 MHz. Recommend using matched pairs and checking motherboard QVL.",
        "price": "₱1,800"
    },
    "hkcmemory hu40 ddr4 (16gb)": {
        "name": "HKCMEMORY HU40 DDR4 (16GB)",
        "capacity": "16GB",
        "type": "DDR4",
        "speed": "3200 MHz",
        "voltage": "1.2 V",
        "compatibility": "Compatible with DDR4 (288-pin) motherboards supporting 1.2V and 3200 MHz. Check QVL for higher capacity module compatibility.",
        "price": "₱3,500"
    },
    "hkcmemory hu40 ddr4 (8gb)": {
        "name": "HKCMEMORY HU40 DDR4 (8GB)",
        "capacity": "8GB",
        "type": "DDR4",
        "speed": "3200 MHz",
        "voltage": "1.2 V",
        "compatibility": "Compatible with DDR4 (288-pin) motherboards supporting 1.2V and 3200 MHz.",
        "price": "₱1,700"
    }
}

# RAM Model Variants (mapping user inputs to database keys)
ramModelMap = {
    "kingston fury beast ddr4": "kingston fury beast ddr4",
    "fury beast ddr4": "kingston fury beast ddr4",
    "kingston beast ddr4": "kingston fury beast ddr4",
    "kingston fury beast": "kingston fury beast ddr4",
    "fury beast": "kingston fury beast ddr4",

    "kingston hyperx fury ddr3": "kingston hyperx fury ddr3",
    "hyperx fury ddr3": "kingston hyperx fury ddr3",
    "kingston fury ddr3": "kingston hyperx fury ddr3",
    "hyperx fury": "kingston hyperx fury ddr3",

    "hkc pc ddr4-3200 dimm": "hkc pc ddr4-3200 dimm",
    "hkc ddr4-3200": "hkc pc ddr4-3200 dimm",
    "hkc pc ddr4": "hkc pc ddr4-3200 dimm",
    "hkc 3200 dimm": "hkc pc ddr4-3200 dimm",

    "hkcmemory hu40 ddr4 (16gb)": "hkcmemory hu40 ddr4 (16gb)",
    "hu40 ddr4 16gb": "hkcmemory hu40 ddr4 (16gb)",
    "hkc hu40 ddr4": "hkcmemory hu40 ddr4 (16gb)",
    "hu40 16gb": "hkcmemory hu40 ddr4 (16gb)",
    "hkcmemory hu40": "hkcmemory hu40 ddr4 (16gb)",
    "hu40": "hkcmemory hu40 ddr4 (16gb)",

    "hkcmemory hu40 ddr4 (8gb)": "hkcmemory hu40 ddr4 (8gb)",
    "hu40 ddr4 8gb": "hkcmemory hu40 ddr4 (8gb)",
    "hu40 8gb": "hkcmemory hu40 ddr4 (8gb)"
}


# =====================================================================
# STORAGE Database (NEW)
# =====================================================================
storages = {
    "seagate barracuda 1tb": {
        "name": "Seagate Barracuda 1TB",
        "type": "HDD",
        "capacity": "1TB",
        "interface": "SATA 6Gb/s",
        "formFactor": "3.5-inch",
        "rpm": "7200 RPM",
        "compatibility": "Requires a motherboard with an available SATA port and a SATA power connector from the PSU. Ensure your case has a 3.5-inch drive bay. It's a good choice for bulk storage.",
        "price": "₱2,500"
    },
    "western digital blue 2tb": {
        "name": "Western Digital Blue 2TB",
        "type": "HDD",
        "capacity": "2TB",
        "interface": "SATA 6Gb/s",
        "formFactor": "3.5-inch",
        "rpm": "5400/7200 RPM (typically 5400 for Blue)",
        "compatibility": "Requires a motherboard with an available SATA port and a SATA power connector from the PSU. Ensure your case has a 3.5-inch drive bay. Excellent for larger storage needs.",
        "price": "₱3,800"
    },
    "samsung 970 evo plus 1tb": {
        "name": "Samsung 970 EVO Plus 1TB",
        "type": "NVMe SSD",
        "capacity": "1TB",
        "interface": "PCIe Gen 3.0 x4",
        "formFactor": "M.2 2280",
        "readSpeed": "~3500MB/s",
        "writeSpeed": "~3300MB/s",
        "compatibility": "Requires a motherboard with an available M.2 slot supporting PCIe Gen 3.0 x4 NVMe SSDs. Check if your motherboard shares M.2 bandwidth with SATA ports.",
        "price": "₱5,500"
    },
    "crucial mx500 500gb": {
        "name": "Crucial MX500 500GB",
        "type": "SATA SSD",
        "capacity": "500GB",
        "interface": "SATA 6Gb/s",
        "formFactor": "2.5-inch",
        "readSpeed": "~560MB/s",
        "writeSpeed": "~510MB/s",
        "compatibility": "Requires a motherboard with an available SATA port and a SATA power connector from the PSU. Ensure your case has a 2.5-inch drive bay. It's a reliable and cost-effective option for a fast boot drive or general storage.",
        "price": "₱3,000"
    }
}

# Storage Model Variants (mapping user inputs to database keys)
storageModelMap = {
    "seagate barracuda 1tb": "seagate barracuda 1tb",
    "barracuda 1tb": "seagate barracuda 1tb",
    "seagate 1tb hdd": "seagate barracuda 1tb",
    "1tb barracuda": "seagate barracuda 1tb",

    "western digital blue 2tb": "western digital blue 2tb",
    "wd blue 2tb": "western digital blue 2tb",
    "2tb blue hdd": "western digital blue 2tb",

    "samsung 970 evo plus 1tb": "samsung 970 evo plus 1tb",
    "970 evo plus 1tb": "samsung 970 evo plus 1tb",
    "samsung nvme 1tb": "samsung 970 evo plus 1tb",
    "970 evo plus": "samsung 970 evo plus 1tb",

    "crucial mx500 500gb": "crucial mx500 500gb",
    "mx500 500gb": "crucial mx500 500gb",
    "crucial 500gb ssd": "crucial mx500 500gb",
    "mx500 ssd": "crucial mx500 500gb"
}

# ==================
# STORAGE ACTIONS 
# ==================
class ActionStorageDetails(Action):
    def name(self) -> Text:
        return "action_storage_details"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        storage_entity = next(tracker.get_latest_entity_values("storage_model"), None)
        intent_name = tracker.latest_message['intent']['name']

        if not storage_entity:
            if intent_name == "request_storage_price":
                dispatcher.utter_message(template="utter_ask_storage_price")
            else:
                dispatcher.utter_message(template="utter_ask_storage_details")
            return []

        storage_key = storageModelMap.get(storage_entity.lower().strip())

        if storage_key and storage_key in storages:
            data = storages[storage_key]
            
            if intent_name == "request_storage_price":
                price = data.get('price')
                if price:
                    dispatcher.utter_message(text=f"The price for the **{data['name']}** is typically **{price}**.")
                else:
                    dispatcher.utter_message(text=f"Sorry, I don’t have the price for **{data['name']}**.")
            
            else:
                # Dynamic response based on HDD or SSD
                if data['type'] in ["NVMe SSD", "SATA SSD"]:
                    # SSD format
                    message = (f"The **{data['name']}** key specifications are:\n\n"
                               f"* **Type:** {data['type']}\n"
                               f"* **Capacity:** {data['capacity']}\n"
                               f"* **Interface:** {data['interface']}\n"
                               f"* **Form Factor:** {data['formFactor']}\n"
                               f"* **Read/Write Speed:** ~{data['readSpeed']}/~{data['writeSpeed']}\n"
                               f"* **Compatibility:** {data['compatibility']}\n"
                               f"* **Price:** {data['price']}")
                else:
                    # HDD format
                    message = (f"The **{data['name']}** key specifications are:\n\n"
                               f"* **Type:** {data['type']}\n"
                               f"* **Capacity:** {data['capacity']}\n"
                               f"* **Interface:** {data['interface']}\n"
                               f"* **Form Factor:** {data['formFactor']}\n"
                               f"* **RPM:** {data['rpm']}\n"
                               f"* **Compatibility:** {data['compatibility']}\n"
                               f"* **Price:** {data['price']}")
                
                dispatcher.utter_message(text=message)
        else:
            dispatcher.utter_message(template="utter_storage_not_found")
            
        return []

class ActionCompareStorages(Action):
    def name(self) -> Text:
        return "action_compare_storages"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
            
        entities = list(tracker.get_latest_entity_values("storage_model"))
        
        if len(entities) >= 2:
            k1 = storageModelMap.get(entities[0].lower().strip())
            k2 = storageModelMap.get(entities[1].lower().strip())
            
            if k1 and k2 and k1 in storages and k2 in storages:
                d1, d2 = storages[k1], storages[k2]
                
                # Dynamic feature extraction based on type (for a cleaner table)
                def get_main_spec(data):
                    if data['type'] in ["NVMe SSD", "SATA SSD"]:
                        return f"R:{data.get('readSpeed', 'N/A')}/W:{data.get('writeSpeed', 'N/A')}"
                    else:
                        return data.get('rpm', 'N/A')

                spec1 = get_main_spec(d1)
                spec2 = get_main_spec(d2)

                main_spec_header = "RPM / Speed" # Unified header

                msg = (f"**Storage Comparison:**\n\n"
                       f"| Feature | {d1['name']} | {d2['name']} |\n"
                       f"|---|---|---|\n"
                       f"| **Type** | {d1['type']} | {d2['type']} |\n"
                       f"| **Capacity** | {d1['capacity']} | {d2['capacity']} |\n"
                       f"| **Interface** | {d1['interface']} | {d2['interface']} |\n"
                       f"| **Form Factor** | {d1['formFactor']} | {d2['formFactor']} |\n"
                       f"| **{main_spec_header}** | {spec1} | {spec2} |\n"
                       f"| **Price** | {d1['price']} | {d2['price']} |")

                dispatcher.utter_message(text=msg)
            else:
                dispatcher.utter_message(template="utter_storage_not_found")
        else:
            dispatcher.utter_message(template="utter_too_many_storages")
            
        return []

# ==================
# RAM ACTIONS 
# ==================

class ActionRamDetails(Action):
    def name(self) -> Text:
        return "action_ram_details"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        ram_entity = next(tracker.get_latest_entity_values("ram_model"), None)
        intent_name = tracker.latest_message['intent']['name']

        if not ram_entity:
            if intent_name == "request_ram_price":
                dispatcher.utter_message(template="utter_ask_ram_price")
            else:
                dispatcher.utter_message(template="utter_ask_ram_details")
            return []

        ram_key = ramModelMap.get(ram_entity.lower().strip())

        if ram_key and ram_key in rams:
            data = rams[ram_key]
            
            if intent_name == "request_ram_price":
                price = data.get('price')
                if price:
                    dispatcher.utter_message(text=f"The price for the **{data['name']}** is typically **{price}**.")
                else:
                    dispatcher.utter_message(text=f"Sorry, I don’t have the price for **{data['name']}**.")
            
            else:
                message = (f"The **{data['name']}** key specifications are:\n\n"
                           f"* **Type:** {data['type']}\n"
                           f"* **Capacity:** {data['capacity']}\n"
                           f"* **Speed:** {data['speed']}\n"
                           f"* **Voltage:** {data['voltage']}\n"
                           f"* **Compatibility:** {data['compatibility']}\n"
                           f"* **Price:** {data['price']}")
                
                dispatcher.utter_message(text=message)
        else:
            dispatcher.utter_message(template="utter_ram_not_found")
            
        return []

class ActionCompareRams(Action):
    def name(self) -> Text:
        return "action_compare_rams"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
            
        entities = list(tracker.get_latest_entity_values("ram_model"))
        
        if len(entities) >= 2:
            k1 = ramModelMap.get(entities[0].lower().strip())
            k2 = ramModelMap.get(entities[1].lower().strip())
            
            if k1 and k2 and k1 in rams and k2 in rams:
                d1, d2 = rams[k1], rams[k2]
                
                msg = (f"**RAM Comparison:**\n\n"
                       f"| Feature | {d1['name']} | {d2['name']} |\n"
                       f"|---|---|---|\n"
                       f"| **Type** | {d1['type']} | {d2['type']} |\n"
                       f"| **Capacity** | {d1['capacity']} | {d2['capacity']} |\n"
                       f"| **Speed** | {d1['speed']} | {d2['speed']} |\n"
                       f"| **Voltage** | {d1['voltage']} | {d2['voltage']} |\n"
                       f"| **Price** | {d1['price']} | {d2['price']} |\n"
                       f"| **Compatibility Note** | {d1['compatibility']} | {d2['compatibility']} |")

                dispatcher.utter_message(text=msg)
            else:
                dispatcher.utter_message(template="utter_ram_not_found")
        else:
            dispatcher.utter_message(template="utter_too_many_rams")
            
        return []


# =====================================================================
# PSU ACTIONS
# =====================================================================

class ActionPsuDetails(Action):
    def name(self) -> Text:
        return "action_psu_details"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        # 1. Get the entity and determine the request type
        psu_entity = next(tracker.get_latest_entity_values("psu_model"), None)
        intent_name = tracker.latest_message['intent']['name']

        if not psu_entity:
            # No PSU specified, ask for it
            if intent_name == "request_psu_price":
                dispatcher.utter_message(template="utter_ask_psu_price")
            else:
                dispatcher.utter_message(template="utter_ask_psu_details")
            return []

        # 2. Map the entity to the canonical key in the database
        psu_key = psuModelMap.get(psu_entity.lower().strip())

        if psu_key and psu_key in psus:
            data = psus[psu_key]
            
            # Case 1: User requested Price only
            if intent_name == "request_psu_price":
                price = data.get('price')
                if price:
                    dispatcher.utter_message(text=f"The price for the **{data['name']}** is typically **{price}**.")
                else:
                    dispatcher.utter_message(text=f"Sorry, I don’t have the price for **{data['name']}**.")
            
            # Case 2: User requested general Specs
            else:
                # Format the detailed response message
                message = (f"The **{data['name']}** is an excellent choice! Here are the key specifications:\n\n"
                           f"* **Wattage:** {data['wattage']}\n"
                           f"* **Efficiency:** {data['efficiencyRating']}\n"
                           f"* **Modularity:** {data['modularity']}\n"
                           f"* **Cables:** {data['cables']}\n"
                           f"* **Compatibility:** {data['compatibility']}\n"
                           f"* **Price:** {data['price']}")
                
                dispatcher.utter_message(text=message)
        else:
            # PSU not found in the database
            dispatcher.utter_message(template="utter_psu_not_found")
            
        return []

class ActionComparePsus(Action):
    def name(self) -> Text:
        return "action_compare_psus"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
            
        # Get all extracted 'psu_model' entities
        entities = list(tracker.get_latest_entity_values("psu_model"))
        
        # Check if exactly two entities were extracted
        if len(entities) >= 2:
            # Map the first two extracted entities to canonical keys
            k1 = psuModelMap.get(entities[0].lower().strip())
            k2 = psuModelMap.get(entities[1].lower().strip())
            
            if k1 and k2 and k1 in psus and k2 in psus:
                d1, d2 = psus[k1], psus[k2]
                
                # Format the comparison into a Markdown table
                msg = (f"**PSU Comparison:**\n\n"
                       f"| Feature | {d1['name']} | {d2['name']} |\n"
                       f"|---|---|---|\n"
                       f"| **Wattage** | {d1['wattage']} | {d2['wattage']} |\n"
                       f"| **Efficiency** | {d1['efficiencyRating']} | {d2['efficiencyRating']} |\n"
                       f"| **Modularity** | {d1['modularity']} | {d2['modularity']} |\n"
                       f"| **Price** | {d1['price']} | {d2['price']} |\n"
                       f"| **Best Use** | {d1['compatibility']} | {d2['compatibility']} |")

                dispatcher.utter_message(text=msg)
            else:
                # One or both PSUs were not found
                dispatcher.utter_message(template="utter_psu_not_found")
        else:
            # Not enough PSUs for comparison
            dispatcher.utter_message(template="utter_too_many_psus")
            
        return []


# =====================================================================
# Motherboard Actions (Carried over)
# =====================================================================

class ActionBoardDetails(Action):
    def name(self) -> Text:
        return "action_board_details"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        board = next(tracker.get_latest_entity_values("motherboard"), None)
        key = motherboardModelMap.get(board.lower().strip()) if board else None
        
        if key and key in motherboards:
            details = motherboards[key]
            dispatcher.utter_message(
                text=f"Here are the details for **{details['name']}**:\n"
                     f"- Socket: {details['socket']}\n"
                     f"- Chipset: {details['chipset']}\n"
                     f"- Form Factor: {details['formFactor']}\n"
                     f"- Memory: {details['ram']}\n"
                     f"- Features: {details['features']}\n"
                     f"- Compatibility: {details['compatibility']}\n"
                     f"- Price: {details['price']}"
            )
        elif board:
            dispatcher.utter_message(text=f"Sorry, I don’t have details for **{board}**. Please check the model name.")
        else:
            dispatcher.utter_message(text="Please specify which motherboard you want details for.")
        return []

class ActionFindMotherboard(Action):
    def name(self) -> Text:
        return "action_find_motherboard"

    def run(self, dispatcher, tracker, domain):
        dispatcher.utter_message(text="I can provide details for specific boards like ASUS PRIME B550M-K, MSI PRO H610M-S DDR4, or MSI B650M Gaming Plus WiFi. What would you like to know?")
        return []

class ActionCompareBoards(Action):
    def name(self) -> Text:
        return "action_compare_boards"

    def run(self, dispatcher, tracker, domain):
        entities = list(tracker.get_latest_entity_values("motherboard"))
        
        if len(entities) >= 2:
            k1 = motherboardModelMap.get(entities[0].lower().strip())
            k2 = motherboardModelMap.get(entities[1].lower().strip())
            
            if k1 and k2 and k1 in motherboards and k2 in motherboards:
                d1, d2 = motherboards[k1], motherboards[k2]
                msg = (f"**Motherboard Comparison:**\n\n"
                       f"| Feature | {d1['name']} | {d2['name']} |\n"
                       f"|---|---|---|\n"
                       f"| Socket | {d1['socket']} | {d2['socket']} |\n"
                       f"| Chipset | {d1['chipset']} | {d2['chipset']} |\n"
                       f"| Form Factor | {d1['formFactor']} | {d2['formFactor']} |\n"
                       f"| RAM | {d1['ram']} | {d2['ram']} |\n"
                       f"| Price | {d1['price']} | {d2['price']} |") 
                dispatcher.utter_message(text=msg)
            else:
                dispatcher.utter_message(text="One or both of the motherboards are not in my database or the model name is unclear.")
        else:
            dispatcher.utter_message(text="Please mention two motherboards to compare.")
        return []

class ActionPriceCheck(Action):
    def name(self) -> Text:
        return "action_price_check"

    def run(self, dispatcher, tracker, domain):
        board = next(tracker.get_latest_entity_values("motherboard"), None)
        key = motherboardModelMap.get(board.lower().strip()) if board else None
        
        if key and key in motherboards:
            price = motherboards[key]["price"]
            dispatcher.utter_message(text=f"The price of **{motherboards[key]['name']}** is **{price}**.")
        elif board:
            dispatcher.utter_message(text=f"Sorry, I don’t have the price for **{board}**.")
        else:
            dispatcher.utter_message(text="Please tell me which motherboard you want the price for.")
        return []


# =====================================================================
# Case Fan Actions (Carried over)
# =====================================================================

class ActionFanDetails(Action):
    def name(self) -> Text:
        return "action_fan_details"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        fan_entity = next(tracker.get_latest_entity_values("fan_model"), None)
        
        if fan_entity:
            key = caseFanModelMap.get(fan_entity.lower().strip())
            
            if key and key in case_fans:
                details = case_fans[key]
                dispatcher.utter_message(
                    text=f"Here are the details for the **{details['name']}** case fan:\n"
                         f"- Size: {details['size']}\n"
                         f"- RPM Range: {details['rpm']}\n"
                         f"- Airflow: {details['airflow']}\n"
                         f"- Noise Level: {details['noise']}\n"
                         f"- RGB: {details['rgb']}\n"
                         f"- Price: {details['price']}"
                )
            else:
                dispatcher.utter_message(text=f"Sorry, I don’t have details for the fan model **{fan_entity}**.")
        else:
            dispatcher.utter_message(template="utter_ask_fan_details")
        
        return []

class ActionFanPriceCheck(Action):
    def name(self) -> Text:
        return "action_fan_price_check"

    def run(self, dispatcher, tracker, domain):
        fan_entity = next(tracker.get_latest_entity_values("fan_model"), None)
        
        if fan_entity:
            key = caseFanModelMap.get(fan_entity.lower().strip())
            
            if key and key in case_fans:
                price = case_fans[key]["price"]
                dispatcher.utter_message(text=f"The price of the **{case_fans[key]['name']}** is **{price}**.")
            else:
                dispatcher.utter_message(text=f"Sorry, I don’t have the price for **{fan_entity}**.")
        else:
            dispatcher.utter_message(template="utter_ask_fan_price")
            
        return []

class ActionCompareFans(Action):
    def name(self) -> Text:
        return "action_compare_fans"

    def run(self, dispatcher, tracker, domain):
        entities = list(tracker.get_latest_entity_values("fan_model"))
        
        if len(entities) >= 2:
            k1 = caseFanModelMap.get(entities[0].lower().strip())
            k2 = caseFanModelMap.get(entities[1].lower().strip())
            
            if k1 and k2 and k1 in case_fans and k2 in case_fans:
                d1, d2 = case_fans[k1], case_fans[k2]
                msg = (f"**Case Fan Comparison:**\n\n"
                       f"| Feature | {d1['name']} | {d2['name']} |\n"
                       f"|---|---|---|\n"
                       f"| Size | {d1['size']} | {d2['size']} |\n"
                       f"| RPM | {d1['rpm']} | {d2['rpm']} |\n"
                       f"| Airflow | {d1['airflow']} | {d2['airflow']} |\n"
                       f"| Noise | {d1['noise']} | {d2['noise']} |\n"
                       f"| RGB | {d1['rgb']} | {d2['rgb']} |\n"
                       f"| Price | {d1['price']} | {d2['price']} |")
                dispatcher.utter_message(text=msg)
            else:
                dispatcher.utter_message(text="One or both of the specified case fans are not in my database.")
        else:
            dispatcher.utter_message(text="Please mention two case fans to compare.")

        return []

# =====================================================================
# CPU Cooler Actions (Carried over)
# =====================================================================

class ActionCoolerDetails(Action):
    def name(self) -> Text:
        return "action_cooler_details"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        cooler_entity = next(tracker.get_latest_entity_values("cooler_model"), None)
        
        if cooler_entity:
            key = cpuCoolerModelMap.get(cooler_entity.lower().strip())
            
            if key and key in cpu_coolers:
                details = cpu_coolers[key]
                dispatcher.utter_message(
                    text=f"Here are the details for the **{details['name']}** CPU Cooler:\n"
                         f"- Type: {details['type']}\n"
                         f"- Fan Size: {details['fanSize']}\n"
                         f"- Max TDP: {details['tdp']}\n"
                         f"- RGB: {details['rgb']}\n"
                         f"- Compatible Sockets: {details['sockets']}\n"
                         f"- Price: {details['price']}"
                )
            else:
                dispatcher.utter_message(text=f"Sorry, I don’t have details for the cooler model **{cooler_entity}**.")
        else:
            dispatcher.utter_message(template="utter_ask_cooler_details")
        
        return []

class ActionCoolerPriceCheck(Action):
    def name(self) -> Text:
        return "action_cooler_price_check"

    def run(self, dispatcher, tracker, domain):
        cooler_entity = next(tracker.get_latest_entity_values("cooler_model"), None)
        
        if cooler_entity:
            key = cpuCoolerModelMap.get(cooler_entity.lower().strip())
            
            if key and key in cpu_coolers:
                price = cpu_coolers[key]["price"]
                dispatcher.utter_message(text=f"The price of the **{cpu_coolers[key]['name']}** is **{price}**.")
            else:
                dispatcher.utter_message(text=f"Sorry, I don’t have the price for **{cooler_entity}**.")
        else:
            dispatcher.utter_message(template="utter_ask_cooler_price")
            
        return []

class ActionCompareCoolers(Action):
    def name(self) -> Text:
        return "action_compare_coolers"

    def run(self, dispatcher, tracker, domain):
        entities = list(tracker.get_latest_entity_values("cooler_model"))
        
        if len(entities) >= 2:
            k1 = cpuCoolerModelMap.get(entities[0].lower().strip())
            k2 = cpuCoolerModelMap.get(entities[1].lower().strip())
            
            if k1 and k2 and k1 in cpu_coolers and k2 in cpu_coolers:
                d1, d2 = cpu_coolers[k1], cpu_coolers[k2]
                msg = (f"**CPU Cooler Comparison:**\n\n"
                       f"| Feature | {d1['name']} | {d2['name']} |\n"
                       f"|---|---|---|\n"
                       f"| Type | {d1['type']} | {d2['type']} |\n"
                       f"| Max TDP | {d1['tdp']} | {d2['tdp']} |\n"
                       f"| RGB | {d1['rgb']} | {d2['rgb']} |\n"
                       f"| Price | {d1['price']} | {d2['price']} |\n"
                       f"| Sockets | {d1['sockets']} | {d2['sockets']} |")
                dispatcher.utter_message(text=msg)
            else:
                dispatcher.utter_message(text="One or both of the specified CPU coolers are not in my database.")
        else:
            dispatcher.utter_message(text="Please mention two CPU coolers to compare.")

        return []

# =====================================================================
# CPU Actions (Carried over)
# =====================================================================

class ActionCpuDetails(Action):
    def name(self) -> Text:
        return "action_cpu_details"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        cpu_entity = next(tracker.get_latest_entity_values("cpu_model"), None)
        
        key = cpuModelMap.get(cpu_entity.lower().strip()) if cpu_entity else None
        
        if key and key in cpus:
            details = cpus[key]
            dispatcher.utter_message(
                text=f"Here are the details for the **{details['name']}** CPU:\n"
                     f"- Price: {details['price']}\n"
                     f"- Socket: {details['socket']}\n"
                     f"- Cores/Threads: {details['coresThreads']}\n"
                     f"- Base Clock: {details['baseClock']}\n"
                     f"- TDP (Max): {details['tdp']}\n"
                     f"- Compatibility: {details['compatibility']}"
            )
        elif cpu_entity:
            dispatcher.utter_message(text=f"Sorry, I don’t have details for the CPU **{cpu_entity}**.")
        else:
            dispatcher.utter_message(template="utter_ask_cpu_details")
        
        return []

class ActionCpuPriceCheck(Action):
    def name(self) -> Text:
        return "action_cpu_price_check"

    def run(self, dispatcher, tracker, domain):
        cpu_entity = next(tracker.get_latest_entity_values("cpu_model"), None)
        
        key = cpuModelMap.get(cpu_entity.lower().strip()) if cpu_entity else None
        
        if key and key in cpus:
            price = cpus[key]["price"]
            dispatcher.utter_message(text=f"The price of the **{cpus[key]['name']}** is **{price}**.")
        elif cpu_entity:
            dispatcher.utter_message(text=f"Sorry, I don’t have the price for **{cpu_entity}**.")
        else:
            dispatcher.utter_message(template="utter_ask_cpu_price")
            
        return []

class ActionCompareCpus(Action):
    def name(self) -> Text:
        return "action_compare_cpus"

    def run(self, dispatcher, tracker, domain):
        entities = list(tracker.get_latest_entity_values("cpu_model"))
        
        if len(entities) >= 2:
            k1 = cpuModelMap.get(entities[0].lower().strip())
            k2 = cpuModelMap.get(entities[1].lower().strip())
            
            if k1 and k2 and k1 in cpus and k2 in cpus:
                d1, d2 = cpus[k1], cpus[k2]
                msg = (f"**CPU Comparison:**\n\n"
                       f"| Feature | {d1['name']} | {d2['name']} |\n"
                       f"|---|---|---|\n"
                       f"| Price | {d1['price']} | {d2['price']} |\n"
                       f"| Socket | {d1['socket']} | {d2['socket']} |\n"
                       f"| Cores/Threads | {d1['coresThreads']} | {d2['coresThreads']} |\n"
                       f"| Base Clock | {d1['baseClock']} | {d2['baseClock']} |\n"
                       f"| TDP | {d1['tdp']} | {d2['tdp']} |")
                dispatcher.utter_message(text=msg)
            else:
                dispatcher.utter_message(text="One or both of the specified CPUs are not in my database.")
        else:
            dispatcher.utter_message(text="Please mention two CPUs to compare.")

        return []


# =====================================================================
# GPU Actions (NEW)
# =====================================================================

class ActionGpuDetails(Action):
    def name(self) -> Text:
        return "action_gpu_details"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        gpu_entity = next(tracker.get_latest_entity_values("gpu_model"), None)
        
        key = gpuModelMap.get(gpu_entity.lower().strip()) if gpu_entity else None
        
        if key and key in gpus:
            details = gpus[key]
            dispatcher.utter_message(
                text=f"Here are the details for the **{details['name']}** GPU:\n"
                     f"- VRAM: {details['vram']}\n"
                     f"- Clock Speed: {details['clockSpeed']}\n"
                     f"- Power Consumption: {details['powerConsumption']}\n"
                     f"- Slot Type: {details['slotType']}\n"
                     f"- Compatibility: {details['compatibility']}"
            )
        elif gpu_entity:
            dispatcher.utter_message(text=f"Sorry, I don’t have details for the GPU **{gpu_entity}**.")
        else:
            dispatcher.utter_message(template="utter_ask_gpu_details")
        
        return []

class ActionGpuPriceCheck(Action):
    def name(self) -> Text:
        return "action_gpu_price_check"

    # NOTE: Since no price is provided in the GPU data, I will use a default response for now.
    def run(self, dispatcher, tracker, domain):
        gpu_entity = next(tracker.get_latest_entity_values("gpu_model"), None)
        
        key = gpuModelMap.get(gpu_entity.lower().strip()) if gpu_entity else None
        
        if key and key in gpus:
            # Check for a 'price' key, otherwise state that price is unavailable
            price = gpus[key].get("price", "unavailable")
            if price != "unavailable":
                 dispatcher.utter_message(text=f"The price of the **{gpus[key]['name']}** is **{price}**.")
            else:
                 dispatcher.utter_message(text=f"I don't have the current price for the **{gpus[key]['name']}** in my database.")
        elif gpu_entity:
            dispatcher.utter_message(text=f"Sorry, I don’t have the price for **{gpu_entity}**.")
        else:
            dispatcher.utter_message(template="utter_ask_gpu_price")
            
        return []

class ActionCompareGpus(Action):
    def name(self) -> Text:
        return "action_compare_gpus"

    def run(self, dispatcher, tracker, domain):
        entities = list(tracker.get_latest_entity_values("gpu_model"))
        
        if len(entities) >= 2:
            k1 = gpuModelMap.get(entities[0].lower().strip())
            k2 = gpuModelMap.get(entities[1].lower().strip())
            
            if k1 and k2 and k1 in gpus and k2 in gpus:
                d1, d2 = gpus[k1], gpus[k2]
                # Price is omitted from the comparison table since it's missing in the data
                msg = (f"**GPU Comparison:**\n\n"
                       f"| Feature | {d1['name']} | {d2['name']} |\n"
                       f"|---|---|---|\n"
                       f"| VRAM | {d1['vram']} | {d2['vram']} |\n"
                       f"| Clock Speed | {d1['clockSpeed']} | {d2['clockSpeed']} |\n"
                       f"| Power (Watts) | {d1['powerConsumption']} | {d2['powerConsumption']} |\n"
                       f"| Slot Type | {d1['slotType']} | {d2['slotType']} |")
                dispatcher.utter_message(text=msg)
            else:
                dispatcher.utter_message(text="One or both of the specified GPUs are not in my database.")
        else:
            dispatcher.utter_message(text="Please mention two GPUs to compare.")

        return []