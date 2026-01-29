"""
Main Application Module
Entry point for the hardware system design application.

This script provides a command-line interface (CLI) to run the entire
hardware system design workflow or individual components. It serves as the
main orchestrator for all other modules in the project.
"""

import os
import sys
import argparse
import json
from typing import Dict, Any, Optional

# Import custom modules from the project
from client_profile import (
    create_animation_studio_client,
    create_scientific_research_client,
    create_gaming_studio_client,
    Client
)
from hardware_recommendation import (
    create_animation_studio_system,
    create_scientific_research_system,
    create_gaming_studio_system,
    get_recommended_system,
    HardwareSystem
)
from parallel_processing_demo import ParallelProcessingDemo
from benchmarking import SystemBenchmark
from report_generator import ReportGenerator


class HardwareSystemDesignApp:
    """Main application class for hardware system design and reporting."""

    def __init__(self):
        """Initialize the application with empty data containers."""
        self.client: Optional[Client] = None
        self.hardware_system: Optional[HardwareSystem] = None
        self.benchmark_results: Optional[Dict[str, Any]] = None
        self.parallel_results: Optional[Dict[str, Any]] = None

    def create_client(self, client_type: str) -> None:
        """
        Create a client profile based on the specified type.

        Args:
            client_type (str): The type of client to create ('animation', 'research', 'gaming').
        """
        if client_type.lower() == "animation":
            self.client = create_animation_studio_client()
        elif client_type.lower() == "research":
            self.client = create_scientific_research_client()
        elif client_type.lower() == "gaming":
            self.client = create_gaming_studio_client()
        else:
            print(f"Error: Unknown client type '{client_type}'.")
            print("Valid types are: animation, research, gaming")
            return

        print(f"✅ Successfully created client profile for: {self.client.name}")

    def load_client_from_file(self, filepath: str) -> None:
        """
        Load a client profile from a JSON file.

        Args:
            filepath (str): The path to the client JSON file.
        """
        try:
            self.client = Client.load_from_file(filepath)
            print(f"✅ Successfully loaded client profile from: {filepath}")
        except FileNotFoundError:
            print(f"Error: Client file not found at '{filepath}'")
        except Exception as e:
            print(f"Error loading client: {e}")

    def create_hardware_system(self, client_type: str) -> None:
        """
        Create a hardware system recommendation based on the client type.

        Args:
            client_type (str): The type of client the system is for.
        """
        self.hardware_system = get_recommended_system(client_type)
        if self.hardware_system:
            print(f"✅ Successfully created hardware system: {self.hardware_system.name}")
            print(f"   Total Price: ${self.hardware_system.get_total_price():,.2f}")
        else:
            print(f"Error: Could not create hardware system for client type '{client_type}'.")

    def load_hardware_system_from_file(self, filepath: str) -> None:
        """
        Load a hardware system configuration from a JSON file.

        Args:
            filepath (str): The path to the hardware system JSON file.
        """
        try:
            self.hardware_system = HardwareSystem.load_from_file(filepath)
            print(f"✅ Successfully loaded hardware system from: {filepath}")
        except FileNotFoundError:
            print(f"Error: Hardware system file not found at '{filepath}'")
        except Exception as e:
            print(f"Error loading hardware system: {e}")

    def run_benchmarks(self, output_dir: str = ".") -> None:
        """
        Run system benchmarks and save the results.

        Args:
            output_dir (str): The directory to save benchmark results and plots.
        """
        print("🚀 Running system benchmarks...")
        
        benchmark = SystemBenchmark()
        results = benchmark.run_all_benchmarks()
        
        # Save results to JSON
        results_path = os.path.join(output_dir, "system_benchmark_results.json")
        benchmark.save_results(results_path)
        
        # Save plot to output directory
        plot_path = os.path.join(output_dir, "system_benchmark.png")
        if os.path.exists("system_benchmark.png"):
            os.rename("system_benchmark.png", plot_path)
        
        self.benchmark_results = results
        print(f"✅ Benchmarks completed. Results saved to '{results_path}'")
        print(f"   Benchmark plot saved to '{plot_path}'")

    def run_parallel_processing_demo(self, output_dir: str = ".") -> None:
        """
        Run the parallel processing demonstration and save the results.

        Args:
            output_dir (str): The directory to save demo results and plots.
        """
        print("🚀 Running parallel processing demonstration...")
        
        demo = ParallelProcessingDemo()
        demo.run_matrix_multiplication_benchmark(matrix_size=500)
        demo.run_image_filtering_benchmark(image_size=(1000, 1000))
        
        # Save results to JSON
        results_path = os.path.join(output_dir, "parallel_processing_results.json")
        demo.save_results(results_path)
        
        # Move plots to output directory
        matrix_plot_path = os.path.join(output_dir, "matrix_multiplication_benchmark.png")
        if os.path.exists("matrix_multiplication_benchmark.png"):
            os.rename("matrix_multiplication_benchmark.png", matrix_plot_path)
        
        image_plot_path = os.path.join(output_dir, "image_filtering_benchmark.png")
        if os.path.exists("image_filtering_benchmark.png"):
            os.rename("image_filtering_benchmark.png", image_plot_path)

        self.parallel_results = demo.results
        print(f"✅ Parallel processing demo completed. Results saved to '{results_path}'")
        print(f"   Plots saved to '{matrix_plot_path}' and '{image_plot_path}'")

    def generate_reports(self, output_dir: str = ".") -> None:
        """
        Generate the final reports in HTML, Markdown, and JSON formats.

        Args:
            output_dir (str): The directory to save the generated reports.
        """
        if not self.client or not self.hardware_system:
            print("Error: Client and hardware system must be created before generating reports.")
            return

        print("📝 Generating reports...")
        
        report_generator = ReportGenerator(
            client=self.client,
            hardware_system=self.hardware_system,
            benchmark_results=self.benchmark_results,
            parallel_results=self.parallel_results
        )
        
        report_generator.generate_all_reports(output_dir)
        print(f"✅ Reports generated in '{output_dir}'")

    def run_full_workflow(self, client_type: str, output_dir: str = ".") -> None:
        """
        Run the complete end-to-end workflow.

        This includes creating a client, designing a system, running benchmarks,
        running the parallel demo, and generating the final report.

        Args:
            client_type (str): The type of client for the workflow.
            output_dir (str): The directory to save all output files.
        """
        print(f"🎯 Starting full workflow for client type: '{client_type}'")
        print("=" * 50)

        # Ensure output directory exists
        os.makedirs(output_dir, exist_ok=True)
        print(f"Output will be saved to: '{output_dir}'\n")

        # Step 1: Create Client
        self.create_client(client_type)
        if not self.client: return
        client_path = os.path.join(output_dir, "client_profile.json")
        self.client.save_to_file(client_path)
        print(f"   -> Saved client profile to '{client_path}'\n")

        # Step 2: Create Hardware System
        self.create_hardware_system(client_type)
        if not self.hardware_system: return
        system_path = os.path.join(output_dir, "hardware_system.json")
        self.hardware_system.save_to_file(system_path)
        print(f"   -> Saved hardware system to '{system_path}'\n")

        # Step 3: Run Benchmarks
        self.run_benchmarks(output_dir)
        print()

        # Step 4: Run Parallel Demo
        self.run_parallel_processing_demo(output_dir)
        print()

        # Step 5: Generate Reports
        self.generate_reports(output_dir)
        print()

        print("=" * 50)
        print("🎉 Full workflow completed successfully!")
        print(f"📁 All files are located in the '{output_dir}' directory.")


