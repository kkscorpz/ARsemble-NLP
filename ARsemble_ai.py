import json
import re
import torch
from sentence_transformers import SentenceTransformer, util
import os
import sys

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# ai_chatbot.py - COMPLETE AI CHATBOT WITH COMPATIBILITY


class PCChatbot:
    def __init__(self):
        print("Initializing PC Expert AI...")
        try:
            self.model = SentenceTransformer('all-MiniLM-L6-v2')
            self.components_db = self.load_all_components()
            self.component_names = list(self.components_db.keys())
            self.embeddings = self.model.encode(
                self.component_names, convert_to_tensor=True
            )

            # Load training data
            self.training_file = "training_data/user_queries.json"
            self.load_training_data()

            print(
                f"ARsemble AI Ready! Loaded {len(self.components_db)} components!")

        except Exception as e:
            print(f"Error initializing ARsemble AI: {e}")
            # Set defaults to prevent crashes
            self.model = None
            self.components_db = {}
            self.component_names = []
            self.embeddings = None
            self.training_data = []

    def load_training_data(self):
        """Load or create training data file"""
        self.training_data = []
        if os.path.exists(self.training_file):
            with open(self.training_file, 'r', encoding='utf-8') as f:
                self.training_data = json.load(f)
            print(f"Loaded {len(self.training_data)} training examples")
        else:
            os.makedirs(os.path.dirname(self.training_file), exist_ok=True)
            print("Starting with fresh training data")

    def save_training_example(self, user_query, ai_response):
        """Save user query and AI response to training data"""
        training_example = {
            "user_query": user_query,
            "ai_response": ai_response
        }

        # Check if similar query already exists
        for example in self.training_data:
            if user_query.lower() == example['user_query'].lower():
                return  # Skip if already exists

        self.training_data.append(training_example)

        # Save to file
        with open(self.training_file, 'w', encoding='utf-8') as f:
            json.dump(self.training_data, f, indent=2, ensure_ascii=False)

    def load_all_components(self):
        """Load COMPLETE PC components database - ALL YOUR COMPONENTS"""
        components = {
            # ==========================
            # ========== GPUs ==========
            # ==========================
            "rtx 3050": {
                "name": "Gigabyte RTX 3050 EAGLE OC", "type": "GPU",
                "vram": "8GB GDDR6", "clock": "~1777 MHz (Boost)", "power": "~130 Watts",
                "slot": "PCIe 4.0 x16",
                "compatibility": "Requires a motherboard with an available PCIe x16 slot (compatible with PCIe 3.0/4.0/5.0). Needs a PSU with sufficient wattage (450W-550W recommended total system power) and at least one 8-pin PCIe power connector. Ensure your case has enough physical clearance."
            },
            "rtx 4060": {
                "name": "MSI RTX 4060 GAMING X", "type": "GPU",
                "vram": "8GB GDDR6", "clock": "~2595 MHz (Boost)", "power": "~115 Watts",
                "slot": "PCIe 4.0 x8",
                "compatibility": "Requires a motherboard with an available PCIe x16 slot. Needs a 550W+ PSU with one 8-pin PCIe power connector. Compatible with modern cases."
            },
            "rx 9060 xt 8gb": {
                "name": "Gigabyte RX 9060 XT Gaming OC", "type": "GPU",
                "vram": "8GB GDDR6", "clock": "~2200 MHz (Boost)", "power": "~180 Watts",
                "slot": "PCIe 4.0 x16",
                "compatibility": "Requires PCIe x16 slot. Recommended 600W PSU with 2x 8-pin PCIe connectors. Ensure your case supports full-length GPUs."
            },
            "gtx 750 ti": {
                "name": "NVIDIA GTX 750 Ti", "type": "GPU",
                "vram": "4GB GDDR5", "clock": "~1085 MHz (Boost)", "power": "~60 Watts",
                "slot": "PCIe 3.0 x16",
                "compatibility": "Very low power draw (300W PSU recommended). Single 6-pin PCIe power connector or none depending on model. Fits in most cases due to compact size."
            },
            "rtx 3060": {
                "name": "MSI RTX 3060", "type": "GPU",
                "vram": "12GB GDDR6", "clock": "~1777 MHz (Boost)", "power": "~170 Watts",
                "slot": "PCIe 4.0 x16",
                "compatibility": "Needs PCIe x16 slot and 550W+ PSU. Requires 1x 8-pin PCIe power connector. Ensure case has enough clearance."
            },
            "rx 9060 xt 16gb": {  # failed
                "name": "Sapphire RX 9060 XT", "type": "GPU",
                "vram": "16GB GDDR6", "clock": "~2400 MHz (Boost)", "power": "~220 Watts",
                "slot": "PCIe 4.0 x16",
                "compatibility": "Requires PCIe x16 slot, 650W+ PSU with 2x 8-pin PCIe connectors. Ensure case supports large GPUs with proper cooling."
            },

            "rx 9060 xt 8gb": {
                "name": "Gigabyte RX 9060 XT Gaming OC", "type": "GPU", "price": "₱26,000",
                "vram": "8GB GDDR6", "clock": "~2200 MHz (Boost)", "power": "~180 Watts",
                "slot": "PCIe 4.0 x16",
                "compatibility": "Requires PCIe x16 slot. Recommended 600W PSU with 2x 8-pin PCIe connectors. Ensure your case supports full-length GPUs."
            },
            "gtx 750 ti": {
                "name": "NVIDIA GTX 750 Ti", "type": "GPU", "price": "₱4,000",
                "vram": "4GB GDDR5", "clock": "~1085 MHz (Boost)", "power": "~60 Watts",
                "slot": "PCIe 3.0 x16",
                "compatibility": "Very low power draw (300W PSU recommended). Single 6-pin PCIe power connector or none depending on model. Fits in most cases due to compact size."
            },
            # ==========================
            # ========== CPUs ==========
            # ==========================
            "intel core i9-14900k": {
                "name": "Intel Core i9-14900K", "type": "CPU", "price": "₱39,000",
                "socket": "LGA 1700", "cores": "24 cores (8P + 16E), 32 threads",
                "clock": "3.2 GHz (P), 2.4 GHz (E)", "tdp": "125W TDP / 253W max",
                "compatibility": "Intel 600/700 series chipsets, BIOS update may be needed, Z790 recommended, requires strong cooling (240mm+), 750W+ PSU"
            },
            "intel core i7-14700k": {
                "name": "Intel Core i7-14700K", "type": "CPU", "price": "₱29,000",
                "socket": "LGA 1700", "cores": "20 cores (8P + 12E), 28 threads",
                "clock": "3.4 GHz (P), 2.5 GHz (E)", "tdp": "125W TDP / 253W max",
                "compatibility": "Z790 or B760, high-performance cooling, 750W+ PSU"
            },
            "intel core i7-13700k": {
                "name": "Intel Core i7-13700K", "type": "CPU", "price": "₱25,000",
                "socket": "LGA 1700", "cores": "16 cores (8P + 8E), 24 threads",
                "clock": "~3.4 GHz (P), ~2.5 GHz (E)", "tdp": "125W TDP / 253W max",
                "compatibility": "Z790 or B760, strong cooling, 700W+ PSU"
            },
            "intel core i5-14600k": {
                "name": "Intel Core i5-14600K", "type": "CPU", "price": "₱19,000",
                "socket": "LGA 1700", "cores": "14 cores (6P + 8E), 20 threads",
                "clock": "3.5 GHz (P), 2.6 GHz (E)", "tdp": "125W TDP / 181W max",
                "compatibility": "B760 or Z790, mid to high-end cooling, 650W+ PSU"
            },
            "intel core i5-14500": {
                "name": "Intel Core i5-14500", "type": "CPU", "price": "₱15,000",
                "socket": "LGA 1700", "cores": "14 cores (6P + 8E), 20 threads",
                "clock": "2.6 GHz (P), 1.9 GHz (E)", "tdp": "65W TDP / 154W max",
                "compatibility": "B760 or H610, basic cooling, 550W+ PSU"
            },
            "intel core i5-13400": {
                "name": "Intel Core i5-13400", "type": "CPU", "price": "₱13,000",
                "socket": "LGA 1700", "cores": "10 cores (6P + 4E), 16 threads",
                "clock": "2.5 GHz (P), 1.8 GHz (E)", "tdp": "65W TDP / 148W max",
                "compatibility": "H610 or B760, basic cooling, 500W+ PSU"
            },
            "intel core i3-14100": {
                "name": "Intel Core i3-14100", "type": "CPU", "price": "₱8,000",
                "socket": "LGA 1700", "cores": "4 cores (P only), 8 threads",
                "clock": "3.5 GHz (P)", "tdp": "60W TDP / 110W max",
                "compatibility": "H610 or B760, stock or basic cooling, 450W+ PSU"
            },
            "intel core i3-13100": {
                "name": "Intel Core i3-13100", "type": "CPU", "price": "₱7,500",
                "socket": "LGA 1700", "cores": "4 cores, 8 threads",
                "clock": "3.4 GHz (P)", "tdp": "60W TDP / ~89W max",
                "compatibility": "H610 or B760, stock or basic cooling, 450W+ PSU"
            },
            "amd ryzen 9 7950x": {
                "name": "AMD Ryzen 9 7950X", "type": "CPU", "price": "₱34,000",
                "socket": "AM5", "cores": "16 cores / 32 threads",
                "clock": "4.5 GHz", "tdp": "170W TDP / 230W max",
                "compatibility": "AM5 boards (X670E/X670/B650E), DDR5 only, 360mm+ AIO, 850W+ PSU"
            },
            "amd ryzen 9 9900x": {
                "name": "AMD Ryzen 9 9900X", "type": "CPU", "price": "TBD",
                "socket": "AM5 (expected)", "cores": "TBD",
                "clock": "TBD", "tdp": "TBD",
                "compatibility": "Expected AM5 + DDR5 + high cooling"
            },
            "amd ryzen 9 9900x3d": {
                "name": "AMD Ryzen 9 9900X3D", "type": "CPU", "price": "TBD",
                "socket": "AM5 (expected)", "cores": "TBD",
                "clock": "TBD", "tdp": "TBD",
                "compatibility": "Expected AM5, DDR5, advanced cooling due to 3D V-Cache"
            },
            "amd ryzen 7 7700x": {
                "name": "AMD Ryzen 7 7700X", "type": "CPU", "price": "₱21,000",
                "socket": "AM5", "cores": "8 cores / 16 threads",
                "clock": "4.5 GHz", "tdp": "105W TDP",
                "compatibility": "AM5 only, DDR5 only, 240mm AIO or mid-high air cooling, 650W+ PSU"
            },
            "amd ryzen 7 5700x": {
                "name": "AMD Ryzen 7 5700X", "type": "CPU", "price": "₱14,000",
                "socket": "AM4", "cores": "8 cores / 16 threads",
                "clock": "3.4 GHz", "tdp": "65W TDP",
                "compatibility": "AM4 boards (B550, X570), DDR4, BIOS update may be needed, 550W+ PSU"
            },
            "amd ryzen 5 5600x": {
                "name": "AMD Ryzen 5 5600X", "type": "CPU", "price": "₱11,000",
                "socket": "AM4", "cores": "6 cores / 12 threads",
                "clock": "3.7 GHz", "tdp": "65W TDP",
                "compatibility": "AM4 DDR4, B550/X570, basic to mid-air cooling, 550W+ PSU"
            },
            "amd ryzen 5 5600g": {
                "name": "AMD Ryzen 5 5600G", "type": "CPU", "price": "₱9,000",
                "socket": "AM4", "cores": "6 cores / 12 threads",
                "clock": "3.9 GHz", "tdp": "65W TDP",
                "compatibility": "AM4 DDR4, integrated GPU, stock cooling OK, 450W+ PSU"
            },
            "amd ryzen 3 3200g": {
                "name": "AMD Ryzen 3 3200G", "type": "CPU", "price": "₱5,000",
                "socket": "AM4", "cores": "4 cores / 4 threads",
                "clock": "3.6 GHz", "tdp": "65W TDP",
                "compatibility": "AM4, Vega graphics, stock cooler OK, 400W+ PSU"
            },
            "intel core i7-13700k": {
                "name": "Intel Core i7-13700K", "type": "CPU", "price": "₱25,000",
                "socket": "LGA 1700", "cores": "16 cores (8P + 8E), 24 threads",
                "clock": "~3.4 GHz (P), ~2.5 GHz (E)", "tdp": "125W TDP / 253W max",
                "compatibility": "Z790 or B760, strong cooling, 700W+ PSU"
            },
            "amd ryzen 7 5700x": {
                "name": "AMD Ryzen 7 5700X", "type": "CPU", "price": "₱14,000",
                "socket": "AM4", "cores": "8 cores / 16 threads",
                "clock": "3.4 GHz", "tdp": "65W TDP",
                "compatibility": "AM4 boards (B550, X570), DDR4, BIOS update may be needed, 550W+ PSU"
            },
            "intel core i7-13700k": {
                "name": "Intel Core i7-13700K", "type": "CPU", "price": "₱25,000",
                "socket": "LGA 1700", "cores": "16 cores (8P + 8E), 24 threads",
                "clock": "~3.4 GHz (P), ~2.5 GHz (E)", "tdp": "125W TDP / 253W max",
                "compatibility": "Z790 or B760, strong cooling, 700W+ PSU"
            },
            "intel core i5-14500": {
                "name": "Intel Core i5-14500", "type": "CPU", "price": "₱15,000",
                "socket": "LGA 1700", "cores": "14 cores (6P + 8E), 20 threads",
                "clock": "2.6 GHz (P), 1.9 GHz (E)", "tdp": "65W TDP / 154W max",
                "compatibility": "B760 or H610, basic cooling, 550W+ PSU"
            },
            "intel core i5-13400": {
                "name": "Intel Core i5-13400", "type": "CPU", "price": "₱13,000",
                "socket": "LGA 1700", "cores": "10 cores (6P + 4E), 16 threads",
                "clock": "2.5 GHz (P), 1.8 GHz (E)", "tdp": "65W TDP / 148W max",
                "compatibility": "H610 or B760, basic cooling, 500W+ PSU"
            },
            "intel core i3-14100": {
                "name": "Intel Core i3-14100", "type": "CPU", "price": "₱8,000",
                "socket": "LGA 1700", "cores": "4 cores (P only), 8 threads",
                "clock": "3.5 GHz (P)", "tdp": "60W TDP / 110W max",
                "compatibility": "H610 or B760, stock or basic cooling, 450W+ PSU"
            },
            "intel core i3-13100": {
                "name": "Intel Core i3-13100", "type": "CPU", "price": "₱7,500",
                "socket": "LGA 1700", "cores": "4 cores, 8 threads",
                "clock": "3.4 GHz (P)", "tdp": "60W TDP / ~89W max",
                "compatibility": "H610 or B760, stock or basic cooling, 450W+ PSU"
            },
            "amd ryzen 9 9900x": {
                "name": "AMD Ryzen 9 9900X", "type": "CPU", "price": "TBD",
                "socket": "AM5 (expected)", "cores": "TBD",
                "clock": "TBD", "tdp": "TBD",
                "compatibility": "Expected AM5 + DDR5 + high cooling"
            },
            "amd ryzen 9 9900x3d": {
                "name": "AMD Ryzen 9 9900X3D", "type": "CPU", "price": "TBD",
                "socket": "AM5 (expected)", "cores": "TBD",
                "clock": "TBD", "tdp": "TBD",
                "compatibility": "Expected AM5, DDR5, advanced cooling due to 3D V-Cache"
            },
            "amd ryzen 7 5700x": {
                "name": "AMD Ryzen 7 5700X", "type": "CPU", "price": "₱14,000",
                "socket": "AM4", "cores": "8 cores / 16 threads",
                "clock": "3.4 GHz", "tdp": "65W TDP",
                "compatibility": "AM4 boards (B550, X570), DDR4, BIOS update may be needed, 550W+ PSU"
            },
            "amd ryzen 5 5600g": {
                "name": "AMD Ryzen 5 5600G", "type": "CPU", "price": "₱9,000",
                "socket": "AM4", "cores": "6 cores / 12 threads",
                "clock": "3.9 GHz", "tdp": "65W TDP",
                "compatibility": "AM4 DDR4, integrated GPU, stock cooling OK, 450W+ PSU"
            },
            "amd ryzen 3 3200g": {
                "name": "AMD Ryzen 3 3200G", "type": "CPU", "price": "₱5,000",
                "socket": "AM4", "cores": "4 cores / 4 threads",
                "clock": "3.6 GHz", "tdp": "65W TDP",
                "compatibility": "AM4, Vega graphics, stock cooler OK, 400W+ PSU"
            },
            # ==================================
            # ========== Motherboards ==========
            # ==================================
            "asus prime b550m-k": {
                "name": "ASUS PRIME B550M-K", "type": "Motherboard", "price": "₱6,500",
                "socket": "AM4", "chipset": "B550", "form": "Micro-ATX", "ram": "DDR4, up to 128GB",
                "compatibility": "Ryzen 3000/5000 series (excluding 3200G/3400G without BIOS update)"
            },
            "msi b450m a pro max ii": {
                "name": "MSI B450M A PRO MAX II", "type": "Motherboard", "price": "₱4,500",
                "socket": "AM4", "chipset": "B450", "form": "Micro-ATX", "ram": "DDR4, up to 64GB",
                "compatibility": "Supports Ryzen 1000 to 5000 series with BIOS update"
            },
            "msi pro h610m s ddr4": {
                "name": "MSI PRO H610M-S DDR4", "type": "Motherboard", "price": "₱5,000",
                "socket": "LGA 1700", "chipset": "H610", "form": "Micro-ATX", "ram": "DDR4, up to 64GB",
                "compatibility": "Supports 12th/13th/14th Gen Intel CPUs"
            },
            "ramsta rs-b450mp": {
                "name": "RAMSTA RS-B450MP", "type": "Motherboard", "price": "₱3,800",
                "socket": "AM4", "chipset": "B450", "form": "Micro-ATX", "ram": "DDR4, up to 64GB",
                "compatibility": "Supports Ryzen 1000 to 5000 series (BIOS update may be needed)"
            },
            "ramsta rs-h311d4": {
                "name": "RAMSTA RS-H311D4", "type": "Motherboard", "price": "₱2,900",
                "socket": "LGA 1151", "chipset": "H310", "form": "Micro-ATX", "ram": "DDR4, up to 32GB",
                "compatibility": "Supports Intel 8th/9th Gen CPUs (Coffee Lake)"
            },
            "msi b650m gaming plus wifi": {
                "name": "MSI B650M Gaming Plus WiFi", "type": "Motherboard", "price": "₱12,500",
                "socket": "AM5", "chipset": "B650", "form": "Micro-ATX", "ram": "DDR5, up to 128GB",
                "compatibility": "Supports Ryzen 7000/8000 series"
            },
            "msi b760m gaming plus wifi ddr4": {
                "name": "MSI B760M Gaming Plus WiFi DDR4", "type": "Motherboard", "price": "₱8,000",
                "socket": "LGA 1700", "chipset": "B760", "form": "Micro-ATX", "ram": "DDR4, up to 128GB",
                "compatibility": "Supports Intel 12th/13th/14th Gen CPUs"
            },
            "gigabyte h610m k ddr4": {
                "name": "GIGABYTE H610M K DDR4", "type": "Motherboard", "price": "₱4,800",
                "socket": "LGA 1700", "chipset": "H610", "form": "Micro-ATX", "ram": "DDR4, up to 64GB",
                "compatibility": "Supports Intel 12th/13th/14th Gen CPUs"
            },
            # ==========================
            # ========== RAM ==========
            # ==========================
            "kingston fury beast ddr4": {
                "name": "Kingston FURY Beast DDR4", "type": "RAM", "price": "₱2,000",
                "capacity": "8GB, 16GB, or 32GB", "speed": "3200 MHz", "memory_type": "DDR4",
                "compatibility": "Requires motherboard with DDR4 DIMM slots (288-pin) supporting 1.35V and 3200 MHz. Check motherboard QVL (Qualified Vendor List) for guaranteed compatibility."
            },
            "kingston hyperx fury ddr3": {
                "name": "Kingston HyperX FURY DDR3", "type": "RAM", "price": "₱1,200",
                "capacity": "8GB", "speed": "1600 MHz", "memory_type": "DDR3",
                "compatibility": "For older systems only. Requires a DDR3 (240-pin) motherboard. Incompatible with modern DDR4/DDR5 systems."
            },
            "hkc pc ddr4-3200 dimm": {
                "name": "HKC PC DDR4-3200 DIMM", "type": "RAM", "price": "₱1,800",
                "capacity": "8GB", "speed": "3200 MHz", "memory_type": "DDR4",
                "compatibility": "Works with DDR4 (288-pin) motherboards supporting 1.2V and 3200 MHz. Recommend using matched pairs and checking motherboard QVL."
            },
            "hkcmemory hu40 ddr4 (16gb)": {
                "name": "HKCMEMORY HU40 DDR4 (16GB)", "type": "RAM", "price": "₱3,500",
                "capacity": "16GB", "speed": "3200 MHz", "memory_type": "DDR4",
                "compatibility": "Compatible with DDR4 (288-pin) motherboards supporting 1.2V and 3200 MHz. Check QVL for higher capacity module compatibility."
            },
            "hkcmemory hu40 ddr4 (8gb)": {
                "name": "HKCMEMORY HU40 DDR4 (8GB)", "type": "RAM", "price": "₱1,700",
                "capacity": "8GB", "speed": "3200 MHz", "memory_type": "DDR4",
                "compatibility": "Compatible with DDR4 (288-pin) motherboards supporting 1.2V and 3200 MHz."
            },
            # =============================
            # ========== Storage ==========
            # =============================
            "seagate barracuda 1tb": {
                "name": "Seagate Barracuda 1TB", "type": "Storage", "price": "₱2,500",
                "capacity": "1TB", "interface": "SATA 6Gb/s", "form": "3.5-inch",
                "compatibility": "Requires a motherboard with an available SATA port and a SATA power connector from the PSU. Ensure your case has a 3.5-inch drive bay. It's a good choice for bulk storage."
            },
            "western digital blue 2tb": {
                "name": "Western Digital Blue 2TB", "type": "Storage", "price": "₱3,800",
                "capacity": "2TB", "interface": "SATA 6Gb/s", "form": "3.5-inch",
                "compatibility": "Requires a motherboard with an available SATA port and a SATA power connector from the PSU. Ensure your case has a 3.5-inch drive bay. Excellent for larger storage needs."
            },
            "samsung 970 evo plus 1tb": {
                "name": "Samsung 970 EVO Plus 1TB", "type": "Storage", "price": "₱5,500",
                "capacity": "1TB", "interface": "PCIe Gen 3.0 x4", "form": "M.2 2280",
                "compatibility": "Requires a motherboard with an available M.2 slot supporting PCIe Gen 3.0 x4 NVMe SSDs. Check if your motherboard shares M.2 bandwidth with SATA ports."
            },
            "crucial mx500 500gb": {
                "name": "Crucial MX500 500GB", "type": "Storage", "price": "₱3,000",
                "capacity": "500GB", "interface": "SATA 6Gb/s", "form": "2.5-inch",
                "compatibility": "Requires a motherboard with an available SATA port and a SATA power connector from the PSU. Ensure your case has a 2.5-inch drive bay. It's a reliable and cost-effective option for a fast boot drive or general storage."
            },
            "seagate barracuda 1tb": {
                "name": "Seagate Barracuda 1TB", "type": "Storage", "price": "₱2,500",
                "capacity": "1TB", "interface": "SATA 6Gb/s", "form": "3.5-inch",
                "compatibility": "Requires a motherboard with an available SATA port and a SATA power connector from the PSU. Ensure your case has a 3.5-inch drive bay. It's a good choice for bulk storage."
            },
            "rx 9060 xt 8gb": {
                "name": "Gigabyte RX 9060 XT Gaming OC", "type": "GPU", "price": "₱26,000",
                "vram": "8GB GDDR6", "clock": "~2200 MHz (Boost)", "power": "~180 Watts",
                "slot": "PCIe 4.0 x16",
                "compatibility": "Requires PCIe x16 slot. Recommended 600W PSU with 2x 8-pin PCIe connectors. Ensure your case supports full-length GPUs."
            },
            "gtx 750 ti": {
                "name": "NVIDIA GTX 750 Ti", "type": "GPU", "price": "₱4,000",
                "vram": "4GB GDDR5", "clock": "~1085 MHz (Boost)", "power": "~60 Watts",
                "slot": "PCIe 3.0 x16",
                "compatibility": "Very low power draw (300W PSU recommended). Single 6-pin PCIe power connector or none depending on model. Fits in most cases due to compact size."
            },
            "rx 9060 xt 16gb": {  # failed
                "name": "Sapphire RX 9060 XT", "type": "GPU", "price": "₱32,000",
                "vram": "16GB GDDR6", "clock": "~2400 MHz (Boost)", "power": "~220 Watts",
                "slot": "PCIe 4.0 x16",
                "compatibility": "Requires PCIe x16 slot, 650W+ PSU with 2x 8-pin PCIe connectors. Ensure case supports large GPUs with proper cooling."
            },
            "western digital blue 2tb": {
                "name": "Western Digital Blue 2TB", "type": "Storage", "price": "₱3,800",
                "capacity": "2TB", "interface": "SATA 6Gb/s", "form": "3.5-inch",
                "compatibility": "Requires a motherboard with an available SATA port and a SATA power connector from the PSU. Ensure your case has a 3.5-inch drive bay. Excellent for larger storage needs."
            },
            "crucial mx500 500gb": {
                "name": "Crucial MX500 500GB", "type": "Storage", "price": "₱3,000",
                "capacity": "500GB", "interface": "SATA 6Gb/s", "form": "2.5-inch",
                "compatibility": "Requires a motherboard with an available SATA port and a SATA power connector from the PSU. Ensure your case has a 2.5-inch drive bay. It's a reliable and cost-effective option for a fast boot drive or general storage."
            },
            "seagate barracuda 1tb": {
                "name": "Seagate Barracuda 1TB", "type": "Storage", "price": "₱2,500",
                "capacity": "1TB", "interface": "SATA 6Gb/s", "form": "3.5-inch",
                "compatibility": "Requires a motherboard with an available SATA port and a SATA power connector from the PSU. Ensure your case has a 3.5-inch drive bay. It's a good choice for bulk storage."
            },
            # ==========================
            # ========== PSUs ==========
            # ==========================
            "corsair rm850x": {
                "name": "Corsair RM850x", "type": "PSU", "price": "₱8,000",
                "wattage": "850W", "efficiency": "80 Plus Gold", "modular": "Fully Modular",
                "compatibility": "Great for high-performance gaming PCs (RTX 30/40, RX 6000/7000)."
            },
            "cooler master mwe white 750w": {  # failed
                "name": "Cooler Master MWE White 750W", "type": "PSU", "price": "₱3,500",
                "wattage": "750W", "efficiency": "80 Plus White", "modular": "Non-Modular",
                "compatibility": "Best for mid-range PCs. Ensure your GPU's PCIe connectors match. Non-modular = harder cable management."
            },
            "corsair cx650": {
                "name": "Corsair CX650", "type": "PSU", "price": "₱4,000",
                "wattage": "650W", "efficiency": "80 Plus Bronze", "modular": "Non-Modular",
                "compatibility": "Good for Ryzen 5/i5 builds with GPUs like RTX 3050/3060 or RX 6600. Watch for cable clutter (non-modular)."
            },
            "cougar gx-f 750w": {
                "name": "Cougar GX-F 750W", "type": "PSU", "price": "₱5,500",
                "wattage": "750W", "efficiency": "80 Plus Gold", "modular": "Fully Modular",
                "compatibility": "Great for mid to high-end builds. Fully modular makes cable management easier."
            },
            "seasonic focus plus gold 550w": {
                "name": "Seasonic Focus Plus Gold 550W", "type": "PSU", "price": "₱6,000",
                "wattage": "550W", "efficiency": "80 Plus Gold", "modular": "Fully Modular",
                "compatibility": "Ideal for entry-level to mid-range builds with RTX 3050/3060, RX 6600. Fully modular = neat builds."
            },
            # ===============================
            # ========== Case Fans ==========
            # ===============================
            "coolmoon yx120": {
                "name": "COOLMOON YX120", "type": "Case Fan", "price": "₱250",
                "size": "120mm", "rpm": "1200 RPM", "airflow": "38 CFM", "noise": "20 dBA"
            },
            "cooler master sickleflow 120 argb": {
                "name": "Cooler Master SickleFlow 120 ARGB", "type": "Case Fan", "price": "₱600",
                "size": "120mm", "rpm": "650-1800 RPM", "airflow": "62 CFM", "noise": "8-27 dBA"
            },
            "arctic p12 pwm pst": {
                "name": "Arctic P12 PWM PST", "type": "Case Fan", "price": "₱450",
                "size": "120mm", "rpm": "200-1800 RPM", "airflow": "56.3 CFM", "noise": "0.3 Sone"
            },
            # =================================
            # ========== CPU Coolers ==========
            # =================================
            "coolmoon aosor s400": {
                "name": "COOLMOON AOSOR S400", "type": "CPU Cooler", "price": "₱1,200",
                "cooler_type": "Air Cooler", "fan_size": "120mm", "tdp": "Up to 130W",
                "sockets": "Intel LGA 1700/1200/115X, AMD AM4"
            },
            "cooler master hyper 212 black edition": {
                "name": "Cooler Master Hyper 212 Black Edition", "type": "CPU Cooler", "price": "₱2,500",
                "cooler_type": "Air Cooler", "fan_size": "120mm", "tdp": "Up to 150W",
                "sockets": "Intel LGA 1700/1200/115X, AMD AM4/AM5"
            },
            "thermalright peerless assassin 120 se": {
                "name": "Thermalright Peerless Assassin 120 SE", "type": "CPU Cooler", "price": "₱3,000",
                "cooler_type": "Dual-Tower Air Cooler", "fan_size": "2x 120mm", "tdp": "Up to 245W",
                "sockets": "Intel LGA 1700/1200/115X, AMD AM4/AM5"
            },
            "deepcool le500 marrs": {
                "name": "Deepcool LE500 MARRS", "type": "CPU Cooler", "price": "₱4,500",
                "cooler_type": "AIO Liquid Cooler (240mm)", "fan_size": "2x 120mm", "tdp": "Up to 220W",
                "sockets": "Intel LGA 1700/1200/115X, AMD AM4/AM5"
            },
            "cooler master mwe white 750w": {  # failed
                "name": "Cooler Master MWE White 750W", "type": "PSU", "price": "₱3,500",
                "wattage": "750W", "efficiency": "80 Plus White", "modular": "Non-Modular",
                "compatibility": "Best for mid-range PCs. Ensure your GPU's PCIe connectors match. Non-modular = harder cable management."
            },
            "seasonic focus plus gold 550w": {
                "name": "Seasonic Focus Plus Gold 550W", "type": "PSU", "price": "₱6,000",
                "wattage": "550W", "efficiency": "80 Plus Gold", "modular": "Fully Modular",
                "compatibility": "Ideal for entry-level to mid-range builds with RTX 3050/3060, RX 6600. Fully modular = neat builds."
            }
        }
        return components

    def find_component(self, query):
        """Find the most relevant component using SMART matching"""
        query_lower = query.lower().strip()

        print(f"Searching: '{query}'")

        # STRATEGY 1: EXACT NAME MATCH
        for comp_key, component in self.components_db.items():
            if query_lower == component['name'].lower():
                print(f" EXACT MATCH: {component['name']}")
                return component, 1.0

        # STRATEGY 2: KEYWORD MATCHING FOR COMMON COMPONENTS
        keyword_mapping = {
            # GPU
            "rtx 3050": "rtx 3050",
            "3050": "rtx 3050",
            "geforce rtx 3050": "rtx 3050",
            "rtx 4060": "rtx 4060",
            "4060": "rtx 4060",
            "geforce rtx 4060": "rtx 4060",
            "rx 9060 xt": "rx 9060 xt 8gb",
            "rx 9060": "rx 9060 xt 8gb",
            "radeon rx 9060": "rx 9060 xt 8gb",
            "gtx 750 ti": "gtx 750 ti",
            "750 ti": "gtx 750 ti",
            "geforce gtx 750 ti": "gtx 750 ti",
            "rtx 3060": "rtx 3060",
            "3060": "rtx 3060",
            "geforce rtx 3060": "rtx 3060",

            # CPU mappings - Intel
            "i9 14900k": "intel core i9-14900k",
            "14900k": "intel core i9-14900k",
            "core i9": "intel core i9-14900k",
            "i7 14700k": "intel core i7-14700k",
            "14700k": "intel core i7-14700k",
            "i7 13700k": "intel core i7-13700k",
            "13700k": "intel core i7-13700k",
            "i5 14600k": "intel core i5-14600k",
            "14600k": "intel core i5-14600k",
            "i5 14500": "intel core i5-14500",
            "14500": "intel core i5-14500",
            "i5 13400": "intel core i5-13400",
            "13400": "intel core i5-13400",
            "i3 14100": "intel core i3-14100",
            "14100": "intel core i3-14100",
            "i3 13100": "intel core i3-13100",
            "13100": "intel core i3-13100",

            # CPU mappings - AMD
            "ryzen 9 7950x": "amd ryzen 9 7950x",
            "7950x": "amd ryzen 9 7950x",
            "ryzen 9 9900x": "amd ryzen 9 9900x",
            "9900x": "amd ryzen 9 9900x",
            "ryzen 9 9900x3d": "amd ryzen 9 9900x3d",
            "9900x3d": "amd ryzen 9 9900x3d",
            "ryzen 7 7700x": "amd ryzen 7 7700x",
            "7700x": "amd ryzen 7 7700x",
            "ryzen 7 5700x": "amd ryzen 7 5700x",
            "5700x": "amd ryzen 7 5700x",
            "ryzen 5 5600x": "amd ryzen 5 5600x",
            "5600x": "amd ryzen 5 5600x",
            "ryzen 5 5600g": "amd ryzen 5 5600g",
            "5600g": "amd ryzen 5 5600g",
            "ryzen 3 3200g": "amd ryzen 3 3200g",
            "3200g": "amd ryzen 3 3200g",

            # Motherboard mappings
            "asus prime b550m": "asus prime b550m-k",
            "b550m": "asus prime b550m-k",
            "msi b450m": "msi b450m a pro max ii",
            "b450m": "msi b450m a pro max ii",
            "msi h610m": "msi pro h610m s ddr4",
            "h610m": "msi pro h610m s ddr4",
            "ramsta b450": "ramsta rs-b450mp",
            "ramsta h311": "ramsta rs-h311d4",
            "msi b650m": "msi b650m gaming plus wifi",
            "b650m": "msi b650m gaming plus wifi",
            "msi b760m": "msi b760m gaming plus wifi ddr4",
            "b760m": "msi b760m gaming plus wifi ddr4",
            "gigabyte h610m": "gigabyte h610m k ddr4",

            # RAM mappings
            "kingston fury beast": "kingston fury beast ddr4",
            "fury beast": "kingston fury beast ddr4",
            "kingston hyperx fury": "kingston hyperx fury ddr3",
            "hyperx fury": "kingston hyperx fury ddr3",
            "hkc ddr4": "hkc pc ddr4-3200 dimm",
            "hkc memory": "hkcmemory hu40 ddr4 (16gb)",

            # Storage mappings
            "seagate 1tb": "seagate barracuda 1tb",
            "wd blue 2tb": "western digital blue 2tb",
            "samsung 970 evo": "samsung 970 evo plus 1tb",
            "crucial mx500": "crucial mx500 500gb",

            # PSU mappings
            "corsair rm850x": "corsair rm850x",
            "rm850x": "corsair rm850x",
            "cooler master 750w": "cooler master mwe white 750w",
            "corsair cx650": "corsair cx650",
            "cx650": "corsair cx650",
            "cougar 750w": "cougar gx-f 750w",
            "seasonic 550w": "seasonic focus plus gold 550w",

            # Case Fan mappings
            "coolmoon fan": "coolmoon yx120",
            "cooler master sickleflow": "cooler master sickleflow 120 argb",
            "arctic p12": "arctic p12 pwm pst",

            # CPU Cooler mappings
            "coolmoon cooler": "coolmoon aosor s400",
            "hyper 212": "cooler master hyper 212 black edition",
            "peerless assassin": "thermalright peerless assassin 120 se",
            "deepcool le500": "deepcool le500 marrs"
        }

        for keyword, expected_type in keyword_mapping.items():
            if keyword in query_lower:
                # Find component of expected type that matches the keyword
                for comp_key, component in self.components_db.items():
                    if (component['type'] == expected_type and
                            keyword in component['name'].lower()):
                        print(f" KEYWORD MATCH: {component['name']}")
                        return component, 0.9

        # STRATEGY 3: AI EMBEDDINGS MATCHING
        print("Using AI embeddings....")
        query_embedding = self.model.encode(query, convert_to_tensor=True)
        similarities = util.cos_sim(query_embedding, self.embeddings)[0]

        # Show top matches for debugging
        top_matches = torch.topk(similarities, min(3, len(similarities)))
        for i in range(len(top_matches.indices)):
            idx = top_matches.indices[i].item()
            score = top_matches.values[i].item()
            component_key = self.component_names[idx]
            component = self.components_db[component_key]
            print(
                f"   AI Match {i+1}: {component['name']} - Score: {score:.3f}")

        best_match_idx = torch.argmax(similarities).item()
        best_score = similarities[best_match_idx].item()

        if best_score > 0.3:
            component_key = self.component_names[best_match_idx]
            component = self.components_db[component_key]
            print(f"AI SELECTED: {component['name']}")
            return component, best_score

        print("NO MATCH FOUND")
        return None, best_score

    def check_compatibility(self, component1_name, component2_name):
        """Check compatibility between two components and explain why"""
        comp1, score1 = self.find_component(component1_name)
        comp2, score2 = self.find_component(component2_name)

        if not comp1 or not comp2:
            return f"I couldn't find one or both components. Please check the names."

        comp1_type = comp1['type']
        comp2_type = comp2['type']

        # Debug: Show what components were found
        print(
            f"DEBUG: Found {comp1['name']} ({comp1_type}) and {comp2['name']} ({comp2_type})")

        # CPU-Motherboard Compatibility
        if (comp1_type == 'CPU' and comp2_type == 'Motherboard') or (comp1_type == 'Motherboard' and comp2_type == 'CPU'):
            cpu = comp1 if comp1_type == 'CPU' else comp2
            mobo = comp2 if comp2_type == 'Motherboard' else comp1

            cpu_socket = cpu.get('socket', '')
            mobo_socket = mobo.get('socket', '')

            if cpu_socket and mobo_socket:
                if cpu_socket == mobo_socket:
                    return f"COMPATIBLE\n{cpu['name']} fits {mobo['name']}\n\nWhy: Same socket type ({cpu_socket}) means physical and electrical compatibility."
                else:
                    return f"NOT COMPATIBLE\n{cpu['name']} doesn't fit {mobo['name']}\n\nWhy: Different socket types ({cpu_socket} vs {mobo_socket}) - physically incompatible."
            else:
                return f"CANNOT DETERMINE\nMissing socket information."

        # Motherboard-RAM Compatibility
        elif (comp1_type == 'Motherboard' and comp2_type == 'RAM') or (comp1_type == 'RAM' and comp2_type == 'Motherboard'):
            mobo = comp1 if comp1_type == 'Motherboard' else comp2
            ram = comp2 if comp2_type == 'RAM' else comp1

            mobo_ram_type = mobo.get('ram', '')
            ram_type = ram.get('memory_type', '')

            if ram_type and mobo_ram_type:
                if ram_type in mobo_ram_type:
                    return f"COMPATIBLE\n{ram['name']} works with {mobo['name']}\n\nWhy: RAM type ({ram_type}) matches motherboard support ({mobo_ram_type})."
                else:
                    return f"NOT COMPATIBLE\n{ram['name']} doesn't work with {mobo['name']}\n\nWhy: Different RAM generations ({ram_type} vs {mobo_ram_type}) - physically incompatible."
            else:
                return f"CANNOT DETERMINE\nMissing RAM type information."

        # PSU-GPU Compatibility (Power)
        elif (comp1_type == 'PSU' and comp2_type == 'GPU') or (comp1_type == 'GPU' and comp2_type == 'PSU'):
            psu = comp1 if comp1_type == 'PSU' else comp2
            gpu = comp2 if comp2_type == 'GPU' else comp1

            psu_wattage = int(psu.get('wattage', '0W').replace('W', ''))
            gpu_power_match = re.findall(r'\d+', gpu.get('power', '0W'))
            gpu_power = int(gpu_power_match[0]) if gpu_power_match else 0

            if psu_wattage >= gpu_power + 150:
                return f"COMPATIBLE\n{psu['name']} can power {gpu['name']}\n\nWhy: PSU has sufficient wattage ({psu_wattage}W) for GPU ({gpu_power}W) with safety margin."
            elif psu_wattage >= gpu_power + 50:
                return f" BORDERLINE\n{psu['name']} might be enough for {gpu['name']}\n\nWhy: PSU wattage ({psu_wattage}W) is minimal for GPU ({gpu_power}W) - consider higher wattage."
            else:
                return f" NOT COMPATIBLE\n{psu['name']} is too weak for {gpu['name']}\n\nWhy: PSU ({psu_wattage}W) doesn't have enough power for GPU ({gpu_power}W)."

        # PSU-CPU Compatibility
        elif (comp1_type == 'PSU' and comp2_type == 'CPU') or (comp1_type == 'CPU' and comp2_type == 'PSU'):
            psu = comp1 if comp1_type == 'PSU' else comp2
            cpu = comp2 if comp2_type == 'CPU' else comp1

            psu_wattage = int(psu.get('wattage', '0W').replace('W', ''))
            cpu_tdp_match = re.findall(r'\d+', cpu.get('tdp', '0W'))
            cpu_tdp = int(cpu_tdp_match[0]) if cpu_tdp_match else 0

            if psu_wattage >= cpu_tdp + 300:
                return f"COMPATIBLE\n{psu['name']} is sufficient for {cpu['name']}\n\nWhy: PSU has plenty of power ({psu_wattage}W) for CPU ({cpu_tdp}W)."
            else:
                return f"CHECK GPU\n{psu['name']} might be borderline with high-end GPU\n\nWhy: Consider total system power including GPU."

        # CPU-GPU Compatibility (General)
        elif (comp1_type == 'CPU' and comp2_type == 'GPU') or (comp1_type == 'GPU' and comp2_type == 'CPU'):
            cpu = comp1 if comp1_type == 'CPU' else comp2
            gpu = comp2 if comp2_type == 'GPU' else comp1
            return f"✅ COMPATIBLE\n{cpu['name']} and {gpu['name']} work together\n\nWhy: All modern CPUs and GPUs are compatible via PCIe slots."

        # Motherboard-Storage Compatibility
        elif (comp1_type == 'Motherboard' and comp2_type == 'Storage') or (comp1_type == 'Storage' and comp2_type == 'Motherboard'):
            mobo = comp1 if comp1_type == 'Motherboard' else comp2
            storage = comp2 if comp2_type == 'Storage' else comp1

            storage_interface = storage.get('interface', '')

            if 'M.2' in storage_interface or 'NVMe' in storage_interface:
                return f" COMPATIBLE\n{storage['name']} works with {mobo['name']}\n\nWhy: NVMe SSDs require M.2 slots with PCIe support."
            elif 'SATA' in storage_interface:
                return f" COMPATIBLE\n{storage['name']} works with {mobo['name']}\n\nWhy: SATA is universal standard for storage."

        # Case Fan compatibility (works with any motherboard)
        elif (comp1_type == 'Case Fan' and comp2_type == 'Motherboard') or (comp1_type == 'Motherboard' and comp2_type == 'Case Fan'):
            fan = comp1 if comp1_type == 'Case Fan' else comp2
            mobo = comp2 if comp2_type == 'Motherboard' else comp1
            return f"COMPATIBLE\n{fan['name']} works with {mobo['name']}\n\nWhy: Case fans use standard motherboard fan headers."

        # CPU Cooler compatibility (check sockets)
        elif (comp1_type == 'CPU Cooler' and comp2_type == 'CPU') or (comp1_type == 'CPU' and comp2_type == 'CPU Cooler'):
            cooler = comp1 if comp1_type == 'CPU Cooler' else comp2
            cpu = comp2 if comp2_type == 'CPU' else comp1

            cpu_socket = cpu.get('socket', '')
            cooler_sockets = cooler.get('sockets', '')

            if cpu_socket and cooler_sockets:
                if cpu_socket in cooler_sockets:
                    return f" COMPATIBLE\n{cooler['name']} works with {cpu['name']}\n\nWhy: Cooler supports {cpu_socket} socket."
                else:
                    return f" NOT COMPATIBLE\n{cooler['name']} doesn't work with {cpu['name']}\n\nWhy: Cooler doesn't support {cpu_socket} socket."
            else:
                return f" LIKELY COMPATIBLE\n{cooler['name']} should work with {cpu['name']}\n\nWhy: Most coolers support multiple sockets."

        # General compatibility for same type components
        elif comp1_type == comp2_type:
            return f" NOT COMPATIBLE\n{comp1['name']} and {comp2['name']} are both {comp1_type}s\n\nWhy: You can't use two {comp1_type}s of the same type together."

        # Default - assume compatible for other combinations
        return f" LIKELY COMPATIBLE\n{comp1['name']} and {comp2['name']} should work together\n\nWhy: Standard PC components are generally compatible."

    def generate_exact_value_response(self, user_message, component):
        """Generate EXACT VALUE ONLY based on what user asked"""
        user_lower = user_message.lower()

        if any(word in user_lower for word in ['details', 'specs', 'specifications', 'full', 'everything']):
            response = f"{component['name']} ({component['type']})\n\n"

            if component['type'] == 'CPU':
                if 'price' in component:
                    response += f"Price: {component['price']}\n"
                if 'socket' in component:
                    response += f"Socket: {component['socket']}\n"
                if 'cores' in component:
                    response += f"Cores/Threads: {component['cores']}\n"
                if 'clock' in component:
                    response += f"Clock Speed: {component['clock']}\n"
                if 'tdp' in component:
                    response += f"TDP: {component['tdp']}\n"
                if 'compatibility' in component:
                    response += f"Compatibility: {component['compatibility']}\n"

            elif component['type'] == 'GPU':
                if 'price' in component:
                    response += f"Price: {component['price']}\n"
                if 'vram' in component:
                    response += f"VRAM: {component['vram']}\n"
                if 'clock' in component:
                    response += f"Clock Speed: {component['clock']}\n"
                if 'power' in component:
                    response += f"Power Consumption: {component['power']}\n"
                if 'slot' in component:
                    response += f"Slot Type: {component['slot']}\n"
                if 'compatibility' in component:
                    response += f"Compatibility: {component['compatibility']}\n"

            elif component['type'] == 'Motherboard':
                if 'price' in component:
                    response += f"Price: {component['price']}\n"
                if 'socket' in component:
                    response += f"Socket: {component['socket']}\n"
                if 'chipset' in component:
                    response += f"Chipset: {component['chipset']}\n"
                if 'form' in component:
                    response += f"Form Factor: {component['form']}\n"
                if 'ram' in component:
                    response += f"RAM Support: {component['ram']}\n"
                if 'compatibility' in component:
                    response += f"Compatibility: {component['compatibility']}\n"

            elif component['type'] == 'RAM':
                if 'price' in component:
                    response += f"Price: {component['price']}\n"
                if 'capacity' in component:
                    response += f"Capacity: {component['capacity']}\n"
                if 'speed' in component:
                    response += f"Speed: {component['speed']}\n"
                if 'memory_type' in component:
                    response += f"Type: {component['memory_type']}\n"
                if 'compatibility' in component:
                    response += f"Compatibility: {component['compatibility']}\n"

            elif component['type'] == 'Storage':
                if 'price' in component:
                    response += f"Price: {component['price']}\n"
                if 'capacity' in component:
                    response += f"Capacity: {component['capacity']}\n"
                if 'interface' in component:
                    response += f"Interface: {component['interface']}\n"
                if 'form' in component:
                    response += f"Form Factor: {component['form']}\n"
                if 'compatibility' in component:
                    response += f"Compatibility: {component['compatibility']}\n"

            elif component['type'] == 'PSU':
                if 'price' in component:
                    response += f"Price: {component['price']}\n"
                if 'wattage' in component:
                    response += f"Wattage: {component['wattage']}\n"
                if 'efficiency' in component:
                    response += f"Efficiency: {component['efficiency']}\n"
                if 'modular' in component:
                    response += f"Modularity: {component['modular']}\n"
                if 'compatibility' in component:
                    response += f"Compatibility: {component['compatibility']}\n"

            elif component['type'] == 'Case Fan':
                if 'price' in component:
                    response += f"Price: {component['price']}\n"
                if 'size' in component:
                    response += f"Size: {component['size']}\n"
                if 'rpm' in component:
                    response += f"RPM: {component['rpm']}\n"
                if 'airflow' in component:
                    response += f"Airflow: {component['airflow']}\n"
                if 'noise' in component:
                    response += f"Noise: {component['noise']}\n"

            elif component['type'] == 'CPU Cooler':
                if 'price' in component:
                    response += f"Price: {component['price']}\n"
                if 'cooler_type' in component:
                    response += f"Type: {component['cooler_type']}\n"
                if 'fan_size' in component:
                    response += f"Fan Size: {component['fan_size']}\n"
                if 'tdp' in component:
                    response += f"Max TDP: {component['tdp']}\n"
                if 'sockets' in component:
                    response += f"Compatible Sockets: {component['sockets']}\n"

            return response

        # ===== SPECIFIC ATTRIBUTES - PERFECT ORDER! =====

    # 1. TYPE QUESTIONS - UNA
        if any(word in user_lower for word in ['type']):
            return f"{component['type']}"

    # 2. VRAM QUESTIONS (GPUs)
        if any(word in user_lower for word in ['vram', 'video memory', 'graphics memory']):
            if 'vram' in component:
                return f"{component['vram']}"

    # 3. CLOCK SPEED QUESTIONS (CPUs, GPUs)
        if any(word in user_lower for word in ['clock', 'speed', 'frequency', 'ghz', 'mhz']):
            if 'clock' in component:
                return f"{component['clock']}"
        elif 'speed' in component:
            return f"{component['speed']}"

    # 4. SLOT QUESTIONS (GPUs)
        if any(word in user_lower for word in ['slot', 'pcie']):
            if 'slot' in component:
                return f"{component['slot']}"

    # 5. SOCKET QUESTIONS (CPUs, Motherboards)
        if any(word in user_lower for word in ['socket']):
            if 'socket' in component:
                return f"{component['socket']}"

    # 6. CORES/THREADS QUESTIONS (CPUs)
        if any(word in user_lower for word in ['core', 'thread', 'cores', 'threads']):
            if 'cores' in component:
                return f"{component['cores']}"

    # 7. CHIPSET QUESTIONS (Motherboards)
        if any(word in user_lower for word in ['chipset']):
            if 'chipset' in component:
                return f"{component['chipset']}"

    # 8. FORM FACTOR QUESTIONS (Motherboards)
        if any(word in user_lower for word in ['form', 'atx', 'micro-atx']):
            if 'form' in component:
                return f"{component['form']}"

    # 9. RAM SUPPORT QUESTIONS (Motherboards)
        if any(word in user_lower for word in ['ram support', 'memory support']):
            if 'ram' in component:
                return f"{component['ram']}"

    # 10. CAPACITY QUESTIONS (Storage, RAM)
        if any(word in user_lower for word in ['capacity', 'tb', 'gb']):
            if 'capacity' in component:
                return f"{component['capacity']}"

    # 11. INTERFACE QUESTIONS (Storage)
        if any(word in user_lower for word in ['interface']):
            if 'interface' in component:
                return f"{component['interface']}"

    # 12. MEMORY TYPE QUESTIONS (RAM)
        if any(word in user_lower for word in ['memory type', 'memory_type', 'ddr']):
            if 'memory_type' in component:
                return f"{component['memory_type']}"

    # 13. SPEED QUESTIONS (RAM)
        if any(word in user_lower for word in ['speed', 'mhz']):
            if 'speed' in component:
                return f"{component['speed']}"

    # 14. RPM QUESTIONS (Fans)
        if any(word in user_lower for word in ['rpm']):
            if 'rpm' in component:
                return f"{component['rpm']}"

    # 15. AIRFLOW QUESTIONS (Fans)
        if any(word in user_lower for word in ['airflow', 'cfm']):
            if 'airflow' in component:
                return f"{component['airflow']}"

    # 16. NOISE QUESTIONS (Fans)
        if any(word in user_lower for word in ['noise', 'db', 'dba', 'sound']):
            if 'noise' in component:
                return f"{component['noise']}"

    # 17. SIZE QUESTIONS (Fans, Storage)
        if any(word in user_lower for word in ['size']):
            if 'size' in component:
                return f"{component['size']}"

    # 18. COOLER TYPE QUESTIONS (CPU Coolers)
        if any(word in user_lower for word in ['cooler type', 'cooler_type']):
            if 'cooler_type' in component:
                return f"{component['cooler_type']}"

    # 19. FAN SIZE QUESTIONS (CPU Coolers)
        if any(word in user_lower for word in ['fan size', 'fan_size']):
            if 'fan_size' in component:
                return f"{component['fan_size']}"

    # 20. COMPATIBLE SOCKETS QUESTIONS (CPU Coolers)
        if any(word in user_lower for word in ['sockets', 'compatible sockets']):
            if 'sockets' in component:
                return f"{component['sockets']}"

    # 21. MAX TDP QUESTIONS (CPU Coolers)
        if any(word in user_lower for word in ['max tdp', 'cooler tdp']):
            if 'tdp' in component:
                return f"{component['tdp']}"

    # 22. EFFICIENCY QUESTIONS (PSUs)
        if any(word in user_lower for word in ['efficiency', '80 plus', 'gold', 'bronze']):
            if 'efficiency' in component:
                return f"{component['efficiency']}"

    # 23. MODULARITY QUESTIONS (PSUs)
        if any(word in user_lower for word in ['modular', 'modularity']):
            if 'modular' in component:
                return f"{component['modular']}"

    # 24. POWER/WATTAGE QUESTIONS - BAGO PRICE
        if any(word in user_lower for word in ['wattage', 'watts', 'power']):
            if 'power' in component:  # ← ITO ANG MERON KA!
                return f"{component['power']}"  # "~130 Watts"
        elif 'wattage' in component:
            return f"{component['wattage']}"
        elif 'tdp' in component:
            return f"{component['tdp']}"

    # 25. PRICE QUESTIONS - PINAKA-HULI
        if any(word in user_lower for word in ['price', 'cost', 'how much', 'magkano']):
            if 'price' in component:
                return f"{component['price']}"
        # DEFAULT
        if 'price' in component:
            return f"{component['price']}"
        elif 'wattage' in component:
            return f"{component['wattage']}"
        elif 'socket' in component:
            return f"{component['socket']}"
        else:
            return f"{component['name']}"

    def check_previous_training(self, user_query):
        """Check if we have the exact same query in training data"""
        for example in self.training_data:
            if user_query.lower() == example['user_query'].lower():
                return example['ai_response']
        return None

    def generate_response(self, user_message):
        """Generate AI response based on user message"""
        try:
            user_lower = user_message.lower().strip()

            if not user_message or len(user_message.strip()) == 0:
                return "Please type a question about PC components!"

            # First, check training data for exact same query
            previous_response = self.check_previous_training(user_message)
            if previous_response:
                return previous_response

            # Greeting
            if any(word in user_lower for word in ['hi', 'hello', 'hey']):
                response = """Hello! I'm your PC Expert AI. Ask me about:

Specifications:
Compatibility:
Full Details:
"""
                self.save_training_example(user_message, response)
                return response

            # Help
            if 'help' in user_lower:
                response = """Ask me questions like:

Specifications
Compatibility
Full Details
"""
                self.save_training_example(user_message, response)
                return response

            # Compatibility questions
            compatibility_patterns = [
                (r'is (.+) compatible with (.+)\?', 2),
                (r'will (.+) work with (.+)\?', 2),
                (r'can (.+) use with (.+)\?', 2),
                (r'does (.+) fit (.+)\?', 2),
                (r'compatibility of (.+) and (.+)', 2),
                (r'compatible (.+) (.+)', 2),
                (r'(.+) and (.+) compatible', 2),
                (r'(.+) with (.+) compatibility', 2)
            ]

            for pattern, num_components in compatibility_patterns:
                match = re.search(pattern, user_lower)
                if match:
                    if num_components == 2:
                        comp1 = match.group(1).strip()
                        comp2 = match.group(2).strip()
                        response = self.check_compatibility(comp1, comp2)
                        self.save_training_example(user_message, response)
                        return response

            # Find component
            component, confidence = self.find_component(user_message)

            if component and confidence > 0.3:
                # Generate EXACT VALUE response based on what user asked
                response = self.generate_exact_value_response(
                    user_message, component)

                # Save to training data
                self.save_training_example(user_message, response)
                return response

            elif component and confidence > 0.2:
                response = self.generate_exact_value_response(
                    user_message, component)
                self.save_training_example(user_message, response)
                return response

            # Default response
            response = """Ask me questions like:

Specifications:
Compatibility:
Full Details
"""
            self.save_training_example(user_message, response)
            return response

        except Exception as e:
            return f"Sorry, I encountered an error. Please try again with a different question."


def main():
    chatbot = PCChatbot()

    print("\n" + "=" * 60)
    print("PC EXPERT AI CHATBOT")
    print("Type 'quit' to exit")
    print("=" * 60)

    while True:
        user_input = input("\nYou: ").strip()

        if user_input.lower() in ['quit', 'exit', 'bye']:
            print("Goodbye! Your questions are saved!")
            break

        if user_input:
            response = chatbot.generate_response(user_input)
            print(f"AI: {response}")


if __name__ == "__main__":
    main()
