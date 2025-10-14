import os
from flask import Flask, render_template, request, jsonify
import json
import re

app = Flask(__name__)


class PCChatbotSimple:
    def __init__(self):
        print("Initializing PC Expert AI (Simple Version)...")
        self.components_db = self.load_all_components()
        print(
            f"ARsemble AI Ready! Loaded {len(self.components_db)} components!")

    def load_all_components(self):
        """Load COMPLETE PC components database"""
        components = {
            # ==========================
            # ========== GPUs ==========
            # ==========================
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
            }
        }
        return components

    def find_component(self, query):
        """Simple component search"""
        query_lower = query.lower().strip()
        print(f"Searching: '{query}'")

        # Exact match
        for comp_key, component in self.components_db.items():
            if comp_key in query_lower or component['name'].lower() in query_lower:
                print(f"MATCH: {component['name']}")
                return component, 1.0

        # Partial match
        for comp_key, component in self.components_db.items():
            if any(word in query_lower for word in comp_key.split()):
                print(f"PARTIAL MATCH: {component['name']}")
                return component, 0.7

        return None, 0.0

    def generate_response(self, user_message):
        """Generate response based on user message"""
        try:
            user_lower = user_message.lower().strip()

            if not user_message:
                return "Please type a question about PC components!"

            # Help
            if 'help' in user_lower:
                return """Ask me questions like:
• "price RTX 4060"
• "specs Intel i7-14700K" 
• "details RTX 3050"
• "compatibility questions" """

            # Find component
            component, confidence = self.find_component(user_message)

            if component and confidence > 0.3:
                # Return component info
                response = f"{component['name']} ({component['type']})\n"
                if 'price' in component:
                    response += f"Price: {component['price']}\n"
                if 'vram' in component:
                    response += f"VRAM: {component['vram']}\n"
                if 'clock' in component:
                    response += f"Clock: {component['clock']}\n"
                if 'power' in component:
                    response += f"Power: {component['power']}\n"
                return response

            return "I'm not sure about that. Try asking about component specifications or prices. Type 'help' for examples."

        except Exception as e:
            return f"Sorry, I encountered an error: {str(e)}"


# Initialize chatbot
chatbot = PCChatbotSimple()


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/chat', methods=['POST'])
def chat():
    try:
        user_message = request.json.get('message', '')
        print(f"Received: {user_message}")

        if not user_message:
            return jsonify({'response': 'Please enter a message'})

        response = chatbot.generate_response(user_message)
        print(f"Response: {response}")

        return jsonify({'response': response})

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'response': 'Sorry, there was an error processing your request.'})


@app.route('/health')
def health():
    return jsonify({'status': 'healthy'})


@app.route('/test')
def test():
    return jsonify({'message': 'ARsemble AI Simple - Working!'})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000, debug=True)
