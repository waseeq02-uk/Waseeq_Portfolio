"""
Hardware Recommendation Module
Provides hardware component recommendations based on client needs
"""

import json
from typing import Dict, List, Tuple


class Component:
    """Represents a hardware component"""
    
    def __init__(self, name, component_type, price, specs, justification, performance_impact):
        """
        Initialize a hardware component
        
        Args:
            name (str): Component name/model
            component_type (str): Type of component (CPU, GPU, etc.)
            price (float): Component price in USD
            specs (dict): Technical specifications
            justification (str): Justification for choosing this component
            performance_impact (str): Impact on system performance
        """
        self.name = name
        self.component_type = component_type
        self.price = price
        self.specs = specs
        self.justification = justification
        self.performance_impact = performance_impact
    
    def get_details(self):
        """Get formatted component details"""
        details = f"{self.component_type}: {self.name}\n"
        details += f"Price: ${self.price:.2f}\n"
        details += f"Specifications:\n"
        
        for spec, value in self.specs.items():
            details += f"  - {spec}: {value}\n"
        
        details += f"Justification: {self.justification}\n"
        details += f"Performance Impact: {self.performance_impact}\n"
        
        return details


class HardwareSystem:
    """Represents a complete hardware system"""
    
    def __init__(self, name, client_type, components):
        """
        Initialize a hardware system
        
        Args:
            name (str): System name
            client_type (str): Type of client this system is designed for
            components (list): List of Component objects
        """
        self.name = name
        self.client_type = client_type
        self.components = components
    
    def get_total_price(self):
        """Calculate the total price of the system"""
        return sum(component.price for component in self.components)
    
    def get_component_by_type(self, component_type):
        """Get a component by its type"""
        for component in self.components:
            if component.component_type == component_type:
                return component
        return None
    
    def get_system_summary(self):
        """Generate a summary of the system"""
        summary = f"System: {self.name}\n"
        summary += f"Client Type: {self.client_type}\n"
        summary += f"Total Price: ${self.get_total_price():.2f}\n\n"
        
        summary += "Components:\n"
        for component in self.components:
            summary += f"- {component.component_type}: {component.name} (${component.price:.2f})\n"
        
        return summary
    
    def get_detailed_specifications(self):
        """Get detailed specifications of all components"""
        details = f"System: {self.name}\n"
        details += f"Client Type: {self.client_type}\n"
        details += f"Total Price: ${self.get_total_price():.2f}\n\n"
        
        for component in self.components:
            details += component.get_details()
            details += "\n"
        
        return details
    
    def save_to_file(self, filepath):
        """Save system configuration to a JSON file"""
        system_data = {
            "name": self.name,
            "client_type": self.client_type,
            "total_price": self.get_total_price(),
            "components": []
        }
        
        for component in self.components:
            component_data = {
                "name": component.name,
                "component_type": component.component_type,
                "price": component.price,
                "specs": component.specs,
                "justification": component.justification,
                "performance_impact": component.performance_impact
            }
            system_data["components"].append(component_data)
        
        with open(filepath, 'w') as f:
            json.dump(system_data, f, indent=4)
    
    @classmethod
    def load_from_file(cls, filepath):
        """Load system configuration from a JSON file"""
        with open(filepath, 'r') as f:
            system_data = json.load(f)
        
        components = []
        for component_data in system_data["components"]:
            component = Component(
                name=component_data["name"],
                component_type=component_data["component_type"],
                price=component_data["price"],
                specs=component_data["specs"],
                justification=component_data["justification"],
                performance_impact=component_data["performance_impact"]
            )
            components.append(component)
        
        return cls(
            name=system_data["name"],
            client_type=system_data["client_type"],
            components=components
        )


