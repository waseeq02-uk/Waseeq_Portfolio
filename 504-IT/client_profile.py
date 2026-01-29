"""
Client Profile Module
Defines the fictional client for the hardware system design assignment
"""

class Client:
    """Represents a client with specific hardware needs"""
    
    def __init__(self, name, industry, size, primary_use_cases, software_requirements, 
                 performance_goals, budget, constraints):
        """
        Initialize a client profile
        
        Args:
            name (str): Client company name
            industry (str): Industry sector
            size (str): Company size (small, medium, large)
            primary_use_cases (list): Main use cases for the computer system
            software_requirements (list): Software that needs to run on the system
            performance_goals (dict): Performance targets
            budget (float): Budget in USD
            constraints (list): Technical or operational constraints
        """
        self.name = name
        self.industry = industry
        self.size = size
        self.primary_use_cases = primary_use_cases
        self.software_requirements = software_requirements
        self.performance_goals = performance_goals
        self.budget = budget
        self.constraints = constraints
    
    def get_profile_summary(self):
        """Generate a summary of the client profile"""
        summary = f"Client: {self.name}\n"
        summary += f"Industry: {self.industry}\n"
        summary += f"Company Size: {self.size}\n"
        summary += f"Primary Use Cases: {', '.join(self.primary_use_cases)}\n"
        summary += f"Software Requirements: {', '.join(self.software_requirements)}\n"
        summary += f"Budget: ${self.budget:,.2f}\n"
        summary += f"Constraints: {', '.join(self.constraints)}\n"
        
        summary += "\nPerformance Goals:\n"
        for goal, target in self.performance_goals.items():
            summary += f"- {goal}: {target}\n"
            
        return summary
    
    def save_to_file(self, filepath):
        """Save client profile to a JSON file"""
        import json
        
        client_data = {
            "name": self.name,
            "industry": self.industry,
            "size": self.size,
            "primary_use_cases": self.primary_use_cases,
            "software_requirements": self.software_requirements,
            "performance_goals": self.performance_goals,
            "budget": self.budget,
            "constraints": self.constraints
        }
        
        with open(filepath, 'w') as f:
            json.dump(client_data, f, indent=4)
    
    @classmethod
    def load_from_file(cls, filepath):
        """Load client profile from a JSON file"""
        import json
        
        with open(filepath, 'r') as f:
            client_data = json.load(f)
        
        return cls(
            name=client_data["name"],
            industry=client_data["industry"],
            size=client_data["size"],
            primary_use_cases=client_data["primary_use_cases"],
            software_requirements=client_data["software_requirements"],
            performance_goals=client_data["performance_goals"],
            budget=client_data["budget"],
            constraints=client_data["constraints"]
        )


def create_animation_studio_client():
    """Create a client profile for an animation studio"""
    return Client(
        name="Creative Visions Animation Studio",
        industry="3D Animation and Visual Effects",
        size="Medium",
        primary_use_cases=[
            "3D modeling and animation",
            "High-resolution rendering",
            "Video editing and compositing",
            "Texture creation and editing"
        ],
        software_requirements=[
            "Blender",
            "Autodesk Maya",
            "Adobe Creative Suite",
            "Various rendering engines (Cycles, V-Ray, Arnold)"
        ],
        performance_goals={
            "rendering_time_reduction": "40%",
            "viewport_performance": "Smooth with complex scenes",
            "video_editing": "4K support",
            "reliability": "8+ hours continuous operation"
        },
        budget=3000.0,
        constraints=[
            "Budget limit of $3,000 per workstation",
            "Must be upgradeable for future needs",
            "Energy efficiency to reduce operational costs",
            "Low noise levels for studio environment"
        ]
    )


def create_scientific_research_client():
    """Create a client profile for a scientific research institution"""
    return Client(
        name="Quantum Research Institute",
        industry="Scientific Research",
        size="Large",
        primary_use_cases=[
            "Complex simulations",
            "Data analysis and visualization",
            "Machine learning model training",
            "Statistical computations"
        ],
        software_requirements=[
            "MATLAB",
            "Python with scientific libraries",
            "R",
            "TensorFlow/PyTorch",
            "SAS"
        ],
        performance_goals={
            "simulation_speed": "50% faster than current systems",
            "data_processing": "Handle datasets up to 1TB",
            "model_training": "Reduce training time by 30%",
            "reliability": "24/7 operation capability"
        },
        budget=4500.0,
        constraints=[
            "Budget limit of $4,500 per workstation",
            "Must support high-speed networking",
            "ECC memory preferred for data integrity",
            "Expandable storage options"
        ]
    )


def create_gaming_studio_client():
    """Create a client profile for a game development studio"""
    return Client(
        name="PixelForge Games",
        industry="Game Development",
        size="Small",
        primary_use_cases=[
            "Game engine development",
            "Asset creation and editing",
            "Testing and debugging",
            "Compilation and building"
        ],
        software_requirements=[
            "Unreal Engine",
            "Unity",
            "Visual Studio",
            "Adobe Creative Suite",
            "Substance Painter"
        ],
        performance_goals={
            "compilation_time": "Reduce by 50%",
            "engine_performance": "Maintain 60fps with complex scenes",
            "asset_loading": "Minimize loading times",
            "multi-tasking": "Smooth operation with multiple tools"
        },
        budget=3500.0,
        constraints=[
            "Budget limit of $3,500 per workstation",
            "Must support multiple monitors",
            "High-quality audio support",
            "VR development capabilities"
        ]
    )