def parse_arguments():
    """Parse command-line arguments for the application."""
    parser = argparse.ArgumentParser(
        description="Hardware System Design Application for 504IT Assignment.",
        epilog="Example: python main.py workflow animation --output ./my_report"
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Available commands", required=True)

    # Full workflow command
    workflow_parser = subparsers.add_parser("workflow", help="Run the complete end-to-end workflow")
    workflow_parser.add_argument("client_type", choices=["animation", "research", "gaming"], 
                                help="Type of client to design for")
    workflow_parser.add_argument("--output", "-o", default="output", 
                                help="Directory to save all output files (default: output)")

    # Generate reports command (requires existing files)
    report_parser = subparsers.add_parser("report", help="Generate reports from existing JSON files")
    report_parser.add_argument("--client", "-c", required=True, 
                              help="Path to client profile JSON file")
    report_parser.add_argument("--system", "-s", required=True, 
                              help="Path to hardware system JSON file")
    report_parser.add_argument("--output", "-o", default="output", 
                              help="Directory to save reports (default: output)")
    
    # Individual step commands (for testing/demonstration)
    subparsers.add_parser("benchmark", help="Run system benchmarks only")
    subparsers.add_parser("parallel", help="Run parallel processing demo only")

    return parser.parse_args()


def main():
    """Main function to parse arguments and execute commands."""
    args = parse_arguments()
    app = HardwareSystemDesignApp()

    if args.command == "workflow":
        app.run_full_workflow(args.client_type, args.output)
    elif args.command == "report":
        app.load_client_from_file(args.client)
        app.load_hardware_system_from_file(args.system)
        
        # Try to auto-load benchmark and parallel results if they exist in the output dir
        benchmark_path = os.path.join(args.output, "system_benchmark_results.json")
        if os.path.exists(benchmark_path):
            with open(benchmark_path, 'r') as f:
                app.benchmark_results = json.load(f)['benchmark_results']
            print(f"Found and loaded benchmark results from '{benchmark_path}'")

        parallel_path = os.path.join(args.output, "parallel_processing_results.json")
        if os.path.exists(parallel_path):
            with open(parallel_path, 'r') as f:
                app.parallel_results = json.load(f)
            print(f"Found and loaded parallel results from '{parallel_path}'")
            
        app.generate_reports(args.output)
    elif args.command == "benchmark":
        app.run_benchmarks(args.output)
    elif args.command == "parallel":
        app.run_parallel_processing_demo(args.output)
    else:
        # This case should not be reached due to 'required=True' in subparsers
        print("No command specified. Use --help for available commands.")


if __name__ == "__main__":
    main()