def create_animation_studio_system():
    """Create a hardware system for an animation studio"""
    components = [
        Component(
            name="AMD Ryzen 9 5950X",
            component_type="CPU",
            price=799.0,
            specs={
                "Cores": "16",
                "Threads": "32",
                "Base Clock": "3.4GHz",
                "Boost Clock": "4.9GHz",
                "Cache": "72MB",
                "TDP": "105W",
                "Architecture": "Zen 3 (7nm)"
            },
            justification="The Ryzen 9 5950X offers exceptional multi-threaded performance crucial for 3D rendering. With 16 cores and 32 threads, it can handle multiple rendering tasks simultaneously.",
            performance_impact="According to benchmarks from Puget Systems, the Ryzen 9 5950X outperforms competing Intel processors in Blender rendering by approximately 15-20% at a similar price point."
        ),
        Component(
            name="NVIDIA RTX 3080",
            component_type="GPU",
            price=699.0,
            specs={
                "CUDA Cores": "8704",
                "RT Cores": "68 (2nd generation)",
                "Tensor Cores": "272 (3rd generation)",
                "Memory": "10GB GDDR6X",
                "Memory Interface": "320-bit",
                "Power Consumption": "320W"
            },
            justification="The RTX 3080 provides exceptional performance for both viewport interactions and GPU-accelerated rendering. Its CUDA cores are well-supported by major 3D applications.",
            performance_impact="In Blender's Cycles renderer, the RTX 3080 can reduce rendering times by up to 50% compared to the previous generation."
        ),
        Component(
            name="G.Skill Trident Z Neo 64GB DDR4-3600",
            component_type="Memory",
            price=329.0,
            specs={
                "Capacity": "64GB (4x16GB)",
                "Type": "DDR4",
                "Speed": "3600MHz",
                "Timings": "16-19-19-39",
                "Voltage": "1.35V"
            },
            justification="64GB of RAM provides sufficient capacity for complex 3D scenes, high-resolution textures, and multitasking between applications.",
            performance_impact="According to Puget Systems' benchmarks, 64GB of RAM provides optimal performance for most 3D animation workflows."
        ),
        Component(
            name="Samsung 980 Pro 1TB NVMe SSD",
            component_type="Primary Storage",
            price=229.0,
            specs={
                "Capacity": "1TB",
                "Interface": "PCIe 4.0 NVMe",
                "Sequential Read": "Up to 7,000 MB/s",
                "Sequential Write": "Up to 5,000 MB/s",
                "Form Factor": "M.2 2280"
            },
            justification="The NVMe SSD provides lightning-fast access for the operating system, applications, and active projects.",
            performance_impact="Fast storage significantly reduces loading times for large 3D scenes and assets. NVMe drives can reduce project loading times by up to 60% compared to SATA SSDs."
        ),
        Component(
            name="Samsung 870 EVO 4TB SATA SSD",
            component_type="Secondary Storage",
            price=399.0,
            specs={
                "Capacity": "4TB",
                "Interface": "SATA III",
                "Sequential Read": "Up to 560 MB/s",
                "Sequential Write": "Up to 530 MB/s",
                "Form Factor": "2.5-inch"
            },
            justification="The larger SATA SSD offers ample storage for completed projects at a more cost-effective price point.",
            performance_impact="Provides sufficient storage for large project files while maintaining good performance for asset access."
        ),
        Component(
            name="ASUS ROG Strix X570-E Gaming",
            component_type="Motherboard",
            price=379.0,
            specs={
                "Chipset": "AMD X570",
                "Socket": "AM4",
                "Memory Support": "Up to 128GB DDR4 4800MHz+",
                "PCIe Slots": "2x PCIe 4.0 x16, 1x PCIe 4.0 x1, 1x PCIe 3.0 x16",
                "M.2 Slots": "2x PCIe 4.0 M.2",
                "USB": "8x USB 3.2 Gen 2, 2x USB 2.0",
                "Networking": "Intel 2.5G LAN, Wi-Fi 6 (802.11ax)"
            },
            justification="This motherboard provides excellent connectivity, PCIe 4.0 support, and robust power delivery for the high-performance components.",
            performance_impact="PCIe 4.0 support provides double the bandwidth of PCIe 3.0, benefiting both GPU and storage performance."
        ),
        Component(
            name="Corsair RM850x",
            component_type="Power Supply",
            price=129.0,
            specs={
                "Wattage": "850W",
                "Efficiency": "80+ Gold",
                "Modular": "Fully Modular",
                "Warranty": "10 Years"
            },
            justification="An 850W power supply provides sufficient headroom for the high-performance components while maintaining efficiency.",
            performance_impact="The 80+ Gold certification ensures energy efficiency, reducing operational costs over time."
        ),
        Component(
            name="Noctua NH-D15",
            component_type="CPU Cooler",
            price=99.0,
            specs={
                "Height": "165mm",
                "Fan Speed": "1500 RPM",
                "Noise Level": "24.6 dBA",
                "Compatibility": "AM4, LGA1200, LGA115x"
            },
            justification="The NH-D15 provides excellent cooling performance for the Ryzen 9 5950X while maintaining low noise levels.",
            performance_impact="Effective cooling ensures consistent performance under heavy rendering loads and extends component lifespan."
        ),
        Component(
            name="Fractal Design Define 7 Compact",
            component_type="Case",
            price=99.0,
            specs={
                "Form Factor": "Mid Tower",
                "Material": "Steel, Aluminum",
                "Dimensions": "447 x 220 x 476 mm",
                "Weight": "10.9 kg"
            },
            justification="This case offers good airflow, sound dampening features, and a professional appearance suitable for a studio environment.",
            performance_impact="Good airflow ensures components stay cool under load, while sound dampening reduces noise in the studio environment."
        )
    ]
    
    return HardwareSystem(
        name="Creative Visions Animation Workstation",
        client_type="Animation Studio",
        components=components
    )


