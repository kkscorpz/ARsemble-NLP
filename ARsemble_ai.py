import json
import re
import torch
from sentence_transformers import SentenceTransformer, util
import os
import sys

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))


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
        """Load COMPLETE PC components database - FIXED DUPLICATES"""
        components = {
            # ==========================
            # ========== GPUs ==========
            # ==========================
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
            "rtx 3050": {
                "name": "Gigabyte RTX 3050 EAGLE OC", "type": "GPU",
                "vram": "8GB GDDR6", "clock": "~1777 MHz (Boost)", "power": "~130 Watts",
                "slot": "PCIe 4.0 x16", "price": "₱12,000",
                "compatibility": "Requires a motherboard with an available PCIe x16 slot (compatible with PCIe 3.0/4.0/5.0). Needs a PSU with sufficient wattage (450W-550W recommended total system power) and at least one 8-pin PCIe power connector. Ensure your case has enough physical clearance."
            },
            "rtx 4060": {
                "name": "MSI RTX 4060 GAMING X", "type": "GPU",
                "vram": "8GB GDDR6", "clock": "~2595 MHz (Boost)", "power": "~115 Watts",
                "slot": "PCIe 4.0 x8", "price": "₱18,000",
                "compatibility": "Requires a motherboard with an available PCIe x16 slot. Needs a 550W+ PSU with one 8-pin PCIe power connector. Compatible with modern cases."
            },
            "rx 9060 xt 8gb": {
                "name": "Gigabyte RX 9060 XT Gaming OC", "type": "GPU",
                "vram": "8GB GDDR6", "clock": "~2200 MHz (Boost)", "power": "~180 Watts",
                "slot": "PCIe 4.0 x16", "price": "₱26,000",
                "compatibility": "Requires PCIe x16 slot. Recommended 600W PSU with 2x 8-pin PCIe connectors. Ensure your case supports full-length GPUs."
            },
            "gtx 750 ti": {
                "name": "NVIDIA GTX 750 Ti", "type": "GPU",
                "vram": "4GB GDDR5", "clock": "~1085 MHz (Boost)", "power": "~60 Watts",
                "slot": "PCIe 3.0 x16", "price": "₱4,000",
                "compatibility": "Very low power draw (300W PSU recommended). Single 6-pin PCIe power connector or none depending on model. Fits in most cases due to compact size."
            },
            "rtx 3060": {
                "name": "MSI RTX 3060", "type": "GPU",
                "vram": "12GB GDDR6", "clock": "~1777 MHz (Boost)", "power": "~170 Watts",
                "slot": "PCIe 4.0 x16", "price": "₱16,000",
                "compatibility": "Needs PCIe x16 slot and 550W+ PSU. Requires 1x 8-pin PCIe power connector. Ensure case has enough clearance."
            },
            "rx 9060 xt 16gb": {
                "name": "Sapphire RX 9060 XT", "type": "GPU",
                "vram": "16GB GDDR6", "clock": "~2400 MHz (Boost)", "power": "~220 Watts",
                "slot": "PCIe 4.0 x16", "price": "₱32,000",
                "compatibility": "Requires PCIe x16 slot, 650W+ PSU with 2x 8-pin PCIe connectors. Ensure case supports large GPUs with proper cooling."
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

            # ==========================
            # ========== PSUs ==========
            # ==========================
            "corsair rm850x": {
                "name": "Corsair RM850x", "type": "PSU", "price": "₱8,000",
                "wattage": "850W", "efficiency": "80 Plus Gold", "modular": "Fully Modular",
                "compatibility": "Great for high-performance gaming PCs (RTX 30/40, RX 6000/7000)."
            },
            "cooler master mwe white 750w": {
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
            # ========== Case Fans ========== hindi na kasama sa data
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
            }
        }
        return components

    def find_component(self, query):
        """Find the most relevant component using SMART matching"""
        query_lower = query.lower().strip()

        # STRATEGY 1: EXACT NAME MATCH
        for comp_key, component in self.components_db.items():
            if query_lower == component['name'].lower():
                return component, 1.0

        # STRATEGY 2: KEYWORD MATCHING FOR COMMON COMPONENTS - FIXED MAPPINGS
        keyword_mapping = {
            # GPU - SORTED BY LENGTH (longest/most specific first)
            "integrated graphics": "integrated graphics",
            "integrated gpu": "integrated graphics",
            "igpu": "integrated graphics",
            "onboard graphics": "integrated graphics",
            "geforce rtx 3050": "rtx 3050",
            "geforce rtx 4060": "rtx 4060",
            "geforce rtx 3060": "rtx 3060",
            "geforce gtx 750 ti": "gtx 750 ti",
            "radeon rx 9060 xt": "rx 9060 xt 8gb",
            "radeon rx 9060": "rx 9060 xt 8gb",
            "rtx 3050": "rtx 3050",
            "rtx 4060": "rtx 4060",
            "rtx 3060": "rtx 3060",
            "rx 9060 xt": "rx 9060 xt 8gb",
            "gtx 750 ti": "gtx 750 ti",
            "3050": "rtx 3050",
            "4060": "rtx 4060",
            "3060": "rtx 3060",
            "rx 9060": "rx 9060 xt 8gb",
            "750 ti": "gtx 750 ti",

            # CPU mappings - Intel (MOST SPECIFIC FIRST)
            "intel-core i9-14900k": "intel core i9-14900k",
            "intel-core i7-14700k": "intel core i7-14700k",
            "intel-core i7-13700k": "intel core i7-13700k",
            "intel-core i5-14600k": "intel core i5-14600k",
            "intel-core i5-14500": "intel core i5-14500",
            "intel-core i5-13400": "intel core i5-13400",
            "intel-core i3-14100": "intel core i3-14100",
            "intel-core i3-13100": "intel core i3-13100",
            "i9-14900k": "intel core i9-14900k",
            "i7-14700k": "intel core i7-14700k",
            "i7-13700k": "intel core i7-13700k",
            "i5-14600k": "intel core i5-14600k",
            "i5-14500": "intel core i5-14500",
            "i5-13400": "intel core i5-13400",
            "i3-14100": "intel core i3-14100",
            "i3-13100": "intel core i3-13100",
            "14900k": "intel core i9-14900k",
            "14700k": "intel core i7-14700k",
            "13700k": "intel core i7-13700k",
            "14600k": "intel core i5-14600k",
            "14500": "intel core i5-14500",
            "13400": "intel core i5-13400",
            "14100": "intel core i3-14100",
            "13100": "intel core i3-13100",

            # CPU mappings - AMD (MOST SPECIFIC FIRST)
            "amd ryzen 9 7950x": "amd ryzen 9 7950x",
            "amd ryzen 9 9900x": "amd ryzen 9 9900x",
            "amd ryzen 9 9900x3d": "amd ryzen 9 9900x3d",
            "amd ryzen 7 7700x": "amd ryzen 7 7700x",
            "amd ryzen 7 5700x": "amd ryzen 7 5700x",
            "amd ryzen 5 5600x": "amd ryzen 5 5600x",
            "amd ryzen 5 5600g": "amd ryzen 5 5600g",
            "amd ryzen 3 3200g": "amd ryzen 3 3200g",
            "ryzen 9 7950x": "amd ryzen 9 7950x",
            "ryzen 9 9900x": "amd ryzen 9 9900x",
            "ryzen 9 9900x3d": "amd ryzen 9 9900x3d",
            "ryzen 7 7700x": "amd ryzen 7 7700x",
            "ryzen 7 5700x": "amd ryzen 7 5700x",
            "ryzen 5 5600x": "amd ryzen 5 5600x",
            "ryzen 5 5600g": "amd ryzen 5 5600g",
            "ryzen 3 3200g": "amd ryzen 3 3200g",
            "7950x": "amd ryzen 9 7950x",
            "9900x": "amd ryzen 9 9900x",
            "9900x3d": "amd ryzen 9 9900x3d",
            "7700x": "amd ryzen 7 7700x",
            "5700x": "amd ryzen 7 5700x",
            "5600x": "amd ryzen 5 5600x",
            "5600g": "amd ryzen 5 5600g",
            "3200g": "amd ryzen 3 3200g",

            # Motherboard mappings
            "asus prime b550m-k": "asus prime b550m-k",
            "msi b450m a pro max ii": "msi b450m a pro max ii",
            "msi pro h610m s ddr4": "msi pro h610m s ddr4",
            "ramsta rs-b450mp": "ramsta rs-b450mp",
            "ramsta rs-h311d4": "ramsta rs-h311d4",
            "msi b650m gaming plus wifi": "msi b650m gaming plus wifi",
            "msi b760m gaming plus wifi ddr4": "msi b760m gaming plus wifi ddr4",
            "gigabyte h610m k ddr4": "gigabyte h610m k ddr4",
            "asus prime b550m": "asus prime b550m-k",
            "msi b450m": "msi b450m a pro max ii",
            "msi h610m": "msi pro h610m s ddr4",
            "ramsta b450": "ramsta rs-b450mp",
            "ramsta h311": "ramsta rs-h311d4",
            "msi b650m": "msi b650m gaming plus wifi",
            "msi b760m": "msi b760m gaming plus wifi ddr4",
            "gigabyte h610m": "gigabyte h610m k ddr4",
            "b550m": "asus prime b550m-k",
            "b450m": "msi b450m a pro max ii",
            "h610m": "msi pro h610m s ddr4",
            "b650m": "msi b650m gaming plus wifi",
            "b760m": "msi b760m gaming plus wifi ddr4",

            # RAM mappings
            "kingston fury beast ddr4": "kingston fury beast ddr4",
            "kingston hyperx fury ddr3": "kingston hyperx fury ddr3",
            "hkc pc ddr4-3200 dimm": "hkc pc ddr4-3200 dimm",
            "hkcmemory hu40 ddr4 (16gb)": "hkcmemory hu40 ddr4 (16gb)",
            "hkcmemory hu40 ddr4 (8gb)": "hkcmemory hu40 ddr4 (8gb)",
            "kingston fury beast": "kingston fury beast ddr4",
            "kingston hyperx fury": "kingston hyperx fury ddr3",
            "fury beast": "kingston fury beast ddr4",
            "hyperx fury": "kingston hyperx fury ddr3",
            "hkc ddr4": "hkc pc ddr4-3200 dimm",
            "hkc memory": "hkcmemory hu40 ddr4 (16gb)",

            # Storage mappings
            "seagate barracuda 1tb": "seagate barracuda 1tb",
            "western digital blue 2tb": "western digital blue 2tb",
            "samsung 970 evo plus 1tb": "samsung 970 evo plus 1tb",
            "crucial mx500 500gb": "crucial mx500 500gb",
            "seagate 1tb": "seagate barracuda 1tb",
            "wd blue 2tb": "western digital blue 2tb",
            "samsung 970 evo": "samsung 970 evo plus 1tb",
            "crucial mx500": "crucial mx500 500gb",

            # PSU mappings
            "corsair rm850x": "corsair rm850x",
            "cooler master mwe white 750w": "cooler master mwe white 750w",
            "corsair cx650": "corsair cx650",
            "cougar gx-f 750w": "cougar gx-f 750w",
            "seasonic focus plus gold 550w": "seasonic focus plus gold 550w",
            "rm850x": "corsair rm850x",
            "cooler master 750w": "cooler master mwe white 750w",
            "cx650": "corsair cx650",
            "cougar 750w": "cougar gx-f 750w",
            "seasonic 550w": "seasonic focus plus gold 550w",

            # Case Fan mappings
            "coolmoon yx120": "coolmoon yx120",
            "cooler master sickleflow 120 argb": "cooler master sickleflow 120 argb",
            "arctic p12 pwm pst": "arctic p12 pwm pst",
            "coolmoon fan": "coolmoon yx120",
            "cooler master sickleflow": "cooler master sickleflow 120 argb",
            "arctic p12": "arctic p12 pwm pst",

            # CPU Cooler mappings
            "coolmoon aosor s400": "coolmoon aosor s400",
            "cooler master hyper 212 black edition": "cooler master hyper 212 black edition",
            "thermalright peerless assassin 120 se": "thermalright peerless assassin 120 se",
            "deepcool le500 marrs": "deepcool le500 marrs",
            "coolmoon cooler": "coolmoon aosor s400",
            "hyper 212": "cooler master hyper 212 black edition",
            "peerless assassin": "thermalright peerless assassin 120 se",
            "deepcool le500": "deepcool le500 marrs"
        }

        # Sort by length (longest first for most specific matches)
        sorted_keywords = sorted(keyword_mapping.keys(), key=len, reverse=True)

        for keyword in sorted_keywords:
            if keyword in query_lower:
                component_key = keyword_mapping[keyword]
                if component_key in self.components_db:
                    component = self.components_db[component_key]
                    return component, 0.9

        # STRATEGY 3: PARTIAL NAME MATCH (fallback)
        for comp_key, component in self.components_db.items():
            component_name_lower = component['name'].lower()
            # Check if ALL important words from component name are in query
            important_words = [
                word for word in component_name_lower.split() if len(word) > 2]
            if important_words and all(word in query_lower for word in important_words):
                print(f" PARTIAL MATCH: {component['name']}")
                return component, 0.7

        # STRATEGY 4: SEMANTIC SEARCH FALLBACK (AI-powered)
        if self.model and self.embeddings is not None:
            try:
                query_embedding = self.model.encode(
                    query, convert_to_tensor=True)
                similarities = util.cos_sim(
                    query_embedding, self.embeddings)[0]

                best_match_idx = torch.argmax(similarities).item()
                best_score = similarities[best_match_idx].item()

                if best_score > 0.3:
                    component_key = self.component_names[best_match_idx]
                    component = self.components_db[component_key]
                    return component, best_score

            except Exception as e:
                print(f"Semantic search error: {e}")

        return None, 0.0

    def check_compatibility(self, component1_name, component2_name):
        """Check compatibility between two components and explain why"""
        comp1, score1 = self.find_component(component1_name)
        comp2, score2 = self.find_component(component2_name)

        if not comp1 or not comp2:
            return f"I couldn't find one or both components. Please check the names."

        comp1_type = comp1['type']
        comp2_type = comp2['type']

        # CPU-Motherboard Compatibility (FIXED)
        if (comp1_type == 'CPU' and comp2_type == 'Motherboard') or (comp1_type == 'Motherboard' and comp2_type == 'CPU'):
            cpu = comp1 if comp1_type == 'CPU' else comp2
            mobo = comp2 if comp2_type == 'Motherboard' else comp1

            cpu_socket = cpu.get('socket', '').strip()
            mobo_socket = mobo.get('socket', '').strip()

            if cpu_socket and mobo_socket:
                if cpu_socket == mobo_socket:
                    return f"✅ COMPATIBLE\n{cpu['name']} fits {mobo['name']}\n\nWhy: Same socket type ({cpu_socket}) means physical and electrical compatibility."
                else:
                    return f"❌ NOT COMPATIBLE\n{cpu['name']} doesn't fit {mobo['name']}\n\nWhy: Different socket types ({cpu_socket} vs {mobo_socket}) - physically incompatible."
            else:
                return f"❓ CANNOT DETERMINE\nMissing socket information for compatibility check."

        # Motherboard-RAM Compatibility (FIXED)
        elif (comp1_type == 'Motherboard' and comp2_type == 'RAM') or (comp1_type == 'RAM' and comp2_type == 'Motherboard'):
            mobo = comp1 if comp1_type == 'Motherboard' else comp2
            ram = comp2 if comp2_type == 'RAM' else comp1

            mobo_ram_type = mobo.get('ram', '').upper()
            ram_type = ram.get('memory_type', '').upper()

            if ram_type and mobo_ram_type:
                if ram_type in mobo_ram_type:
                    return f"✅ COMPATIBLE\n{ram['name']} works with {mobo['name']}\n\nWhy: RAM type ({ram_type}) matches motherboard support ({mobo_ram_type})."
                else:
                    return f"❌ NOT COMPATIBLE\n{ram['name']} doesn't work with {mobo['name']}\n\nWhy: Different RAM generations ({ram_type} vs {mobo_ram_type}) - physically incompatible."
            else:
                return f"❓ CANNOT DETERMINE\nMissing RAM type information."

        # PSU-GPU Compatibility (Power) - IMPROVED
        elif (comp1_type == 'PSU' and comp2_type == 'GPU') or (comp1_type == 'GPU' and comp2_type == 'PSU'):
            psu = comp1 if comp1_type == 'PSU' else comp2
            gpu = comp2 if comp2_type == 'GPU' else comp1

            # Extract wattage numbers more reliably
            psu_wattage_match = re.findall(r'\d+', psu.get('wattage', '0W'))
            psu_wattage = int(psu_wattage_match[0]) if psu_wattage_match else 0

            gpu_power_match = re.findall(r'\d+', gpu.get('power', '0W'))
            gpu_power = int(gpu_power_match[0]) if gpu_power_match else 0

            if psu_wattage == 0 or gpu_power == 0:
                return f"❓ CANNOT DETERMINE\nMissing power information for {gpu['name']} or {psu['name']}."

            if psu_wattage >= gpu_power + 200:
                return f"✅ COMPATIBLE\n{psu['name']} can easily power {gpu['name']}\n\nWhy: PSU has sufficient wattage ({psu_wattage}W) for GPU ({gpu_power}W) with good safety margin."
            elif psu_wattage >= gpu_power + 100:
                return f"⚠️ BORDERLINE COMPATIBLE\n{psu['name']} should work with {gpu['name']}\n\nWhy: PSU wattage ({psu_wattage}W) is adequate for GPU ({gpu_power}W) but consider higher wattage for future upgrades."
            else:
                return f"❌ NOT COMPATIBLE\n{psu['name']} is too weak for {gpu['name']}\n\nWhy: PSU ({psu_wattage}W) doesn't have enough power for GPU ({gpu_power}W). Minimum recommended: {gpu_power + 150}W."

        # PSU-CPU Compatibility - IMPROVED
        elif (comp1_type == 'PSU' and comp2_type == 'CPU') or (comp1_type == 'CPU' and comp2_type == 'PSU'):
            psu = comp1 if comp1_type == 'PSU' else comp2
            cpu = comp2 if comp2_type == 'CPU' else comp1

            psu_wattage_match = re.findall(r'\d+', psu.get('wattage', '0W'))
            psu_wattage = int(psu_wattage_match[0]) if psu_wattage_match else 0

            cpu_tdp_match = re.findall(r'\d+', cpu.get('tdp', '0W'))
            cpu_tdp = int(cpu_tdp_match[0]) if cpu_tdp_match else 0

            if psu_wattage == 0 or cpu_tdp == 0:
                return f"❓ CANNOT DETERMINE\nMissing power information for {cpu['name']} or {psu['name']}."

            if psu_wattage >= cpu_tdp + 400:
                return f"✅ COMPATIBLE\n{psu['name']} is excellent for {cpu['name']}\n\nWhy: PSU has plenty of power ({psu_wattage}W) for CPU ({cpu_tdp}W) and additional components."
            elif psu_wattage >= cpu_tdp + 200:
                return f"⚠️ ADEQUATE\n{psu['name']} is sufficient for {cpu['name']}\n\nWhy: PSU wattage ({psu_wattage}W) works for CPU ({cpu_tdp}W) but consider total system power including GPU."
            else:
                return f"❌ NOT RECOMMENDED\n{psu['name']} is too weak for {cpu['name']} with dedicated GPU\n\nWhy: PSU ({psu_wattage}W) doesn't leave enough power for other components."

        # CPU-GPU Compatibility (General)
        elif (comp1_type == 'CPU' and comp2_type == 'GPU') or (comp1_type == 'GPU' and comp2_type == 'CPU'):
            cpu = comp1 if comp1_type == 'CPU' else comp2
            gpu = comp2 if comp2_type == 'GPU' else comp1
            return f"✅ COMPATIBLE\n{cpu['name']} and {gpu['name']} work together\n\nWhy: All modern CPUs and GPUs are compatible via PCIe slots."

        # Motherboard-Storage Compatibility - IMPROVED
        elif (comp1_type == 'Motherboard' and comp2_type == 'Storage') or (comp1_type == 'Storage' and comp2_type == 'Motherboard'):
            mobo = comp1 if comp1_type == 'Motherboard' else comp2
            storage = comp2 if comp2_type == 'Storage' else comp1

            storage_interface = storage.get('interface', '').upper()

            if 'M.2' in storage_interface or 'NVMe' in storage_interface:
                return f"✅ COMPATIBLE\n{storage['name']} works with {mobo['name']}\n\nWhy: NVMe SSDs use standard M.2 slots available on modern motherboards."
            elif 'SATA' in storage_interface:
                return f"✅ COMPATIBLE\n{storage['name']} works with {mobo['name']}\n\nWhy: SATA is universal standard for storage devices."

        # Case Fan compatibility (works with any motherboard)
        elif (comp1_type == 'Case Fan' and comp2_type == 'Motherboard') or (comp1_type == 'Motherboard' and comp2_type == 'Case Fan'):
            fan = comp1 if comp1_type == 'Case Fan' else comp2
            mobo = comp2 if comp2_type == 'Motherboard' else comp1
            return f"✅ COMPATIBLE\n{fan['name']} works with {mobo['name']}\n\nWhy: Case fans use standard motherboard fan headers."

        # CPU Cooler compatibility (check sockets) - FIXED
        elif (comp1_type == 'CPU Cooler' and comp2_type == 'CPU') or (comp1_type == 'CPU' and comp2_type == 'CPU Cooler'):
            cooler = comp1 if comp1_type == 'CPU Cooler' else comp2
            cpu = comp2 if comp2_type == 'CPU' else comp1

            cpu_socket = cpu.get('socket', '').strip()
            cooler_sockets = cooler.get('sockets', '')

            if cpu_socket and cooler_sockets:
                if cpu_socket in cooler_sockets:
                    return f"✅ COMPATIBLE\n{cooler['name']} works with {cpu['name']}\n\nWhy: Cooler supports {cpu_socket} socket."
                else:
                    return f"❌ NOT COMPATIBLE\n{cooler['name']} doesn't work with {cpu['name']}\n\nWhy: Cooler doesn't support {cpu_socket} socket."
            else:
                return f"❓ CANNOT DETERMINE\nMissing socket information for compatibility check."

        # General compatibility for same type components
        elif comp1_type == comp2_type:
            return f"❌ NOT COMPATIBLE\n{comp1['name']} and {comp2['name']} are both {comp1_type}s\n\nWhy: You can't use two {comp1_type}s of the same type together."

        # Default - assume compatible for other combinations
        return f"✅ LIKELY COMPATIBLE\n{comp1['name']} and {comp2['name']} should work together\n\nWhy: Standard PC components are generally compatible."

    def calculate_psu_wattage(self, cpu_model, gpu_model, other_components=None):
        """Calculate recommended PSU wattage based on components"""

        # Find Components
        cpu, cpu_score = self.find_component(cpu_model)
        gpu, gpu_score = self.find_component(gpu_model)

        if not cpu or not gpu:
            return "I couldn't find one or both components. Please check the names."

        # Extract power consumption
        cpu_power = 0
        gpu_power = 0

        # Extract CPU power from TDP
        cpu_tdp_match = re.findall(r'\d+', cpu.get('tdp', '0W'))
        if cpu_tdp_match:
            cpu_power = int(cpu_tdp_match[0])

        gpu_power_match = re.findall(r'\d+', gpu.get('power', '0W'))
        if gpu_power_match:
            gpu_power = int(gpu_power_match[0])

        # Base power for other components
        base_power = 100  # Motherboard, RAM, storage, fans

        # Calculate total power consumption
        total_power = cpu_power + gpu_power + base_power

        # Calculate recommended PSU with safety margin
        safety_margin = total_power * 0.3  # 30% safety margin
        recommended_psu = total_power + safety_margin

        # Round up to nearest standard PSU wattage
        standard_wattages = [450, 550, 650, 750, 850, 1000]
        final_recommendation = min(
            [w for w in standard_wattages if w >= recommended_psu], default=850)

        response = f"""⚡ PSU Wattage Calculation for {cpu['name']} + {gpu['name']}:
        
        📊 Power Breakdown:
• CPU ({cpu['name']}): {cpu_power}W
• GPU ({gpu['name']}): {gpu_power}W  
• Other components (mobo, RAM, storage, fans): ~100W
• Total estimated power: {total_power}W

💡 Recommended PSU:
• Minimum: {total_power + 100}W
• Recommended: {final_recommendation}W (with 30% safety margin)

🎯 Why {final_recommendation}W?
• Provides headroom for peak power spikes
• Allows for future upgrades
• More efficient operation (PSUs run best at 50-80% load)
• Choose 80+ Bronze, Gold, or better for reliability

🔧 Tip: Always choose quality PSU brands like Corsair, Seasonic, Cooler Master, etc."""

        return response

    def generate_exact_value_response(self, user_message, component):
        """Generate EXACT VALUE ONLY based on what user asked - FIXED LOGIC ORDER"""
        user_lower = user_message.lower()

        # FULL DETAILS REQUEST - Highest priority
        if any(word in user_lower for word in ['details', 'specs', 'specifications', 'full', 'everything', 'all', 'specification, spec']):
            response = f"{component['name']} ({component['type']})\n\n"

            # Add all available fields
            for key, value in component.items():
                if key not in ['name', 'type']:
                    response += f"{key.title()}: {value}\n"
            return response

        # COMPONENT TYPE REQUEST - High priority
        if any(word in user_lower for word in ['what type', 'component type', 'type of']):
            return f"{component['type']}"

        # SPECIFIC ATTRIBUTE QUESTIONS - Grouped by priority

        # 1. POWER RELATED (TDP, Wattage, Power) - HIGH PRIORITY
        if any(word in user_lower for word in ['tdp']):
            if 'tdp' in component:
                return f"{component['tdp']}"

        if any(word in user_lower for word in ['wattage', 'watts', 'power']):
            if 'power' in component:
                return f"{component['power']}"
            elif 'wattage' in component:
                return f"{component['wattage']}"
            elif 'tdp' in component:
                return f"{component['tdp']}"

        # 2. RAM SPECIFIC ATTRIBUTES
        if any(word in user_lower for word in ['capacity']):
            if 'capacity' in component:
                return f"{component['capacity']}"

        if any(word in user_lower for word in ['speed']):
            if 'speed' in component:
                return f"{component['speed']}"

        if any(word in user_lower for word in ['memory type', 'memory']):
            if 'memory_type' in component:
                return f"{component['memory_type']}"

        # 3. MOTHERBOARD SPECIFIC ATTRIBUTES
        if any(word in user_lower for word in ['chipset']):
            if 'chipset' in component:
                return f"{component['chipset']}"

        if any(word in user_lower for word in ['socket']):
            if 'socket' in component:
                return f"{component['socket']}"

        if any(word in user_lower for word in ['form', 'form factor', 'size', 'atx', 'micro-atx', 'mini-itx']):
            if 'form' in component:
                return f"{component['form']}"

        if any(word in user_lower for word in ['ram', 'memory support']):
            if 'ram' in component:
                return f"{component['ram']}"

        # 4. STORAGE SPECIFIC ATTRIBUTES
        if any(word in user_lower for word in ['storage', 'sata', 'm.2', 'nvme']):
            if component['type'] == 'Motherboard':
                return "This motherboard has multiple SATA ports and M.2 slots for storage devices"
            elif 'capacity' in component:
                return f"{component['capacity']}"
            elif 'interface' in component:
                return f"{component['interface']}"

        if any(word in user_lower for word in ['interface']):
            if 'interface' in component:
                return f"{component['interface']}"

        # 5. GPU SPECIFIC ATTRIBUTES
        if any(word in user_lower for word in ['vram', 'video memory', 'graphics memory']):
            if 'vram' in component:
                return f"{component['vram']}"

        if any(word in user_lower for word in ['clock', 'speed', 'frequency', 'boost', 'ghz', 'mhz']):
            if 'clock' in component:
                return f"{component['clock']}"
            elif 'speed' in component:
                return f"{component['speed']}"

        # 6. CPU SPECIFIC ATTRIBUTES
        if any(word in user_lower for word in ['cores', 'threads', 'core count', 'core']):
            if 'cores' in component:
                return f"{component['cores']}"

        # 7. PSU SPECIFIC ATTRIBUTES
        if any(word in user_lower for word in ['efficiency', '80 plus', 'gold', 'bronze']):
            if 'efficiency' in component:
                return f"{component['efficiency']}"

        if any(word in user_lower for word in ['modular', 'cable management']):
            if 'modular' in component:
                return f"{component['modular']}"

        # 8. COOLERS & FANS SPECIFIC ATTRIBUTES
        if any(word in user_lower for word in ['cooler type', 'cooling type']):
            if 'cooler_type' in component:
                return f"{component['cooler_type']}"

        if any(word in user_lower for word in ['fan size', 'size']):
            if 'fan_size' in component:
                return f"{component['fan_size']}"
            elif 'size' in component:
                return f"{component['size']}"

        if any(word in user_lower for word in ['rpm', 'rotation']):
            if 'rpm' in component:
                return f"{component['rpm']}"

        if any(word in user_lower for word in ['airflow', 'cfm']):
            if 'airflow' in component:
                return f"{component['airflow']}"

        if any(word in user_lower for word in ['noise', 'dba', 'sound']):
            if 'noise' in component:
                return f"{component['noise']}"

        # 9. PRICE - Check before default
        if any(word in user_lower for word in ['price', 'cost', 'how much', 'magkano', 'presyo']):
            if 'price' in component:
                return f"{component['price']}"

        # 10. COMPATIBILITY
        if any(word in user_lower for word in ['compatibility', 'compatible', 'works with']):
            if 'compatibility' in component:
                return f"{component['compatibility']}"

        # DEFAULT: Return component name if no specific attribute found
        return f"{component['name']}"

    # get_build_recommendation

    def get_build_recommendation(self, build_type, budget_range=None):
        """Return PC build recommendations USING ONLY EXISTING COMPONENTS"""
        if not build_type or build_type not in ['budget', 'entry', 'mid', 'high']:
            return None

        build_presets = {
            "budget": {
                "name": "💸 Ultra Budget PC",
                "budget": "₱15,000 - ₱20,000",
                "target": "Basic Computing, School, Office Work",
                "description": "Most affordable build for essential computing",
                "components": {
                    "CPU": "AMD Ryzen 3 3200G",  # FROM YOUR DATA
                    "GPU": "Integrated Graphics (from CPU)",
                    "Motherboard": "RAMSTA RS-B450MP",  # FROM YOUR DATA
                    "RAM": "HKCMEMORY HU40 DDR4 (8GB)",  # FROM YOUR DATA
                    "Storage": "Crucial MX500 500GB",  # FROM YOUR DATA
                    "PSU": "Seasonic Focus Plus Gold 550W",  # FROM YOUR DATA
                    "Case Fan": "COOLMOON YX120"  # FROM YOUR DATA
                },
                "performance": "• Web Browsing: Smooth\n• Office Apps: Fast\n• Light Gaming: Basic esports games\n• Video Streaming: 1080p",
                "upgrade_path": "Add more RAM or upgrade CPU later"
            },

            "entry": {
                "name": "🎮 Entry Level Gaming PC",
                "budget": "₱25,000 - ₱35,000",
                "target": "1080p Gaming, Esports, School/Work",
                "description": "Perfect for beginners and budget gaming",
                "components": {
                    "CPU": "AMD Ryzen 5 5600G",  # FROM YOUR DATA
                    "GPU": "Integrated Graphics (from CPU)",
                    "Motherboard": "ASUS PRIME B550M-K",  # FROM YOUR DATA
                    # FROM YOUR DATA (8GB or 16GB)
                    "RAM": "Kingston FURY Beast DDR4",
                    "Storage": "Crucial MX500 500GB",  # FROM YOUR DATA
                    "PSU": "Seasonic Focus Plus Gold 550W",  # FROM YOUR DATA
                    "Case Fan": "COOLMOON YX120"  # FROM YOUR DATA
                },
                "performance": "• Valorant: 100+ FPS\n• Dota 2: 80+ FPS\n• GTA V: 60 FPS (Medium)\n• Perfect for school/work",
                "upgrade_path": "Add GPU like GTX 750 Ti or RTX 3050 later"
            },

            "mid": {
                "name": "⚡ Mid-Range Gaming PC",
                "budget": "₱45,000 - ₱60,000",
                "target": "1440p Gaming, Streaming, Content Creation",
                "description": "Great balance of performance and value",
                "components": {
                    "CPU": "Intel Core i5-14600K",  # FROM YOUR DATA
                    "GPU": "MSI RTX 4060 GAMING X",  # FROM YOUR DATA
                    "Motherboard": "MSI B760M Gaming Plus WiFi DDR4",  # FROM YOUR DATA
                    "RAM": "HKCMEMORY HU40 DDR4 (16GB)",  # FROM YOUR DATA
                    "Storage": "Samsung 970 EVO Plus 1TB",  # FROM YOUR DATA
                    "PSU": "Corsair CX650",  # FROM YOUR DATA
                    "CPU Cooler": "Cooler Master Hyper 212 Black Edition",  # FROM YOUR DATA
                    "Case Fan": "Cooler Master SickleFlow 120 ARGB"  # FROM YOUR DATA
                },
                "performance": "• Cyberpunk 2077: 60+ FPS (High)\n• Streaming: Smooth 1080p60\n• AAA Games: High settings 1440p\n• Video Editing: Fast rendering",
                "upgrade_path": "Add more storage or better cooling"
            },

            "high": {
                "name": "🔥 High-End Gaming PC",
                "budget": "₱70,000 - ₱100,000+",
                "target": "4K Gaming, Professional Work, Streaming",
                "description": "Premium performance for enthusiasts",
                "components": {
                    "CPU": "Intel Core i7-14700K",  # FROM YOUR DATA
                    "GPU": "Sapphire RX 9060 XT 16GB",  # FROM YOUR DATA
                    "Motherboard": "MSI B760M Gaming Plus WiFi DDR4",  # FROM YOUR DATA
                    # FROM YOUR DATA (32GB total)
                    "RAM": "HKCMEMORY HU40 DDR4 (16GB) x2",
                    "Storage": "Samsung 970 EVO Plus 1TB + Western Digital Blue 2TB",  # FROM YOUR DATA
                    "PSU": "Corsair RM850x",  # FROM YOUR DATA
                    "CPU Cooler": "Deepcool LE500 MARRS",  # FROM YOUR DATA
                    "Case Fan": "Arctic P12 PWM PST"  # FROM YOUR DATA
                },
                "performance": "• 4K Gaming: 60+ FPS Ultra\n• Streaming: 4K capable\n• 3D Rendering: Professional grade\n• VR Ready: Excellent performance",
                "upgrade_path": "Top-tier components as needed"
            }
        }
        return build_presets.get(build_type.lower())

    # suggest_build_type

    def suggest_build_type(self, user_message):
        """Auto-detect what build type user wants"""
        user_lower = user_message.lower()

        build_trigger_words = [
            'build', 'pc build', 'recommend', 'suggest', 'setup', 'rig', 'system', 'pc']
        if not any(keyword in user_lower for keyword in build_trigger_words):
            return None

         # BUDGET
        if any(word in user_lower for word in ['15', '15k', '15,000', '15000', '16', '17', '18', '19']):
            return "budget"
        elif any(word in user_lower for word in ['20', '25', '30', '35', '20k', '25k', '30k', '35k', '20,000', '25,000', '30,000', '35,000']):
            return "entry"
        elif any(word in user_lower for word in ['45', '50', '55', '60', '45k', '50k', '60k', '45,000', '50,000', '55,000', '60,000']):
            return "mid"
        elif any(word in user_lower for word in ['70', '80', '90', '100', '70k', '80k', '100k', '70,000', '80,000', '90,000', '100,000']):
            return "high"

        build_keywords_mapping = {
            "budget": ['ultra budget', 'very cheap', 'minimum', 'basic computing', 'office pc', 'budget', 'cheap', 'low cost', 'economy', 'affordable', 'basic'],
            "entry": ['entry', 'starter', 'beginner', 'gaming'],
            "mid": ['mid', 'medium', 'mid-range', 'balanced', 'all-rounder', 'mainstream', 'standard'],
            "high": ['high', 'premium', 'high-end', 'best', 'pro', 'enthusiast', 'streaming', '4k']
        }

        build_scores = {}
        for build_type, keywords in build_keywords_mapping.items():
            score = sum(1 for keyword in keywords if keyword in user_lower)
            if score > 0:
                build_scores[build_type] = score

        if build_scores:
            return max(build_scores.items(), key=lambda x: x[1])[0]

        return None

    # verify_build_compatibility
    def verify_build_compatibility(self, build_type):
        """Verify that recommended build components are compatible"""
        build = self.get_build_recommendation(build_type)
        if not build:
            return "Build not found"

        issues = []
        components = build['components']

        cpu = components.get('CPU')
        motherboard = components.get('Motherboard')
        if cpu and motherboard:
            cpu_info, _ = self.find_component(cpu)
            mobo_info, _ = self.find_component(motherboard)
            if cpu_info and mobo_info:
                if cpu_info.get('socket') != mobo_info.get('socket'):
                    issues.append(
                        f"❌ CPU {cpu_info['socket']} not compatible with motherboard {mobo_info['socket']}")

        # Check Ram-MOBO compatibility
        ram = components.get('RAM')
        if ram and motherboard:
            ram_info, _ = self.find_component(
                ram.split(' x2')[0])  # Handle "x2" notation
            mobo_info, _ = self.find_component(motherboard)
            if ram_info and mobo_info:
                ram_type = ram_info.get('memory_type', '')
                mobo_ram = mobo_info.get('ram', '')
                if ram_type not in mobo_ram:
                    issues.append(
                        f"❌ RAM type {ram_type} not supported by motherboard")

        return issues if issues else ["✅ All components are compatible!"]

    # Compare_builds
    def compare_builds(self, build1_type, build2_type):
        """Compare two build types"""
        build1 = self.get_build_recommendation(build1_type)
        build2 = self.get_build_recommendation(build2_type)

        if not build1 or not build2:
            return "Cannot compare those build types."

        comparison = f"🆚 {build1['name']} vs {build2['name']}\n\n"
        comparison += f"💰 Budget:\n• {build1['name']}: {build1['budget']}\n• {build2['name']}: {build2['budget']}\n\n"

        # Target audience comparison
        comparison += f"🎯 Best For:\n• {build1['name']}: {build1['target']}\n• {build2['name']}: {build2['target']}\n\n"

        comparison += "🔧 Main Differences:\n"

        # CPU Comparison
        cpu1 = build1['components'].get('CPU', 'N/A')
        cpu2 = build2['components'].get('CPU', 'N/A')
        if cpu1 != cpu2:
            comparison += f"• **CPU**: {cpu1} vs {cpu2}\n"

        # GPU Comparison
        gpu1 = build1['components'].get('GPU', 'N/A')
        gpu2 = build2['components'].get('GPU', 'N/A')
        if gpu1 != gpu2:
            comparison += f"• GPU: {gpu1} vs {gpu2}\n"

        # RAM Comparison
        ram1 = build1['components'].get('RAM', 'N/A')
        ram2 = build2['components'].get('RAM', 'N/A')
        if ram1 != ram2:
            comparison += f"• RAM: {ram1} vs {ram2}\n"

          # Storage Comparison
        storage1 = build1['components'].get('Storage', 'N/A')
        storage2 = build2['components'].get('Storage', 'N/A')
        if storage1 != storage2:
            comparison += f"• Storage: {storage1} vs {storage2}\n"

            # PSU Comparison
        psu1 = build1['components'].get('PSU', 'N/A')
        psu2 = build2['components'].get('PSU', 'N/A')
        if psu1 != psu2:
            comparison += f"• PSU: {psu1} vs {psu2}\n"

        comparison += f"\n🎮 **Performance Summary**:\n"

        if build1_type == "entry" and build2_type == "mid":
            comparison += "• Entry: Esports games, 1080p Medium\n• **Mid**: AAA games, 1440p High, Streaming\n"
            comparison += "• **Upgrade**: Entry → Mid adds dedicated GPU\n"

        elif build1_type == "mid" and build2_type == "high":
            comparison += "• **Mid**: Great 1440p gaming, casual streaming\n• **High**: 4K gaming, professional streaming\n"
            comparison += "• **Upgrade**: Mid → High improves CPU & GPU\n"

        elif build1_type == "entry" and build2_type == "high":
            comparison += "• **Entry**: Basic gaming, school/work\n• **High**: Premium gaming, content creation\n"
            comparison += "• **Upgrade**: Major performance jump\n"

        comparison += f"\n💡 **Recommendation**:\n"
        if build1_type == "entry" and build2_type == "mid":
            comparison += "Choose **Entry** if: Budget < ₱35K, casual gaming\nChoose **Mid** if: Budget ₱45K+, serious gaming/streaming"
        elif build1_type == "mid" and build2_type == "high":
            comparison += "Choose **Mid** if: Budget ₱45K-60K, great value\nChoose **High** if: Budget ₱70K+, premium experience"
        elif build1_type == "entry" and build2_type == "high":
            comparison += "Choose **Entry** if: First build, learning PC building\nChoose **High** if: Experienced, want best performance"

        return comparison

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
                print(f"Using training data response for: {user_message}")
                return previous_response

            # Greeting
            if any(word in user_lower for word in ['hi', 'hello', 'hey']):
                response = """Hello! I'm your PC Expert AI. Ask me about:"""
                self.save_training_example(user_message, response)
                return response

            # Help
            if 'help' in user_lower:
                response = """Ask me questions like:

• "price RTX 4060"
• "specs Intel i9-14900K" 
• "compatibility B550 motherboard with Ryzen 7 5700X"
• "details ASUS PRIME B550M-K"
• "ram B550M"
• "storage B550M"
• "chipset B550M"
• "tdp i9-14900K"
• "capacity Kingston Fury Beast DDR4"
• "speed Kingston Fury Beast DDR4\""""
                self.save_training_example(user_message, response)
                return response

            component_keywords = ['details', 'specs', 'specifications', 'price', 'cost', 'tdp', 'wattage',
                                  'vram', 'clock', 'speed', 'cores', 'socket', 'chipset', 'capacity', 'compatibility']
            build_keywords = ['build', 'pc build', 'setup', 'rig', 'system']

            if any(keyword in user_lower for keyword in component_keywords):
                component, confidence = self.find_component(user_message)
                if component and confidence > 0.3:
                    response = self.generate_exact_value_response(
                        user_message, component)
                    self.save_training_example(user_message, response)
                    return response

            # 🆕 BUILD RECOMMENDATION DETECTION
            build_type = self.suggest_build_type(user_message)
            if build_type:
                build_info = self.get_build_recommendation(build_type)
                if build_info:
                    response = f"🖥️ {build_info['name']}\n\n"
                    response += f"💰 Budget: {build_info['budget']}\n"
                    response += f"🎯 Perfect For: {build_info['target']}\n"
                    response += f"📝 Description: {build_info['description']}\n\n"

                    response += "🔧 Components (from my database):\n"

                    total_price = 0
                    component_prices = []

                    for comp_type, comp_name in build_info['components'].items():
                        # Get price if available
                        base_comp_name = comp_name.split(' x2')[0]
                        comp_data, _ = self.find_component(base_comp_name)

                        if comp_data and 'price' in comp_data:
                            price_text = comp_data['price']
                            # Extract numeric price value
                            price_match = re.findall(r'₱([\d,]+)', price_text)
                            if price_match:
                                price_value = int(
                                    price_match[0].replace(',', ''))

                                if ' x2' in comp_name:
                                    price_value *= 2
                                    price_text = f"₱{price_value:,} (x2)"

                                total_price += price_value
                                component_prices.append(
                                    f"• {comp_type}: {comp_name} - {price_text}")

                            else:
                                component_prices.append(
                                    f"• {comp_type}: {comp_name} - {price_text}")

                        else:
                            component_prices.append(
                                f"• {comp_type}: {comp_name} - Price not available")

                 # Add all component prices to response
                response += "\n".join(component_prices)

                # Add TOTAL PRICE
                response += f"\n\n💰 **TOTAL PRICE: ₱{total_price:,}**\n"

                response += f"\n🎮 Performance:\n{build_info['performance']}\n"
                response += f"\n🔄 Upgrade Path: {build_info['upgrade_path']}\n"

                # Add compatibility check
                compatibility = self.verify_build_compatibility(build_type)
                response += f"\n🔍 Compatibility: {compatibility[0]}"

                return response

            # 🆕 BUILD COMPARISON
            if " vs " in user_lower or "compare" in user_lower:
                if "entry" in user_lower and "mid" in user_lower:
                    return self.compare_builds("entry", "mid")
                elif "mid" in user_lower and "high" in user_lower:
                    return self.compare_builds("mid", "high")
                elif "entry" in user_lower and "high" in user_lower:
                    return self.compare_builds("entry", "high")

            # 🆕 COMPATIBILITY CHECK FOR SPECIFIC BUILD
            if "compatible" in user_lower and any(build in user_lower for build in ['entry', 'mid', 'high']):
                for build in ['entry', 'mid', 'high']:
                    if build in user_lower:
                        issues = self.verify_build_compatibility(build)
                        return f"🔍 {build.upper()} Build Compatibility:\n" + "\n".join(issues)

            # BAGONG PSU WATTAGE CALCULATOR PATTERNS - IDAGDAG MO DITO
            psu_patterns = [
                (r'psu for (.+) and (.+)', 2),
                (r'what psu for (.+) with (.+)', 2),
                (r'power supply for (.+) and (.+)', 2),
                (r'recommended psu for (.+) and (.+)', 2),
                (r'wattage for (.+) and (.+)', 2),
                (r'what wattage for (.+) and (.+)', 2),
            ]

            for pattern, num_components in psu_patterns:
                match = re.search(pattern, user_lower)
                if match:
                    if num_components == 2:
                        comp1 = match.group(1).strip()
                        comp2 = match.group(2).strip()
                        response = self.calculate_psu_wattage(comp1, comp2)
                        self.save_training_example(user_message, response)
                        return response

            # Compatibility questions
            compatibility_patterns = [
                (r'is (.+) compatible with (.+)\??', 2),
                (r'will (.+) work with (.+)\??', 2),
                (r'can (.+) use with (.+)\??', 2),
                (r'does (.+) fit (.+)\??', 2),
                (r'compatibility of (.+) and (.+)', 2),
                (r'compatibility between (.+) and (.+)', 2),
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
                self.save_training_example(user_message, response)
                return response

            elif component and confidence > 0.2:
                response = self.generate_exact_value_response(
                    user_message, component)
                self.save_training_example(user_message, response)
                return response

            # Default response
            response = "I'm not sure about that. Try asking about component specifications, compatibility, or prices. Type 'help' for examples."
            self.save_training_example(user_message, response)
            return response

        except Exception as e:
            print(f"Error in generate_response: {e}")
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
