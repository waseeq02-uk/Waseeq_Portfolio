"""
Report Generator Module
Generates a comprehensive hardware system design report
"""

import os
import json
from datetime import datetime
from typing import Dict, List, Any, Optional


class ReportGenerator:
    """Class to generate hardware system design reports"""
    
    def __init__(self, client, hardware_system, benchmark_results=None, parallel_results=None):
        """
        Initialize the report generator
        
        Args:
            client: Client object
            hardware_system: HardwareSystem object
            benchmark_results (dict, optional): System benchmark results
            parallel_results (dict, optional): Parallel processing results
        """
        self.client = client
        self.hardware_system = hardware_system
        self.benchmark_results = benchmark_results
        self.parallel_results = parallel_results
        self.report_date = datetime.now().strftime("%Y-%m-%d")
    
    def generate_html_report(self, output_path: str = "hardware_system_report.html") -> None:
        """
        Generate an HTML report
        
        Args:
            output_path (str): Path to save the HTML report
        """
        html_content = f"""<!DOCTYPE html>
<html>
<head>
    <title>Hardware System Design Report</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; }}
        h1 {{ color: #333; border-bottom: 2px solid #0066cc; padding-bottom: 10px; }}
        h2 {{ color: #0066cc; }}
        table {{ border-collapse: collapse; width: 100%; margin: 20px 0; }}
        th, td {{ border: 1px solid #ddd; padding: 12px; text-align: left; }}
        th {{ background-color: #0066cc; color: white; }}
        tr:nth-child(even) {{ background-color: #f2f2f2; }}
    </style>
</head>
<body>
    <h1>Hardware System Design Report</h1>
    <p><strong>Client:</strong> {self.client.name}</p>
    <p><strong>Date:</strong> {self.report_date}</p>
    <p><strong>Industry:</strong> {self.client.industry}</p>
    
    <h2>System Summary</h2>
    <p><strong>System Name:</strong> {self.hardware_system.name}</p>
    <p><strong>Total Cost:</strong> ${self.hardware_system.get_total_price():,.2f}</p>
    <p><strong>Client Budget:</strong> ${self.client.budget:,.2f}</p>
    
    <h2>Hardware Components</h2>
    <table>
        <tr>
            <th>Component Type</th>
            <th>Component Name</th>
            <th>Specifications</th>
            <th>Price</th>
        </tr>
"""
        
        for component in self.hardware_system.components:
            html_content += f"""        <tr>
            <td>{component.component_type}</td>
            <td>{component.name}</td>
            <td>{getattr(component, 'specifications', 'N/A')}</td>
            <td>${component.price:,.2f}</td>
        </tr>
"""
        
        html_content += """    </table>
    
    <h2>Benchmark Results</h2>
"""
        
        if self.benchmark_results:
            html_content += f"""    <pre>{json.dumps(self.benchmark_results, indent=2)}</pre>
"""
        else:
            html_content += """    <p>No benchmark results available.</p>
"""
        
        html_content += """</body>
</html>
"""
        
        with open(output_path, 'w') as f:
            f.write(html_content)
    
    def generate_markdown_report(self, output_path: str = "hardware_system_report.md") -> None:
        """
        Generate a Markdown report
        
        Args:
            output_path (str): Path to save the Markdown report
        """
        md_content = f"""# Hardware System Design Report

**Client:** {self.client.name}  
**Date:** {self.report_date}  
**Industry:** {self.client.industry}  

## Executive Summary

This report presents a comprehensive hardware system design for {self.client.name}.

## System Overview

**System Name:** {self.hardware_system.name}  
**Total Cost:** ${self.hardware_system.get_total_price():,.2f}  
**Client Budget:** ${self.client.budget:,.2f}  

## Hardware Components

| Component Type | Name | Specifications | Price |
|---|---|---|---|
"""
        
        for component in self.hardware_system.components:
            specs = getattr(component, 'specifications', 'N/A')
            md_content += f"| {component.component_type} | {component.name} | {specs} | ${component.price:,.2f} |\n"
        
        md_content += f"""
## Benchmark Results

"""
        
        if self.benchmark_results:
            md_content += f"""```json
{json.dumps(self.benchmark_results, indent=2)}
```
"""
        else:
            md_content += "No benchmark results available.\n"
        
        # Add reference to execution log if it exists
        import os
        log_file = os.path.join(os.path.dirname(output_path), "outputlog.txt")
        if os.path.exists(log_file):
            md_content += f"""
## Execution Log

The parallel processing demonstration was executed and logged to `outputlog.txt`. Key results:

- Sequential matrix multiplication performance
- NumPy optimized multiplication performance  
- Multiprocessing parallelization speedup
- Verification of result accuracy

*See `outputlog.txt` in the submission for complete execution details.*

"""
        
        with open(output_path, 'w') as f:
            f.write(md_content)
    
    def generate_all_reports(self, output_dir: str = ".") -> None:
        """
        Generate all available reports (HTML and Markdown) in the specified directory.
        
        Args:
            output_dir (str): Directory to save all reports (default: current directory)
        """
        # Ensure output directory exists
        os.makedirs(output_dir, exist_ok=True)
        
        # Generate HTML report
        html_path = os.path.join(output_dir, "hardware_system_report.html")
        self.generate_html_report(html_path)
        
        # Generate Markdown report
        md_path = os.path.join(output_dir, "hardware_system_report.md")
        self.generate_markdown_report(md_path)