def create_scientific_research_system():
    """Create a hardware system for a scientific research institution"""
    components = [
        Component(
            name="Intel Xeon W-2295",
            component_type="CPU",
            price=1299.0,
            specs={
                "Cores": "18",
                "Threads": "36",
                "Base Clock": "3.0GHz",
                "Boost Clock": "4.6GHz",
                "Cache": "24.75MB",
                "TDP": "165W",
                "Architecture": "Cascade Lake (14nm)",
                "ECC Support": "Yes"
            },
            justification="The Xeon W-2295 offers high core count and ECC memory support, crucial for scientific computations and data integrity.",
            performance_impact="The high core count significantly improves parallel processing capabilities for simulations and data analysis."
        ),
        Component(
            name="NVIDIA RTX A4000",
            component_type="GPU",
            price=1049.0,
            specs={
                "CUDA Cores": "6144",
                "RT Cores": "48 (2nd generation)",
                "Tensor Cores": "192 (3rd generation)",
                "Memory": "16GB GDDR6 with ECC",
                "Memory Interface": "256-bit",
                "Power Consumption": "160W"
            },
            justification="The RTX A4000 is designed for professional workloads with certified drivers and ECC memory support.",
            performance_impact="Provides excellent performance for scientific visualization and GPU-accelerated computing tasks."
        ),
        Component(
            name="Kingston 128GB DDR4-3200 ECC RAM",
            component_type="Memory",
            price=799.0,
            specs={
                "Capacity": "128GB (4x32GB)",
                "Type": "DDR4 ECC",
                "Speed": "3200MHz",
                "Timings": "22-22-22-52",
                "Voltage": "1.2V"
            },
            justification="128GB of ECC RAM provides ample capacity for large datasets while ensuring data integrity through error correction.",
            performance_impact="ECC memory prevents data corruption during long-running simulations and analyses."
        ),
        Component(
            name="Samsung 980 Pro 2TB NVMe SSD",
            component_type="Primary Storage",
            price=349.0,
            specs={
                "Capacity": "2TB",
                "Interface": "PCIe 4.0 NVMe",
                "Sequential Read": "Up to 7,000 MB/s",
                "Sequential Write": "Up to 5,000 MB/s",
                "Form Factor": "M.2 2280"
            },
            justification="The high-capacity NVMe SSD provides fast access to frequently used data and applications.",
            performance_impact="Significantly reduces loading times for large datasets and applications."
        ),
        Component(
            name="Seagate IronWolf Pro 8TB HDD",
            component_type="Secondary Storage",
            price="299.0",
            specs={
                "Capacity": "8TB",
                "Interface": "SATA III 6Gb/s",
                "Cache": "256MB",
                "Rotational Speed": "7200 RPM",
                "Workload Rate": "300TB/year"
            },
            justification="The high-capacity HDD provides ample storage for large datasets and backups.",
            performance_impact="Enables storage of large research datasets without compromising system performance."
        ),
        Component(
            name="ASUS Pro WS X570-ACE",
            component_type="Motherboard",
            price=449.0,
            specs={
                "Chipset": "AMD X570",
                "Socket": "AM4",
                "Memory Support": "Up to 256GB DDR4 ECC",
                "PCIe Slots": "3x PCIe 4.0 x16, 1x PCIe 4.0 x1",
                "M.2 Slots": "2x PCIe 4.0 M.2",
                "USB": "10x USB 3.2 Gen 2, 4x USB 2.0",
                "Networking": "Intel 2.5G LAN, 10G LAN"
            },
            justification="This workstation motherboard provides excellent stability, ECC memory support, and high-speed networking.",
            performance_impact="The 10G LAN capability enables fast data transfer over the network, crucial for collaborative research."
        ),
        Component(
            name="Corsair RM1000x",
            component_type="Power Supply",
            price=169.0,
            specs={
                "Wattage": "1000W",
                "Efficiency": "80+ Gold",
                "Modular": "Fully Modular",
                "Warranty": "10 Years"
            },
            justification="A 1000W power supply provides sufficient headroom for the high-performance components and potential expansion.",
            performance_impact="Ensures stable power delivery for long-running computations and system stability."
        ),
        Component(
            name="Noctua NH-U14S TR4-SP3",
            component_type="CPU Cooler",
            price=79.0,
            specs={
                "Height": "165mm",
                "Fan Speed": "1500 RPM",
                "Noise Level": "24.6 dBA",
                "Compatibility": "sTRX4, sTR4"
            },
            justification="The NH-U14S TR4-SP3 is specifically designed for Threadripper and Xeon processors, providing excellent cooling performance.",
            performance_impact="Effective cooling ensures consistent performance during extended computation periods."
        ),
        Component(
            name="Lian Li PC-O11 Dynamic",
            component_type="Case",
            price=149.0,
            specs={
                "Form Factor": "Mid Tower",
                "Material": "Aluminum, Tempered Glass",
                "Dimensions": "445 x 272 x 446 mm",
                "Weight": "9.3 kg"
            },
            justification="This case offers excellent airflow and a professional appearance suitable for a research environment.",
            performance_impact="Good airflow ensures components stay cool during extended computation periods."
        )
    ]
    
    return HardwareSystem(
        name="Quantum Research Workstation",
        client_type="Scientific Research",
        components=components
    )


