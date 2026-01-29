"""
Benchmarking Module
Provides benchmarking capabilities for hardware components
"""

import time
import psutil
import platform
import cpuinfo
import GPUtil
import json
import os
import matplotlib.pyplot as plt
from typing import Dict, List, Tuple, Any
import numpy as np


class SystemBenchmark:
    """Class to benchmark system performance"""
    
    def __init__(self):
        """Initialize the system benchmark"""
        self.results = {}
        self.system_info = self._get_system_info()
    
    def _get_system_info(self) -> Dict[str, Any]:
        """
        Get information about the system
        
        Returns:
            Dict[str, Any]: System information
        """
        info = {
            'platform': platform.platform(),
            'processor': platform.processor(),
            'architecture': platform.architecture()[0],
            'ram': f"{psutil.virtual_memory().total / (1024 ** 3):.2f} GB",
            'cpu_info': cpuinfo.get_cpu_info(),
            'gpu_info': []
        }
        
        # Get GPU information
        try:
            gpus = GPUtil.getGPUs()
            for gpu in gpus:
                info['gpu_info'].append({
                    'name': gpu.name,
                    'memory': f"{gpu.memoryTotal} MB",
                    'driver': gpu.driver
                })
        except:
            info['gpu_info'] = ['Could not retrieve GPU information']
        
        return info
    
    def benchmark_cpu(self, duration: int = 10) -> Dict[str, Any]:
        """
        Benchmark CPU performance
        
        Args:
            duration (int): Duration of the benchmark in seconds
            
        Returns:
            Dict[str, Any]: CPU benchmark results
        """
        print(f"Benchmarking CPU performance for {duration} seconds...")
        
        # Get initial CPU usage
        initial_cpu_percent = psutil.cpu_percent(interval=1)
        
        # Perform CPU-intensive task
        start_time = time.time()
        result = 0
        
        while time.time() - start_time < duration:
            # Perform some calculations
            for i in range(1000000):
                result += i ** 2
        
        end_time = time.time()
        execution_time = end_time - start_time
        
        # Get CPU information
        cpu_info = cpuinfo.get_cpu_info()
        cpu_count = psutil.cpu_count()
        cpu_freq = psutil.cpu_freq()
        
        # Get CPU usage during benchmark
        cpu_percent = psutil.cpu_percent(interval=1)
        
        # Store results
        results = {
            'execution_time': execution_time,
            'result': result,
            'cpu_count': cpu_count,
            'cpu_freq_current': cpu_freq.current if cpu_freq else 'Unknown',
            'cpu_freq_max': cpu_freq.max if cpu_freq else 'Unknown',
            'cpu_percent': cpu_percent,
            'cpu_brand': cpu_info.get('brand_raw', 'Unknown'),
            'cpu_architecture': cpu_info.get('arch', 'Unknown'),
            'cpu_cache': cpu_info.get('l3_cache_size', 'Unknown')
        }
        
        self.results['cpu'] = results
        return results
    
    def benchmark_memory(self, size_mb: int = 1000) -> Dict[str, Any]:
        """
        Benchmark memory performance
        
        Args:
            size_mb (int): Size of the memory block to test in MB
            
        Returns:
            Dict[str, Any]: Memory benchmark results
        """
        print(f"Benchmarking memory performance with {size_mb}MB block...")
        
        # Get initial memory information
        virtual_memory = psutil.virtual_memory()
        swap_memory = psutil.swap_memory()
        
        # Create a large array
        size = size_mb * 1024 * 1024 // 8  # Convert MB to number of 64-bit floats
        array = np.zeros(size, dtype=np.float64)
        
        # Write to memory
        start_time = time.time()
        for i in range(len(array)):
            array[i] = i
        write_time = time.time() - start_time
        
        # Read from memory
        start_time = time.time()
        result = 0
        for i in range(len(array)):
            result += array[i]
        read_time = time.time() - start_time
        
        # Get memory information after benchmark
        virtual_memory_after = psutil.virtual_memory()
        swap_memory_after = psutil.swap_memory()
        
        # Calculate memory bandwidth
        write_bandwidth = (size_mb * 2) / write_time  # MB/s (read and write)
        read_bandwidth = (size_mb * 2) / read_time    # MB/s (read and write)
        
        # Store results
        results = {
            'size_mb': size_mb,
            'write_time': write_time,
            'read_time': read_time,
            'write_bandwidth_mb_s': write_bandwidth,
            'read_bandwidth_mb_s': read_bandwidth,
            'total_memory_gb': virtual_memory.total / (1024 ** 3),
            'available_memory_gb': virtual_memory.available / (1024 ** 3),
            'memory_percent_before': virtual_memory.percent,
            'memory_percent_after': virtual_memory_after.percent,
            'swap_total_gb': swap_memory.total / (1024 ** 3),
            'swap_used_gb': swap_memory.used / (1024 ** 3),
            'swap_percent_before': swap_memory.percent,
            'swap_percent_after': swap_memory_after.percent
        }
        
        self.results['memory'] = results
        return results
    
    def benchmark_storage(self, file_size_mb: int = 1000, file_path: str = 'benchmark_file.tmp') -> Dict[str, Any]:
        """
        Benchmark storage performance
        
        Args:
            file_size_mb (int): Size of the test file in MB
            file_path (str): Path to the test file
            
        Returns:
            Dict[str, Any]: Storage benchmark results
        """
        print(f"Benchmarking storage performance with {file_size_mb}MB file...")
        
        # Generate random data
        data = os.urandom(file_size_mb * 1024 * 1024)
        
        # Write test
        start_time = time.time()
        with open(file_path, 'wb') as f:
            f.write(data)
        write_time = time.time() - start_time
        
        # Read test
        start_time = time.time()
        with open(file_path, 'rb') as f:
            read_data = f.read()
        read_time = time.time() - start_time
        
        # Verify data integrity
        data_integrity = data == read_data
        
        # Calculate storage bandwidth
        write_bandwidth = file_size_mb / write_time  # MB/s
        read_bandwidth = file_size_mb / read_time    # MB/s
        
        # Get disk information
        disk_usage = psutil.disk_usage('/')
        disk_io = psutil.disk_io_counters()
        
        # Clean up
        os.remove(file_path)
        
        # Store results
        results = {
            'file_size_mb': file_size_mb,
            'write_time': write_time,
            'read_time': read_time,
            'write_bandwidth_mb_s': write_bandwidth,
            'read_bandwidth_mb_s': read_bandwidth,
            'data_integrity': data_integrity,
            'disk_total_gb': disk_usage.total / (1024 ** 3),
            'disk_used_gb': disk_usage.used / (1024 ** 3),
            'disk_free_gb': disk_usage.free / (1024 ** 3),
            'disk_percent': disk_usage.percent,
            'disk_read_count': disk_io.read_count if disk_io else 'Unknown',
            'disk_write_count': disk_io.write_count if disk_io else 'Unknown',
            'disk_read_bytes': disk_io.read_bytes if disk_io else 'Unknown',
            'disk_write_bytes': disk_io.write_bytes if disk_io else 'Unknown'
        }
        
        self.results['storage'] = results
        return results
    
    def benchmark_gpu(self, duration: int = 10) -> Dict[str, Any]:
        """
        Benchmark GPU performance
        
        Args:
            duration (int): Duration of the benchmark in seconds
            
        Returns:
            Dict[str, Any]: GPU benchmark results
        """
        print(f"Benchmarking GPU performance for {duration} seconds...")
        
        try:
            import torch
            
            # Check if CUDA is available
            if not torch.cuda.is_available():
                return {'error': 'CUDA is not available'}
            
            # Get GPU information
            device = torch.device('cuda')
            gpu_name = torch.cuda.get_device_name(0)
            gpu_memory = torch.cuda.get_device_properties(0).total_memory / (1024 ** 3)  # GB
            
            # Create tensors
            size = 5000
            a = torch.randn(size, size, device=device)
            b = torch.randn(size, size, device=device)
            
            # Warm up GPU
            for _ in range(5):
                _ = torch.mm(a, b)
            torch.cuda.synchronize()
            
            # Benchmark GPU matrix multiplication
            start_time = time.time()
            iterations = 0
            
            while time.time() - start_time < duration:
                c = torch.mm(a, b)
                torch.cuda.synchronize()
                iterations += 1
            
            end_time = time.time()
            execution_time = end_time - start_time
            
            # Calculate performance metrics
            flops_per_iteration = 2 * size ** 3  # 2 * N^3 for matrix multiplication
            total_flops = flops_per_iteration * iterations
            gflops = total_flops / (execution_time * 10 ** 9)
            
            # Get GPU memory usage
            gpu_memory_used = torch.cuda.memory_allocated() / (1024 ** 3)  # GB
            gpu_memory_percent = (gpu_memory_used / gpu_memory) * 100
            
            # Store results
            results = {
                'execution_time': execution_time,
                'iterations': iterations,
                'gflops': gflops,
                'gpu_name': gpu_name,
                'gpu_memory_total_gb': gpu_memory,
                'gpu_memory_used_gb': gpu_memory_used,
                'gpu_memory_percent': gpu_memory_percent,
                'matrix_size': size
            }
            
            self.results['gpu'] = results
            return results
            
        except ImportError:
            return {'error': 'PyTorch is not installed'}
        except Exception as e:
            return {'error': str(e)}
    
    def benchmark_matrix_operations(self, size: int = 1000) -> Dict[str, Any]:
        """
        Benchmark matrix operations using NumPy
        
        Args:
            size (int): Size of the square matrices
            
        Returns:
            Dict[str, Any]: Matrix operations benchmark results
        """
        print(f"Benchmarking matrix operations with {size}x{size} matrices...")
        
        # Create random matrices
        a = np.random.rand(size, size)
        b = np.random.rand(size, size)
        
        # Matrix multiplication
        start_time = time.time()
        c = np.dot(a, b)
        multiplication_time = time.time() - start_time
        
        # Matrix inversion
        start_time = time.time()
        try:
            a_inv = np.linalg.inv(a)
            inversion_time = time.time() - start_time
            inversion_success = True
        except np.linalg.LinAlgError:
            inversion_time = float('inf')
            inversion_success = False
        
        # Eigenvalue decomposition
        start_time = time.time()
        try:
            eigenvalues, eigenvectors = np.linalg.eig(a)
            eigenvalue_time = time.time() - start_time
            eigenvalue_success = True
        except np.linalg.LinAlgError:
            eigenvalue_time = float('inf')
            eigenvalue_success = False
        
        # Singular value decomposition
        start_time = time.time()
        u, s, vh = np.linalg.svd(a)
        svd_time = time.time() - start_time
        
        # Store results
        results = {
            'matrix_size': size,
            'multiplication_time': multiplication_time,
            'multiplication_gflops': (2 * size ** 3) / (multiplication_time * 10 ** 9),
            'inversion_time': inversion_time,
            'inversion_success': inversion_success,
            'eigenvalue_time': eigenvalue_time,
            'eigenvalue_success': eigenvalue_success,
            'svd_time': svd_time,
            'svd_gflops': (20 * size ** 3) / (svd_time * 10 ** 9)  # Approximate FLOPS for SVD
        }
        
        self.results['matrix_operations'] = results
        return results
    
    def run_all_benchmarks(self) -> Dict[str, Any]:
        """
        Run all benchmarks
        
        Returns:
            Dict[str, Any]: All benchmark results
        """
        print("Running all benchmarks...")
        print("=" * 50)
        
        # CPU benchmark
        cpu_results = self.benchmark_cpu()
        print(f"CPU benchmark completed in {cpu_results['execution_time']:.2f} seconds")
        print()
        
        # Memory benchmark
        memory_results = self.benchmark_memory()
        print(f"Memory benchmark completed")
        print(f"Write bandwidth: {memory_results['write_bandwidth_mb_s']:.2f} MB/s")
        print(f"Read bandwidth: {memory_results['read_bandwidth_mb_s']:.2f} MB/s")
        print()
        
        # Storage benchmark
        storage_results = self.benchmark_storage()
        print(f"Storage benchmark completed")
        print(f"Write bandwidth: {storage_results['write_bandwidth_mb_s']:.2f} MB/s")
        print(f"Read bandwidth: {storage_results['read_bandwidth_mb_s']:.2f} MB/s")
        print()
        
        # GPU benchmark
        gpu_results = self.benchmark_gpu()
        if 'error' not in gpu_results:
            print(f"GPU benchmark completed")
            print(f"Performance: {gpu_results['gflops']:.2f} GFLOPS")
        else:
            print(f"GPU benchmark failed: {gpu_results['error']}")
        print()
        
        # Matrix operations benchmark
        matrix_results = self.benchmark_matrix_operations()
        print(f"Matrix operations benchmark completed")
        print(f"Matrix multiplication: {matrix_results['multiplication_gflops']:.2f} GFLOPS")
        print()
        
        return self.results
    
    def save_results(self, filepath: str) -> None:
        """
        Save benchmark results to a file
        
        Args:
            filepath (str): Path to save the results
        """
        # Convert numpy arrays to lists for JSON serialization
        json_results = {
            'system_info': self.system_info,
            'benchmark_results': {}
        }
        
        for key, value in self.results.items():
            json_results['benchmark_results'][key] = {}
            for sub_key, sub_value in value.items():
                if isinstance(sub_value, np.ndarray):
                    json_results['benchmark_results'][key][sub_key] = sub_value.tolist()
                else:
                    json_results['benchmark_results'][key][sub_key] = sub_value
        
        with open(filepath, 'w') as f:
            json.dump(json_results, f, indent=4)
        
        print(f"Results saved to {filepath}")
    
    def plot_results(self) -> None:
        """Plot benchmark results"""
        if not self.results:
            print("No benchmark results to plot")
            return
        
        # Create figure with subplots
        fig, axes = plt.subplots(2, 3, figsize=(15, 10))
        
        # CPU benchmark
        if 'cpu' in self.results:
            cpu_data = self.results['cpu']
            cpu_labels = ['Execution Time', 'CPU Count', 'CPU %', 'CPU Freq (GHz)']
            cpu_values = [
                cpu_data['execution_time'],
                cpu_data['cpu_count'],
                cpu_data['cpu_percent'],
                cpu_data['cpu_freq_current'] / 1000 if isinstance(cpu_data['cpu_freq_current'], (int, float)) else 0
            ]
            
            axes[0, 0].bar(cpu_labels, cpu_values)
            axes[0, 0].set_title('CPU Benchmark')
            axes[0, 0].set_ylabel('Value')
            
            # Rotate x-axis labels
            for tick in axes[0, 0].get_xticklabels():
                tick.set_rotation(45)
        
        # Memory benchmark
        if 'memory' in self.results:
            memory_data = self.results['memory']
            memory_labels = ['Write Bandwidth', 'Read Bandwidth', 'Memory %']
            memory_values = [
                memory_data['write_bandwidth_mb_s'],
                memory_data['read_bandwidth_mb_s'],
                memory_data['memory_percent_after']
            ]
            
            axes[0, 1].bar(memory_labels, memory_values)
            axes[0, 1].set_title('Memory Benchmark')
            axes[0, 1].set_ylabel('Value')
            
            # Rotate x-axis labels
            for tick in axes[0, 1].get_xticklabels():
                tick.set_rotation(45)
        
        # Storage benchmark
        if 'storage' in self.results:
            storage_data = self.results['storage']
            storage_labels = ['Write Bandwidth', 'Read Bandwidth', 'Disk %']
            storage_values = [
                storage_data['write_bandwidth_mb_s'],
                storage_data['read_bandwidth_mb_s'],
                storage_data['disk_percent']
            ]
            
            axes[0, 2].bar(storage_labels, storage_values)
            axes[0, 2].set_title('Storage Benchmark')
            axes[0, 2].set_ylabel('Value')
            
            # Rotate x-axis labels
            for tick in axes[0, 2].get_xticklabels():
                tick.set_rotation(45)
        
        # GPU benchmark
        if 'gpu' in self.results and 'error' not in self.results['gpu']:
            gpu_data = self.results['gpu']
            gpu_labels = ['GFLOPS', 'GPU Memory %', 'Iterations']
            gpu_values = [
                gpu_data['gflops'],
                gpu_data['gpu_memory_percent'],
                gpu_data['iterations']
            ]
            
            axes[1, 0].bar(gpu_labels, gpu_values)
            axes[1, 0].set_title('GPU Benchmark')
            axes[1, 0].set_ylabel('Value')
            
            # Rotate x-axis labels
            for tick in axes[1, 0].get_xticklabels():
                tick.set_rotation(45)
        else:
            axes[1, 0].text(0.5, 0.5, 'GPU Benchmark\nNot Available', 
                            horizontalalignment='center', verticalalignment='center',
                            transform=axes[1, 0].transAxes)
            axes[1, 0].set_title('GPU Benchmark')
        
        # Matrix operations benchmark
        if 'matrix_operations' in self.results:
            matrix_data = self.results['matrix_operations']
            matrix_labels = ['Multiplication GFLOPS', 'Inversion Time', 'Eigenvalue Time', 'SVD GFLOPS']
            matrix_values = [
                matrix_data['multiplication_gflops'],
                matrix_data['inversion_time'] if matrix_data['inversion_time'] != float('inf') else 0,
                matrix_data['eigenvalue_time'] if matrix_data['eigenvalue_time'] != float('inf') else 0,
                matrix_data['svd_gflops']
            ]
            
            axes[1, 1].bar(matrix_labels, matrix_values)
            axes[1, 1].set_title('Matrix Operations Benchmark')
            axes[1, 1].set_ylabel('Value')
            
            # Rotate x-axis labels
            for tick in axes[1, 1].get_xticklabels():
                tick.set_rotation(45)
        
        # System information
        axes[1, 2].axis('off')
        system_info_text = f"Platform: {self.system_info['platform']}\n"
        system_info_text += f"RAM: {self.system_info['ram']}\n"
        
        if 'brand_raw' in self.system_info['cpu_info']:
            system_info_text += f"CPU: {self.system_info['cpu_info']['brand_raw']}\n"
        
        if self.system_info['gpu_info'] and 'name' in self.system_info['gpu_info'][0]:
            system_info_text += f"GPU: {self.system_info['gpu_info'][0]['name']}\n"
        
        axes[1, 2].text(0.1, 0.9, system_info_text, 
                        horizontalalignment='left', verticalalignment='top',
                        transform=axes[1, 2].transAxes)
        axes[1, 2].set_title('System Information')
        
        # Adjust layout
        plt.tight_layout()
        
        # Save figure
        plt.savefig('system_benchmark.png')
        print("Benchmark plot saved as 'system_benchmark.png'")
        
        # Show plot
        plt.show()


def main():
    """Main function to run the system benchmark"""
    print("System Benchmark")
    print("================")
    
    # Create benchmark instance
    benchmark = SystemBenchmark()
    
    # Run all benchmarks
    results = benchmark.run_all_benchmarks()
    
    # Save results
    benchmark.save_results('system_benchmark_results.json')
    
    # Plot results
    benchmark.plot_results()
    
    print("System benchmark completed.")
    print("Generated files:")
    print("- system_benchmark.png")
    print("- system_benchmark_results.json")


if __name__ == "__main__":
    main()