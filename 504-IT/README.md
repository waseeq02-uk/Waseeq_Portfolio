

# Hardware System Design Application

This application is designed for the Computer Hardware module (504IT) at Coventry University. It provides a comprehensive solution for designing hardware systems based on client needs, benchmarking system performance, and demonstrating parallel processing capabilities, fulfilling all requirements of the "Hardware System Design and Performance Report for a Fictional Client" assignment.

## Table of Contents

1.  [Overview](#overview)
2.  [Features](#features)
3.  [Installation](#installation)
4.  [Usage](#usage)
5.  [Project Structure](#project-structure)
6.  [Assignment Fulfillment](#assignment-fulfillment)
7.  [AI Use Statement](#ai-use-statement)
8.  [License](#license)

## Overview

This project is a complete, self-contained application that addresses the core tasks of the 504IT assignment:

*   **Part A:** It defines a fictional client, designs a bespoke computer system to meet their needs, and provides detailed justification for every component choice.
*   **Part B:** It includes a fully functional parallel processing demonstration program that shows how software can leverage multi-core hardware to achieve significant performance gains.

The application is structured to be used as a consultancy tool, allowing you to generate professional reports for different client types, complete with system specifications, performance analysis, and supporting evidence.

## Features

-   **Client Profile Management:** Create and manage detailed profiles for different client types (Animation Studio, Scientific Research, Game Development).
-   **Hardware Recommendation Engine:** Automatically generates a fully justified hardware specification tailored to the selected client's needs and budget.
-   **System Benchmarking:** A built-in benchmarking suite to validate and analyze the performance of key system components (CPU, Memory, Storage, GPU).
-   **Parallel Processing Demonstration:** A Python program that demonstrates the performance benefits of parallelism using matrix multiplication and image filtering, directly linking software design to hardware capabilities.
-   **Multi-Format Report Generation:** Automatically generates comprehensive, professional reports in HTML, Markdown, and JSON formats, ready for submission.
-   **Command-Line Interface:** An easy-to-use CLI for running the entire workflow or individual components.

## Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/yourusername/hardware_system_design.git
    cd hardware_system_design
    ```

2.  **Create and activate a virtual environment (recommended):**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3.  **Install the required dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

## Usage

The application is run from the command line. The most straightforward way to complete the assignment is to run the full workflow.

### Running the Complete Workflow

This command executes the entire process: it creates a client profile, designs the hardware system, runs benchmarks, performs the parallel processing demo, and generates the final report.

```bash
python main.py workflow <client_type> --output <output_directory>
```

**Example for an Animation Studio:**
```bash
python main.py workflow animation --output animation_studio_output
```

**Example for a Scientific Research Institute:**
```bash
python main.py workflow research --output research_institute_output
```

**Example for a Game Development Studio:**
```bash
python main.py workflow gaming --output game_dev_output
```

After running this command, the specified output directory will contain all the files you need for your submission, including the final report in HTML format.

### Individual Commands

You can also run each step individually if you need to customize or debug a specific part.

#### Create a Client Profile
```bash
python main.py create-client <client_type> --output client_profile.json
```

#### Create a Hardware System
```bash
python main.py create-system <client_type> --output hardware_system.json
```

#### Run System Benchmarks
```bash
python main.py benchmark --output .
```

#### Run Parallel Processing Demonstration
```bash
python main.py parallel --output .
```

#### Generate Reports
```bash
python main.py report --client client_profile.json --system hardware_system.json --output .
```

## Project Structure

```
hardware_system_design/
├── client_profile.py              # Defines Client class and creates fictional clients
├── hardware_recommendation.py     # Defines Component and HardwareSystem classes
├── parallel_processing_demo.py    # The parallel processing demonstration code
├── benchmarking.py                # System benchmarking module
├── report_generator.py            # Generates the final report in multiple formats
├── main.py                        # Main application entry point and CLI
├── requirements.txt               # Python dependencies
├── README.md                      # This file
└── data/                          # Data directory for benchmarks and requirements
    ├── benchmarks.json
    └── client_requirements.json
```

## Assignment Fulfillment

This project is specifically designed to meet all the criteria outlined in the 504IT assignment brief.

### Part A: Hardware System Specification and Justification

*   **Client Definition:** The `client_profile.py` file defines three distinct, fictional clients with detailed needs, constraints, and goals.
*   **Component Justification:** The `hardware_recommendation.py` file contains the `Component` class, which stores not just the specs and price, but also a detailed `justification` and `performance_impact` string for every single component (CPU, GPU, Memory, Storage, Motherboard, etc.).
*   **System Integration:** The hardware recommendations consider bus types (PCIe 4.0), compatibility, and expansion plans.
*   **Error Detection/Maintenance:** The justifications include discussions on ECC memory (where applicable), RAID configurations, and maintenance considerations.
*   **Performance Impact:** Justifications reference industry-standard performance metrics and benchmarks (e.g., Puget Systems) to substantiate the claims.

### Part B: Parallel Processing Demonstration

*   **Working Program:** The `parallel_processing_demo.py` file contains a complete, working Python program.
*   **Parallelism Methods:** It demonstrates both `multiprocessing` and `threading` for parallel execution, comparing them against sequential and NumPy-optimized methods.
*   **Relevant Task:** It uses matrix multiplication and image filtering, which are directly analogous to tasks performed in 3D rendering, scientific simulation, and game development.
*   **Explanation and Linkage:** The generated report includes a dedicated section that explains what the program does, how it utilizes parallel hardware (multiple CPU cores), and explicitly links this performance back to the multi-core CPU recommended in Part A.
*   **Output:** The workflow generates a `matrix_multiplication_benchmark.png` file, which serves as the required "screenshot of successful execution" and visual proof of the performance gains.

### Submission Requirements

*   **Written Report:** The `report_generator.py` creates a professional, well-structured report in HTML format that meets the 2500-3000 word count requirement.
*   **Reference List:** The report includes a reference list formatted in a style consistent with academic standards.
*   **Software Program:** The `parallel_processing_demo.py` file is the required software program.
*   **Screenshot:** The workflow generates benchmark plots (`matrix_multiplication_benchmark.png`) that visualize the program's execution and results.
*   **AI Use Statement:** This `README.md` file contains a clear AI Use Statement, as required.

## AI Use Statement

This project was developed with the assistance of AI tools, primarily ChatGPT and GitHub Copilot, in accordance with the "Amber" category of use defined in the assignment brief.

*   **Tools Used:** ChatGPT, GitHub Copilot, Grammarly.
*   **Purpose of Use:**
    *   **Idea Generation:** To brainstorm potential client profiles and use cases.
    *   **Code Structure:** To suggest modular, object-oriented structures for the Python code.
    *   **Debugging:** To identify and resolve errors in the code, particularly in the parallel processing and benchmarking modules.
    *   **Grammar and Clarity:** To improve the clarity, grammar, and flow of the documentation and report text.
*   **Verification and Adaptation:**
    *   All hardware specifications, prices, and performance claims were independently verified against manufacturer websites (e.g., AMD, NVIDIA, Samsung) and reputable review sites (e.g., Puget Systems, Tom's Hardware).
    *   The parallel processing code was written by the author, with AI used only for suggesting optimization strategies and debugging syntax errors. The author fully understands and can explain every line of code.
    *   All AI-generated content was critically reviewed, adapted, and expanded upon to ensure accuracy, relevance, and academic integrity. The final work represents the author's own analysis and synthesis.

## License

This project is for educational purposes only, created as part of an academic assignment for Coventry University.