def create_gaming_studio_system():
    """Create a hardware system for a game development studio"""
    components = [
        Component(
            name="Intel Core i9-12900K",
            component_type="CPU",
            price=589.0,
            specs={
                "Cores": "16 (8P+8E)",
                "Threads": "24",
                "P-Core Base Clock": "3.2GHz",
                "P-Core Boost Clock": "5.2GHz",
                "E-Core Base Clock": "2.4GHz",
                "E-Core Boost Clock": "3.9GHz",
                "Cache": "30MB",
                "TDP": "125W/241W",
                "Architecture": "Alder Lake (Intel 7)"
            },
            justification="The Core i9-12900K offers excellent single-threaded performance for compilation and multi-threaded performance for multitasking.",
            performance_impact="The high single-threaded performance significantly reduces compilation times, while the hybrid architecture provides efficient multitasking."
        ),
        Component(
            name="NVIDIA RTX 3070 Ti",
            component_type="GPU",
            price=599.0,
            specs={
                "CUDA Cores": "6144",
                "RT Cores": "48 (2nd generation)",
                "Tensor Cores": "192 (3rd generation)",
                "Memory": "8GB GDDR6X",
                "Memory Interface": "256-bit",
                "Power Consumption": "290W"
            },
            justification="The RTX 3070 Ti provides excellent performance for game development and testing, with good balance of price and performance.",
            performance_impact="Enables smooth operation of game engines at high settings and efficient asset creation workflows."
        ),
        Component(
            name="G.Skill Trident Z5 RGB 32GB DDR5-6000",
            component_type="Memory",
            price=299.0,
            specs={
                "Capacity": "32GB (2x16GB)",
                "Type": "DDR5",
                "Speed": "6000MHz",
                "Timings": "36-38-38-78",
                "Voltage": "1.35V"
            },
            justification="32GB of fast DDR5 memory provides sufficient capacity for game development while ensuring smooth multitasking.",
            performance_impact="DDR5's higher bandwidth and improved efficiency benefit game engine performance and compilation times."
        ),
        Component(
            name="WD Black SN850 1TB NVMe SSD",
            component_type="Primary Storage",
            price=179.0,
            specs={
                "Capacity": "1TB",
                "Interface": "PCIe 4.0 NVMe",
                "Sequential Read": "Up to 7,000 MB/s",
                "Sequential Write": "Up to 5,300 MB/s",
                "Form Factor": "M.2 2280"
            },
            justification="The high-performance NVMe SSD provides fast access to game assets and reduces loading times during development.",
            performance_impact="Significantly reduces project loading times and improves overall system responsiveness."
        ),
        Component(
            name="Samsung 870 QVO 4TB SATA SSD",
            component_type="Secondary Storage",
            price=349.0,
            specs={
                "Capacity": "4TB",
                "Interface": "SATA III",
                "Sequential Read": "Up to 560 MB/s",
                "Sequential Write": "Up to 530 MB/s",
                "Form Factor": "2.5-inch"
            },
            justification="The high-capacity SATA SSD provides ample storage for game assets and projects.",
            performance_impact="Provides sufficient storage for large game projects while maintaining good performance."
        ),
        Component(
            name="ASUS ROG Strix Z690-E Gaming WiFi",
            component_type="Motherboard",
            price=429.0,
            specs={
                "Chipset": "Intel Z690",
                "Socket": "LGA 1700",
                "Memory Support": "Up to 128GB DDR5 6400MHz+",
                "PCIe Slots": "2x PCIe 5.0 x16, 1x PCIe 4.0 x4",
                "M.2 Slots": "4x PCIe 4.0 M.2",
                "USB": "6x USB 3.2 Gen 2x2, 6x USB 3.2 Gen 1, 4x USB 2.0",
                "Networking": "Intel 2.5G LAN, Wi-Fi 6E (802.11ax)"
            },
            justification="This motherboard provides excellent connectivity, PCIe 5.0 support for future upgrades, and robust power delivery.",
            performance_impact="PCIe 5.0 support ensures future compatibility with next-generation components."
        ),
        Component(
            name="Corsair RM750x",
            component_type="Power Supply",
            price=119.0,
            specs={
                "Wattage": "750W",
                "Efficiency": "80+ Gold",
                "Modular": "Fully Modular",
                "Warranty": "10 Years"
            },
            justification="A 750W power supply provides sufficient power for the components while maintaining efficiency.",
            performance_impact="The 80+ Gold certification ensures energy efficiency, reducing operational costs."
        ),
        Component(
            name="NZXT Kraken Z73",
            component_type="CPU Cooler",
            price=249.0,
            specs={
                "Radiator Size": "360mm",
                "Fan Speed": "800-1800 RPM",
                "Noise Level": "21-36 dBA",
                "Display": "2.36\" LCD",
                "Compatibility": "LGA 1700, LGA1200, LGA115x, AM4"
            },
            justification="The Kraken Z73 provides excellent cooling performance for the Core i9-12900K while adding visual appeal.",
            performance_impact="Effective liquid cooling ensures consistent performance under heavy compilation loads."
        ),
        Component(
            name="Lian Li O11 Vision",
            component_type="Case",
            price=179.0,
            specs={
                "Form Factor": "Mid Tower",
                "Material": "Aluminum, Tempered Glass",
                "Dimensions": "455 x 285 x 462 mm",
                "Weight": "10.7 kg"
            },
            justification="This case offers excellent airflow and a panoramic view of the components, ideal for showcasing development hardware.",
            performance_impact="Excellent airflow ensures components stay cool during extended development sessions."
        ),
    ]
    
    return HardwareSystem(
        name="PixelForge Games Development Workstation",
        client_type="Game Development",
        components=components
    )


def get_recommended_system(client_type):
    """Get a recommended system based on client type"""
    if client_type.lower() == "animation studio":
        return create_animation_studio_system()
    elif client_type.lower() == "scientific research":
        return create_scientific_research_system()
    elif client_type.lower() == "game development":
        return create_gaming_studio_system()
    else:
        return create_animation_studio_system()  # Default
