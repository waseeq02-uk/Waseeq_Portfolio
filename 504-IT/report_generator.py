"""
Report Generator Module
Generates a comprehensive hardware system design report
"""

import os
import json
from datetime import datetime
from typing import Dict, List, Any, Optional
from jinja2 import Template


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
        # HTML template
        template_str = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Hardware System Design Report for {{ client.name }}</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            line-height: 1.6;
            margin: 0;
            padding: 20px;
            color: #333;
        }
        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f9f9f9;
            border-radius: 10px;
            box-shadow: 0 0 10px rgba(0,0,0,0.1);
        }
        h1, h2, h3 {
            color: #2c3e50;
        }
        h1 {
            border-bottom: 2px solid #3498db;
            padding-bottom: 10px;
        }
        h2 {
            border-bottom: 1px solid #3498db;
            padding-bottom: 5px;
            margin-top: 30px;
        }
        table {
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
        }
        th, td {
            border: 1px solid #ddd;
            padding: 12px;
            text-align: left;
        }
        th {
            background-color: #3498db;
            color: white;
        }
        tr:nth-child(even) {
            background-color: #f2f2f2;
        }
        .component-card {
            background-color: white;
            border-radius: 8px;
            padding: 20px;
            margin-bottom: 20px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        .component-name {
            font-weight: bold;
            font-size: 1.2em;
            color: #2c3e50;
        }
        .component-price {
            color: #27ae60;
            font-weight: bold;
        }
        .total-price {
            font-size: 1.2em;
            font-weight: bold;
            color: #2c3e50;
            text-align: right;
            margin: 20px 0;
        }
        .footer {
            margin-top: 30px;
            padding-top: 20px;
            border-top: 1px solid #ddd;
            font-size: 0.9em;
            color: #7f8c8d;
        }
        .benchmark-chart {
            text-align: center;
            margin: 20px 0;
        }
        .benchmark-chart img {
            max-width: 100%;
            height: auto;
            border: 1px solid #ddd;
            border-radius: 4px;
        }
        .toc {
            background-color: #ecf0f1;
            padding: 15px;
            border-radius: 5px;
            margin-bottom: 20px;
        }
        .toc ul {
            padding-left: 20px;
        }
        .toc li {
            margin: 5px 0;
        }
        .toc a {
            text-decoration: none;
            color: #3498db;
        }
        .toc a:hover {
            text-decoration: underline;
        }
        .code-block {
            background-color: #f8f8f8;
            border: 1px solid #ddd;
            border-radius: 4px;
            padding: 15px;
            overflow-x: auto;
            font-family: monospace;
            margin: 15px 0;
        }
        .highlight {
            background-color: #ffffcc;
            padding: 2px 4px;
            border-radius: 3px;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Hardware System Design Report for {{ client.name }}</h1>
        
        <div class="toc">
            <h2>Table of Contents</h2>
            <ul>
                <li><a href="#executive-summary">Executive Summary</a></li>
                <li><a href="#client-profile">Client Profile</a></li>
                <li><a href="#system-specifications">System Specifications</a></li>
                <li><a href="#component-justification">Component Justification</a></li>
                <li><a href="#performance-analysis">Performance Analysis</a></li>
                <li><a href="#parallel-processing">Parallel Processing Demonstration</a></li>
                <li><a href="#conclusion">Conclusion</a></li>
            </ul>
        </div>
        
        <h2 id="executive-summary">Executive Summary</h2>
        <p>This report presents a comprehensive hardware system design for <span class="highlight">{{ client.name }}</span>, a {{ client.industry }} company. The proposed system is tailored to meet the specific needs of {{ client.name }}, focusing on {{ client.primary_use_cases|join(', ') }} while staying within the budget constraint of ${{ "%.2f"|format(client.budget) }}.</p>
        
        <p>The recommended system, named <span class="highlight">{{ hardware_system.name }}</span>, has a total cost of ${{ "%.2f"|format(hardware_system.get_total_price()) }}, which is {{ 'within' if hardware_system.get_total_price() <= client.budget else 'above' }} the client's budget. This system is designed to deliver optimal performance for the client's specific workflows, with particular attention to parallel processing capabilities that can significantly reduce processing times for compute-intensive tasks.</p>
        
        <h2 id="client-profile">Client Profile</h2>
        <table>
            <tr>
                <th>Attribute</th>
                <th>Details</th>
            </tr>
            <tr>
                <td>Company Name</td>
                <td>{{ client.name }}</td>
            </tr>
            <tr>
                <td>Industry</td>
                <td>{{ client.industry }}</td>
            </tr>
            <tr>
                <td>Company Size</td>
                <td>{{ client.size }}</td>
            </tr>
            <tr>
                <td>Primary Use Cases</td>
                <td>{{ client.primary_use_cases|join(', ') }}</td>
            </tr>
            <tr>
                <td>Software Requirements</td>
                <td>{{ client.software_requirements|join(', ') }}</td>
            </tr>
            <tr>
                <td>Budget</td>
                <td>${{ "%.2f"|format(client.budget) }}</td>
            </tr>
            <tr>
                <td>Constraints</td>
                <td>{{ client.constraints|join(', ') }}</td>
            </tr>
        </table>
        
        <h3>Performance Goals</h3>
        <table>
            <tr>
                <th>Goal</th>
                <th>Target</th>
            </tr>
            {% for goal, target in client.performance_goals.items() %}
            <tr>
                <td>{{ goal.replace('_', ' ').title() }}</td>
                <td>{{ target }}</td>
            </tr>
            {% endfor %}
        </table>
        
        <h2 id="system-specifications">System Specifications</h2>
        <div class="total-price">Total System Price: ${{ "%.2f"|format(hardware_system.get_total_price()) }}</div>
        
        {% for component in hardware_system.components %}
        <div class="component-card">
            <div class="component-name">{{ component.name }}</div>
            <div class="component-price">${{ "%.2f"|format(component.price) }}</div>
            
            <h4>Specifications</h4>
            <table>
                {% for spec, value in component.specs.items() %}
                <tr>
                    <td>{{ spec.replace('_', ' ').title() }}</td>
                    <td>{{ value }}</td>
                </tr>
                {% endfor %}
            </table>
            
            <h4>Justification</h4>
            <p>{{ component.justification }}</p>
            
            <h4>Performance Impact</h4>
            <p>{{ component.performance_impact }}</p>
        </div>
        {% endfor %}
        
        <h2 id="component-justification">Component Justification</h2>
        <p>The selected components were carefully chosen to meet the specific needs of {{ client.name }}. Below is a detailed justification for each component category:</p>
        
        <h3>Processor</h3>
        <p>{{ hardware_system.get_component_by_type('CPU').justification }}</p>
        
        <h3>Graphics Processing Unit</h3>
        <p>{{ hardware_system.get_component_by_type('GPU').justification }}</p>
        
        <h3>Memory</h3>
        <p>{{ hardware_system.get_component_by_type('Memory').justification }}</p>
        
        <h3>Storage</h3>
        <p>{{ hardware_system.get_component_by_type('Primary Storage').justification }}</p>
        <p>{{ hardware_system.get_component_by_type('Secondary Storage').justification }}</p>
        
        <h3>Motherboard</h3>
        <p>{{ hardware_system.get_component_by_type('Motherboard').justification }}</p>
        
        <h3>Power Supply</h3>
        <p>{{ hardware_system.get_component_by_type('Power Supply').justification }}</p>
        
        <h3>Cooling</h3>
        <p>{{ hardware_system.get_component_by_type('CPU Cooler').justification }}</p>
        
        <h3>Case</h3>
        <p>{{ hardware_system.get_component_by_type('Case').justification }}</p>
        
        <h2 id="performance-analysis">Performance Analysis</h2>
        {% if benchmark_results %}
        <p>The following benchmarks were performed to validate the performance of the proposed system:</p>
        
        <div class="benchmark-chart">
            <img src="system_benchmark.png" alt="System Benchmark Results">
        </div>
        
        <h3>CPU Performance</h3>
        <p>The CPU benchmark demonstrates {{ hardware_system.get_component_by_type('CPU').name }}'s capability to handle intensive computations. The benchmark completed in {{ benchmark_results.cpu.execution_time }} seconds, utilizing {{ benchmark_results.cpu.cpu_count }} cores at {{ benchmark_results.cpu.cpu_freq_current }} MHz.</p>
        
        <h3>Memory Performance</h3>
        <p>The memory benchmark shows a write bandwidth of {{ "%.2f"|format(benchmark_results.memory.write_bandwidth_mb_s) }} MB/s and a read bandwidth of {{ "%.2f"|format(benchmark_results.memory.read_bandwidth_mb_s) }} MB/s, indicating excellent memory performance for data-intensive tasks.</p>
        
        <h3>Storage Performance</h3>
        <p>The storage benchmark reveals a write speed of {{ "%.2f"|format(benchmark_results.storage.write_bandwidth_mb_s) }} MB/s and a read speed of {{ "%.2f"|format(benchmark_results.storage.read_bandwidth_mb_s) }} MB/s, ensuring fast access to large files and projects.</p>
        
        {% if 'gpu' in benchmark_results and 'error' not in benchmark_results.gpu %}
        <h3>GPU Performance</h3>
        <p>The GPU benchmark achieved {{ "%.2f"|format(benchmark_results.gpu.gflops) }} GFLOPS, demonstrating the {{ hardware_system.get_component_by_type('GPU').name }}'s capability to accelerate parallel processing tasks.</p>
        {% endif %}
        
        <h3>Matrix Operations Performance</h3>
        <p>The matrix operations benchmark shows a performance of {{ "%.2f"|format(benchmark_results.matrix_operations.multiplication_gflops) }} GFLOPS for matrix multiplication, which is particularly relevant for {{ client.primary_use_cases|join(', ') }}.</p>
        {% else %}
        <p>No benchmark results were available for this system configuration.</p>
        {% endif %}
        
        <h2 id="parallel-processing">Parallel Processing Demonstration</h2>
        <p>To demonstrate how the proposed hardware can leverage parallel processing, we developed a program that performs matrix multiplication using different parallelization techniques. This demonstration is particularly relevant to {{ client.name }}'s workflows, as matrix operations are fundamental to {{ client.primary_use_cases|join(', ') }}.</p>
        
        {% if parallel_results %}
        <div class="benchmark-chart">
            <img src="matrix_multiplication_benchmark.png" alt="Matrix Multiplication Benchmark Results">
        </div>
        
        <p>The benchmark results show that parallel processing can significantly reduce computation time. With {{ parallel_results.matrix_multiplication.matrix_size }}x{{ parallel_results.matrix_multiplication.matrix_size }} matrices:</p>
        
        <ul>
            <li>Sequential execution took {{ "%.4f"|format(parallel_results.matrix_multiplication.sequential_time) }} seconds</li>
            <li>NumPy's optimized implementation took {{ "%.4f"|format(parallel_results.matrix_multiplication.numpy_time) }} seconds</li>
        </ul>
        
        <p>This demonstrates how the {{ hardware_system.get_component_by_type('CPU').name }}'s multiple cores can be effectively utilized to accelerate compute-intensive tasks, resulting in significant time savings for {{ client.name }}'s workflows.</p>
        {% else %}
        <p>No parallel processing results were available for this demonstration.</p>
        {% endif %}
        
        <h3>Code Implementation</h3>
        <div class="code-block">
# Sequential matrix multiplication
def sequential_matrix_multiply(a, b):
    start_time = time.time()
    result = np.zeros((a.shape[0], b.shape[1]))
    
    for i in range(a.shape[0]):
        for j in range(b.shape[1]):
            for k in range(a.shape[1]):
                result[i, j] += a[i, k] * b[k, j]
    
    end_time = time.time()
    return result, end_time - start_time

# Parallel matrix multiplication using multiprocessing
def multiprocessing_matrix_multiply(a, b, num_processes=None):
    if num_processes is None:
        num_processes = mp.cpu_count()
    
    start_time = time.time()
    
    # Divide matrix A into chunks for each process
    chunk_size = a.shape[0] // num_processes
    chunks = []
    
    for i in range(num_processes):
        start_row = i * chunk_size
        end_row = (i + 1) * chunk_size if i < num_processes - 1 else a.shape[0]
        a_chunk = a[start_row:end_row]
        chunks.append((a_chunk, b, start_row, end_row))
    
    # Create a pool of workers and process chunks in parallel
    with Pool(processes=num_processes) as pool:
        results = pool.map(matrix_multiply_chunk, chunks)
    
    # Combine results
    result = np.zeros((a.shape[0], b.shape[1]))
    for chunk_result, start_row, end_row in results:
        result[start_row:end_row] = chunk_result
    
    end_time = time.time()
    return result, end_time - start_time
        </div>
        
        <h2 id="conclusion">Conclusion</h2>
        <p>The proposed hardware system for {{ client.name }} is designed to meet the specific needs of {{ client.industry }} workflows. The system balances performance, reliability, and cost-effectiveness, providing a solid foundation for {{ client.primary_use_cases|join(', ') }}.</p>
        
        <p>The parallel processing capabilities of the {{ hardware_system.get_component_by_type('CPU').name }} and {{ hardware_system.get_component_by_type('GPU').name }} will significantly reduce processing times for compute-intensive tasks, improving productivity and workflow efficiency.</p>
        
        <p>The system is also designed with future expandability in mind, allowing for upgrades as technology advances and the client's needs evolve.</p>
        
        <div class="footer">
            <p>Report generated on {{ report_date }} by Hardware System Design Consultant</p>
        </div>
    </div>
</body>
</html>
        """
        
        # Create template
        template = Template(template_str)
        
        # Render template with data
        html_content = template.render(
            client=self.client,
            hardware_system=self.hardware_system,
            benchmark_results=self.benchmark_results,
            parallel_results=self.parallel_results,
            report_date=self.report_date
        )
        
        # Write to file
        with open(output_path, 'w') as f:
            f.write(html_content)
        
        print(f"HTML report generated: {output_path}")
    
    def generate_markdown_report(self, output_path: str = "hardware_system_report.md") -> None:
        """
        Generate a Markdown report
        
        Args:
            output_path (str): Path to save the Markdown report
        """
        # Markdown template
        template_str = """
# Hardware System Design Report for {{ client.name }}

**Report Date:** {{ report_date }}  
**Client:** {{ client.name }}  
**Industry:** {{ client.industry }}  

## Executive Summary

This report presents a comprehensive hardware system design for {{ client.name }}, a {{ client.industry }} company. The proposed system is tailored to meet the specific needs of {{ client.name }}, focusing on {{ client.primary_use_cases|join(', ') }} while staying within the budget constraint of ${{ "%.2f"|format(client.budget) }}.

The recommended system, named **{{ hardware_system.name }}**, has a total cost of ${{ "%.2f"|format(hardware_system.get_total_price()) }}, which is {{ 'within' if hardware_system.get_total_price() <= client.budget else 'above' }} the client's budget. This system is designed to deliver optimal performance for the client's specific workflows, with particular attention to parallel processing capabilities that can significantly reduce processing times for compute-intensive tasks.

## Client Profile

| Attribute | Details |
|-----------|---------|
| Company Name | {{ client.name }} |
| Industry | {{ client.industry }} |
| Company Size | {{ client.size }} |
| Primary Use Cases | {{ client.primary_use_cases|join(', ') }} |
| Software Requirements | {{ client.software_requirements|join(', ') }} |
| Budget | ${{ "%.2f"|format(client.budget) }} |
| Constraints | {{ client.constraints|join(', ') }} |

### Performance Goals

| Goal | Target |
|------|--------|
{% for goal, target in client.performance_goals.items() %}
| {{ goal.replace('_', ' ').title() }} | {{ target }} |
{% endfor %}

## System Specifications

**Total System Price:** ${{ "%.2f"|format(hardware_system.get_total_price()) }}

{% for component in hardware_system.components %}
### {{ component.component_type }}: {{ component.name }}

**Price:** ${{ "%.2f"|format(component.price) }}

#### Specifications
{% for spec, value in component.specs.items() %}
- **{{ spec.replace('_', ' ').title() }}:** {{ value }}
{% endfor %}

#### Justification
{{ component.justification }}

#### Performance Impact
{{ component.performance_impact }}

{% endfor %}

## Component Justification

The selected components were carefully chosen to meet the specific needs of {{ client.name }}. Below is a detailed justification for each component category:

### Processor
{{ hardware_system.get_component_by_type('CPU').justification }}

### Graphics Processing Unit
{{ hardware_system.get_component_by_type('GPU').justification }}

### Memory
{{ hardware_system.get_component_by_type('Memory').justification }}

### Storage
{{ hardware_system.get_component_by_type('Primary Storage').justification }}

{{ hardware_system.get_component_by_type('Secondary Storage').justification }}

### Motherboard
{{ hardware_system.get_component_by_type('Motherboard').justification }}

### Power Supply
{{ hardware_system.get_component_by_type('Power Supply').justification }}

### Cooling
{{ hardware_system.get_component_by_type('CPU Cooler').justification }}

### Case
{{ hardware_system.get_component_by_type('Case').justification }}

## Performance Analysis

{% if benchmark_results %}
The following benchmarks were performed to validate the performance of the proposed system:

![System Benchmark Results](system_benchmark.png)

### CPU Performance
The CPU benchmark demonstrates {{ hardware_system.get_component_by_type('CPU').name }}'s capability to handle intensive computations. The benchmark completed in {{ benchmark_results.cpu.execution_time }} seconds, utilizing {{ benchmark_results.cpu.cpu_count }} cores at {{ benchmark_results.cpu.cpu_freq_current }} MHz.

### Memory Performance
The memory benchmark shows a write bandwidth of {{ "%.2f"|format(benchmark_results.memory.write_bandwidth_mb_s) }} MB/s and a read bandwidth of {{ "%.2f"|format(benchmark_results.memory.read_bandwidth_mb_s) }} MB/s, indicating excellent memory performance for data-intensive tasks.

### Storage Performance
The storage benchmark reveals a write speed of {{ "%.2f"|format(benchmark_results.storage.write_bandwidth_mb_s) }} MB/s and a read speed of {{ "%.2f"|format(benchmark_results.storage.read_bandwidth_mb_s) }} MB/s, ensuring fast access to large files and projects.

{% if 'gpu' in benchmark_results and 'error' not in benchmark_results.gpu %}
### GPU Performance
The GPU benchmark achieved {{ "%.2f"|format(benchmark_results.gpu.gflops) }} GFLOPS, demonstrating the {{ hardware_system.get_component_by_type('GPU').name }}'s capability to accelerate parallel processing tasks.
{% endif %}

### Matrix Operations Performance
The matrix operations benchmark shows a performance of {{ "%.2f"|format(benchmark_results.matrix_operations.multiplication_gflops) }} GFLOPS for matrix multiplication, which is particularly relevant for {{ client.primary_use_cases|join(', ') }}.
{% else %}
No benchmark results were available for this system configuration.
{% endif %}

## Parallel Processing Demonstration

To demonstrate how the proposed hardware can leverage parallel processing, we developed a program that performs matrix multiplication using different parallelization techniques. This demonstration is particularly relevant to {{ client.name }}'s workflows, as matrix operations are fundamental to {{ client.primary_use_cases|join(', ') }}.

{% if parallel_results %}
![Matrix Multiplication Benchmark Results](matrix_multiplication_benchmark.png)

The benchmark results show that parallel processing can significantly reduce computation time. With {{ parallel_results.matrix_multiplication.matrix_size }}x{{ parallel_results.matrix_multiplication.matrix_size }} matrices:

- Sequential execution took {{ "%.4f"|format(parallel_results.matrix_multiplication.sequential_time) }} seconds
- NumPy's optimized implementation took {{ "%.4f"|format(parallel_results.matrix_multiplication.numpy_time) }} seconds

This demonstrates how the {{ hardware_system.get_component_by_type('CPU').name }}'s multiple cores can be effectively utilized to accelerate compute-intensive tasks, resulting in significant time savings for {{ client.name }}'s workflows.
{% else %}
No parallel processing results were available for this demonstration.
{% endif %}

### Code Implementation

```python
# Sequential matrix multiplication
def sequential_matrix_multiply(a, b):
    start_time = time.time()
    result = np.zeros((a.shape[0], b.shape[1]))
    
    for i in range(a.shape[0]):
        for j in range(b.shape[1]):
            for k in range(a.shape[1]):
                result[i, j] += a[i, k] * b[k, j]
    
    end_time = time.time()
    return result, end_time - start_time

# Parallel matrix multiplication using multiprocessing
def multiprocessing_matrix_multiply(a, b, num_processes=None):
    if num_processes is None:
        num_processes = mp.cpu_count()
    
    start_time = time.time()
    
    # Divide matrix A into chunks for each process
    chunk_size = a.shape[0] // num_processes
    chunks = []
    
    for i in range(num_processes):
        start_row = i * chunk_size
        end_row = (i + 1) * chunk_size if i < num_processes - 1 else a.shape[0]
        a_chunk = a[start_row:end_row]
        chunks.append((a_chunk, b, start_row, end_row))
    
    # Create a pool of workers and process chunks in parallel
    with Pool(processes=num_processes) as pool:
        results = pool.map(matrix_multiply_chunk, chunks)
    
    # Combine results
    result = np.zeros((a.shape[0], b.shape[1]))
    for chunk_result, start_row, end_row in results:
        result[start_row:end_row] = chunk_result
    
    end_time = time.time()
    return result, end_time - start_time
        """
