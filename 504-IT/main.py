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


class RedirectOutput:
    """Context manager to redirect stdout to a file."""
    def __init__(self, filename):
        self.filename = filename
        self._original_stdout = sys.stdout

    def __enter__(self):
        self._file = open(self.filename, 'w')
        sys.stdout = self._file
        return self._file

    def __exit__(self, exc_type, exc_val, exc_tb):
        sys.stdout = self._original_stdout
        self._file.close()


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

        print(f"[OK] Successfully created client profile for: {self.client.name}")

    def load_client_from_file(self, filepath: str) -> None:
        """
        Load a client profile from a JSON file.

        Args:
            filepath (str): The path to the client JSON file.
        """
        try:
            self.client = Client.load_from_file(filepath)
            print(f"[OK] Successfully loaded client profile from: {filepath}")
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
            print(f"[OK] Successfully created hardware system: {self.hardware_system.name}")
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
            print(f"[OK] Successfully loaded hardware system from: {filepath}")
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
        print("[*] Running system benchmarks...")
        
        benchmark = SystemBenchmark()
        results = benchmark.run_all_benchmarks()
        
        # Save results to JSON
        results_path = os.path.join(output_dir, "system_benchmark_results.json")
        benchmark.save_results(results_path)
        
        self.benchmark_results = results
        print(f"[OK] Benchmarks completed. Results saved to '{results_path}'")

    def run_parallel_processing_demo(self, output_dir: str = ".") -> None:
        """
        Run the parallel processing demonstration and save the results.

        Args:
            output_dir (str): The directory to save demo results and plots.
        """
        os.makedirs(output_dir, exist_ok=True)
        log_file_path = os.path.join(output_dir, "outputlog.txt")
        
        # Redirect output to log file
        with RedirectOutput(log_file_path):
            print("[*] Running parallel processing demonstration...")
            
            demo = ParallelProcessingDemo()
            # Use smaller matrix size (100) for faster execution on Windows
            # Larger sizes take significantly longer
            results = demo.run_matrix_multiplication_benchmark(matrix_size=100, output_dir=output_dir)
            
            print("[OK] Parallel processing demo completed.")
        
        # Save results to JSON
        results_path = os.path.join(output_dir, "parallel_processing_results.json")
        with open(results_path, 'w') as f:
            json.dump(results, f, indent=2)

        self.parallel_results = results
        
        # Print summary to main console
        print(f"[OK] Parallel processing demo completed. Results saved to '{results_path}'")
        print(f"   Execution log saved to '{log_file_path}'")

    def generate_reports(self, output_dir: str = ".") -> None:
        """
        Generate the final reports in HTML, Markdown, and JSON formats.

        Args:
            output_dir (str): The directory to save the generated reports.
        """
        if not self.client or not self.hardware_system:
            print("Error: Client and hardware system must be created before generating reports.")
            return

        print("[*] Generating reports...")
        
        report_generator = ReportGenerator(
            client=self.client,
            hardware_system=self.hardware_system,
            benchmark_results=self.benchmark_results,
            parallel_results=self.parallel_results
        )
        
        report_generator.generate_all_reports(output_dir)
        print(f"[OK] Reports generated in '{output_dir}'")

    def run_full_workflow(self, client_type: str, output_dir: str = ".") -> None:
        """
        Run the complete end-to-end workflow.

        This includes creating a client, designing a system, running benchmarks,
        running the parallel demo, and generating the final report.

        Args:
            client_type (str): The type of client for the workflow.
            output_dir (str): The directory to save all output files.
        """
        print(f"[>] Starting full workflow for client type: '{client_type}'")
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
        print("[SUCCESS] Full workflow completed successfully!")
        print(f"[INFO] All files are located in the '{output_dir}' directory.")


def parse_arguments():
    """Parse command-line arguments for the application."""
    parser = argparse.ArgumentParser(
        description="Hardware System Design Application for 504IT Assignment.",
        epilog="Example: python main.py workflow animation --output ./my_report"
    )
    
    # Allow running without a subcommand; handle default behavior in `main()`
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

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
    import multiprocessing as mp
    mp.set_start_method('spawn', force=True)  # Explicitly use spawn on Windows
    
    args = parse_arguments()
    app = HardwareSystemDesignApp()

    # If no command provided, run the full workflow by default.
    if getattr(args, 'command', None) is None:
        print("[*] No command provided — running full workflow with default client 'animation' and output 'output'.")
        app.run_full_workflow('animation', 'output')
        return

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
    import multiprocessing as mp
    mp.freeze_support()  # Required for Windows multiprocessing
    main()


if __name__ == "__main__":
    main()