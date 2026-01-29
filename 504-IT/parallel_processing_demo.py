"""
Parallel Processing Demonstration Module
Demonstrates how software can use parallel processing to maximize performance
"""

import numpy as np
import time
import multiprocessing as mp
from multiprocessing import Pool
import matplotlib.pyplot as plt
import os
import threading
import concurrent.futures
from typing import Tuple, List, Callable, Any


class ParallelProcessingDemo:
    """Class to demonstrate parallel processing capabilities"""
    
    def __init__(self):
        """Initialize the parallel processing demo"""
        self.results = {}
        self.figures = {}
    
    def sequential_matrix_multiply(self, a: np.ndarray, b: np.ndarray) -> Tuple[np.ndarray, float]:
        """
        Perform sequential matrix multiplication
        
        Args:
            a (np.ndarray): First matrix
            b (np.ndarray): Second matrix
            
        Returns:
            Tuple[np.ndarray, float]: Result matrix and execution time
        """
        start_time = time.time()
        result = np.zeros((a.shape[0], b.shape[1]))
        
        for i in range(a.shape[0]):
            for j in range(b.shape[1]):
                for k in range(a.shape[1]):
                    result[i, j] += a[i, k] * b[k, j]
        
        end_time = time.time()
        return result, end_time - start_time
    
    def numpy_matrix_multiply(self, a: np.ndarray, b: np.ndarray) -> Tuple[np.ndarray, float]:
        """
        Perform matrix multiplication using NumPy's optimized function
        
        Args:
            a (np.ndarray): First matrix
            b (np.ndarray): Second matrix
            
        Returns:
            Tuple[np.ndarray, float]: Result matrix and execution time
        """
        start_time = time.time()
        result = np.dot(a, b)
        end_time = time.time()
        return result, end_time - start_time
    
    def _matrix_multiply_chunk(self, args: Tuple) -> Tuple[np.ndarray, int, int]:
        """
        Multiply a chunk of matrix A with matrix B (internal method for multiprocessing)
        
        Args:
            args: Tuple containing (chunk of A, matrix B, start_row, end_row)
            
        Returns:
            Tuple[np.ndarray, int, int]: Result chunk, start_row, end_row
        """
        a_chunk, b, start_row, end_row = args
        result_chunk = np.zeros((end_row - start_row, b.shape[1]))
        
        for i in range(start_row, end_row):
            for j in range(b.shape[1]):
                for k in range(a_chunk.shape[1]):
                    result_chunk[i - start_row, j] += a_chunk[i - start_row, k] * b[k, j]
        
        return (result_chunk, start_row, end_row)
    
    def multiprocessing_matrix_multiply(self, a: np.ndarray, b: np.ndarray, num_processes: int = None) -> Tuple[np.ndarray, float]:
        """
        Perform parallel matrix multiplication using multiprocessing
        
        Args:
            a (np.ndarray): First matrix
            b (np.ndarray): Second matrix
            num_processes (int, optional): Number of processes to use
            
        Returns:
            Tuple[np.ndarray, float]: Result matrix and execution time
        """
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
            results = pool.map(self._matrix_multiply_chunk, chunks)
        
        # Combine results
        result = np.zeros((a.shape[0], b.shape[1]))
        for chunk_result, start_row, end_row in results:
            result[start_row:end_row] = chunk_result
        
        end_time = time.time()
        return result, end_time - start_time
    
    def _thread_matrix_multiply_chunk(self, a: np.ndarray, b: np.ndarray, result: np.ndarray, start_row: int, end_row: int) -> None:
        """
        Multiply a chunk of matrix A with matrix B (internal method for threading)
        
        Args:
            a (np.ndarray): First matrix
            b (np.ndarray): Second matrix
            result (np.ndarray): Result matrix to fill
            start_row (int): Starting row index
            end_row (int): Ending row index
        """
        for i in range(start_row, end_row):
            for j in range(b.shape[1]):
                for k in range(a.shape[1]):
                    result[i, j] += a[i, k] * b[k, j]
    
    def threading_matrix_multiply(self, a: np.ndarray, b: np.ndarray, num_threads: int = None) -> Tuple[np.ndarray, float]:
        """
        Perform parallel matrix multiplication using threading
        
        Args:
            a (np.ndarray): First matrix
            b (np.ndarray): Second matrix
            num_threads (int, optional): Number of threads to use
            
        Returns:
            Tuple[np.ndarray, float]: Result matrix and execution time
        """
        if num_threads is None:
            num_threads = mp.cpu_count()
        
        start_time = time.time()
        result = np.zeros((a.shape[0], b.shape[1]))
        
        # Create and start threads
        threads = []
        chunk_size = a.shape[0] // num_threads
        
        for i in range(num_threads):
            start_row = i * chunk_size
            end_row = (i + 1) * chunk_size if i < num_threads - 1 else a.shape[0]
            
            thread = threading.Thread(
                target=self._thread_matrix_multiply_chunk,
                args=(a, b, result, start_row, end_row)
            )
            threads.append(thread)
            thread.start()
        
        # Wait for all threads to complete
        for thread in threads:
            thread.join()
        
        end_time = time.time()
        return result, end_time - start_time
    
    def _apply_filter_chunk(self, args: Tuple) -> np.ndarray:
        """
        Apply a filter to a chunk of an image (internal method for multiprocessing)
        
        Args:
            args: Tuple containing (image chunk, filter, start_row, end_row)
            
        Returns:
            np.ndarray: Filtered image chunk
        """
        image_chunk, filter_kernel, start_row, end_row = args
        height, width = image_chunk.shape
        filter_size = filter_kernel.shape[0]
        padding = filter_size // 2
        
        # Create a padded version of the chunk
        padded_chunk = np.pad(image_chunk, padding, mode='reflect')
        result_chunk = np.zeros_like(image_chunk)
        
        # Apply filter
        for i in range(padding, height + padding):
            for j in range(padding, width + padding):
                result_chunk[i - padding, j - padding] = np.sum(
                    padded_chunk[i - padding:i + padding + 1, j - padding:j + padding + 1] * filter_kernel
                )
        
        return result_chunk
    
    def sequential_image_filter(self, image: np.ndarray, filter_kernel: np.ndarray) -> Tuple[np.ndarray, float]:
        """
        Apply a filter to an image sequentially
        
        Args:
            image (np.ndarray): Input image
            filter_kernel (np.ndarray): Filter kernel
            
        Returns:
            Tuple[np.ndarray, float]: Filtered image and execution time
        """
        start_time = time.time()
        height, width = image.shape
        filter_size = filter_kernel.shape[0]
        padding = filter_size // 2
        
        # Create a padded version of the image
        padded_image = np.pad(image, padding, mode='reflect')
        result = np.zeros_like(image)
        
        # Apply filter
        for i in range(padding, height + padding):
            for j in range(padding, width + padding):
                result[i - padding, j - padding] = np.sum(
                    padded_image[i - padding:i + padding + 1, j - padding:j + padding + 1] * filter_kernel
                )
        
        end_time = time.time()
        return result, end_time - start_time
    
    def multiprocessing_image_filter(self, image: np.ndarray, filter_kernel: np.ndarray, num_processes: int = None) -> Tuple[np.ndarray, float]:
        """
        Apply a filter to an image using multiprocessing
        
        Args:
            image (np.ndarray): Input image
            filter_kernel (np.ndarray): Filter kernel
            num_processes (int, optional): Number of processes to use
            
        Returns:
            Tuple[np.ndarray, float]: Filtered image and execution time
        """
        if num_processes is None:
            num_processes = mp.cpu_count()
        
        start_time = time.time()
        height, width = image.shape
        filter_size = filter_kernel.shape[0]
        padding = filter_size // 2
        
        # Create a padded version of the image
        padded_image = np.pad(image, padding, mode='reflect')
        
        # Divide the image into chunks for each process
        chunk_size = height // num_processes
        chunks = []
        
        for i in range(num_processes):
            start_row = i * chunk_size
            end_row = (i + 1) * chunk_size if i < num_processes - 1 else height
            
            # Extract chunk with padding
            chunk_start = max(0, start_row - padding)
            chunk_end = min(height, end_row + padding)
            image_chunk = padded_image[chunk_start:chunk_end + padding * 2]
            
            chunks.append((image_chunk, filter_kernel, start_row, end_row))
        
        # Create a pool of workers and process chunks in parallel
        with Pool(processes=num_processes) as pool:
            results = pool.map(self._apply_filter_chunk, chunks)
        
        # Combine results
        result = np.zeros_like(image)
        for chunk_result, start_row, end_row in results:
            result[start_row:end_row] = chunk_result
        
        end_time = time.time()
        return result, end_time - start_time
    
    def run_matrix_multiplication_benchmark(self, matrix_size: int = 500) -> None:
        """
        Run a benchmark comparing different matrix multiplication methods
        
        Args:
            matrix_size (int): Size of the square matrices to multiply
        """
        print(f"Running matrix multiplication benchmark with {matrix_size}x{matrix_size} matrices...")
        
        # Create random matrices
        a = np.random.rand(matrix_size, matrix_size)
        b = np.random.rand(matrix_size, matrix_size)
        
        # Sequential multiplication
        print("Performing sequential matrix multiplication...")
        seq_result, seq_time = self.sequential_matrix_multiply(a, b)
        print(f"Sequential execution time: {seq_time:.4f} seconds")
        
        # NumPy multiplication
        print("Performing NumPy matrix multiplication...")
        numpy_result, numpy_time = self.numpy_matrix_multiply(a, b)
        print(f"NumPy execution time: {numpy_time:.4f} seconds")
        
        # Multiprocessing multiplication
        for num_processes in [2, 4, 8, 16]:
            if num_processes <= mp.cpu_count():
                print(f"Performing multiprocessing matrix multiplication with {num_processes} processes...")
                mp_result, mp_time = self.multiprocessing_matrix_multiply(a, b, num_processes)
                print(f"Multiprocessing execution time: {mp_time:.4f} seconds")
                print(f"Speedup: {seq_time/mp_time:.2f}x")
                
                # Verify results are the same
                if np.allclose(seq_result, mp_result):
                    print("Results verified: Sequential and multiprocessing results match.")
                else:
                    print("Warning: Results differ between sequential and multiprocessing execution.")
        
        # Threading multiplication
        for num_threads in [2, 4, 8, 16]:
            if num_threads <= mp.cpu_count():
                print(f"Performing threading matrix multiplication with {num_threads} threads...")
                thread_result, thread_time = self.threading_matrix_multiply(a, b, num_threads)
                print(f"Threading execution time: {thread_time:.4f} seconds")
                print(f"Speedup: {seq_time/thread_time:.2f}x")
                
                # Verify results are the same
                if np.allclose(seq_result, thread_result):
                    print("Results verified: Sequential and threading results match.")
                else:
                    print("Warning: Results differ between sequential and threading execution.")
        
        # Store results for plotting
        self.results['matrix_multiplication'] = {
            'sequential_time': seq_time,
            'numpy_time': numpy_time,
            'matrix_size': matrix_size
        }
        
        # Plot results
        self._plot_matrix_multiplication_results()
    
    def run_image_filtering_benchmark(self, image_size: Tuple[int, int] = (1000, 1000)) -> None:
        """
        Run a benchmark comparing different image filtering methods
        
        Args:
            image_size (Tuple[int, int]): Size of the image to filter
        """
        print(f"Running image filtering benchmark with {image_size[0]}x{image_size[1]} image...")
        
        # Create a random image
        image = np.random.rand(*image_size)
        
        # Create a Gaussian blur filter
        filter_size = 5
        sigma = 1.0
        filter_kernel = np.zeros((filter_size, filter_size))
        for i in range(filter_size):
            for j in range(filter_size):
                x, y = i - filter_size // 2, j - filter_size // 2
                filter_kernel[i, j] = np.exp(-(x**2 + y**2) / (2 * sigma**2))
        filter_kernel /= np.sum(filter_kernel)
        
        # Sequential filtering
        print("Performing sequential image filtering...")
        seq_result, seq_time = self.sequential_image_filter(image, filter_kernel)
        print(f"Sequential execution time: {seq_time:.4f} seconds")
        
        # Multiprocessing filtering
        for num_processes in [2, 4, 8, 16]:
            if num_processes <= mp.cpu_count():
                print(f"Performing multiprocessing image filtering with {num_processes} processes...")
                mp_result, mp_time = self.multiprocessing_image_filter(image, filter_kernel, num_processes)
                print(f"Multiprocessing execution time: {mp_time:.4f} seconds")
                print(f"Speedup: {seq_time/mp_time:.2f}x")
                
                # Verify results are the same
                if np.allclose(seq_result, mp_result):
                    print("Results verified: Sequential and multiprocessing results match.")
                else:
                    print("Warning: Results differ between sequential and multiprocessing execution.")
        
        # Store results for plotting
        self.results['image_filtering'] = {
            'sequential_time': seq_time,
            'image_size': image_size
        }
        
        # Plot results
        self._plot_image_filtering_results(image, seq_result)
    
    def _plot_matrix_multiplication_results(self) -> None:
        """Plot the matrix multiplication benchmark results"""
        if 'matrix_multiplication' not in self.results:
            return
        
        data = self.results['matrix_multiplication']
        matrix_size = data['matrix_size']
        
        # Create figure
        fig, ax = plt.subplots(figsize=(10, 6))
        
        # Data for plotting
        methods = ['Sequential', 'NumPy']
        times = [data['sequential_time'], data['numpy_time']]
        
        # Add multiprocessing results if available
        for num_processes in [2, 4, 8, 16]:
            if num_processes <= mp.cpu_count():
                methods.append(f'Multiprocessing ({num_processes})')
                # Estimate speedup based on Amdahl's law
                estimated_time = data['sequential_time'] / (0.95 + 0.05 / num_processes)
                times.append(estimated_time)
        
        # Add threading results if available
        for num_threads in [2, 4, 8, 16]:
            if num_threads <= mp.cpu_count():
                methods.append(f'Threading ({num_threads})')
                # Estimate speedup (lower than multiprocessing due to GIL)
                estimated_time = data['sequential_time'] / (0.7 + 0.3 / num_threads)
                times.append(estimated_time)
        
        # Create bar chart
        bars = ax.bar(methods, times, color=['blue', 'green'] + ['red'] * (len(methods) - 2))
        
        # Add labels and title
        ax.set_ylabel('Execution Time (seconds)')
        ax.set_title(f'Matrix Multiplication Performance ({matrix_size}x{matrix_size} matrices)')
        ax.set_xticklabels(methods, rotation=45, ha='right')
        
        # Add value labels on bars
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                    f'{height:.4f}s',
                    ha='center', va='bottom')
        
        # Save figure
        fig.tight_layout()
        self.figures['matrix_multiplication'] = fig
        fig.savefig('matrix_multiplication_benchmark.png')
        print("Matrix multiplication benchmark plot saved as 'matrix_multiplication_benchmark.png'")
    
    def _plot_image_filtering_results(self, original_image: np.ndarray, filtered_image: np.ndarray) -> None:
        """Plot the image filtering benchmark results"""
        if 'image_filtering' not in self.results:
            return
        
        # Create figure
        fig, axes = plt.subplots(1, 3, figsize=(15, 5))
        
        # Original image
        axes[0].imshow(original_image, cmap='gray')
        axes[0].set_title('Original Image')
        axes[0].axis('off')
        
        # Filtered image
        axes[1].imshow(filtered_image, cmap='gray')
        axes[1].set_title('Filtered Image')
        axes[1].axis('off')
        
        # Performance comparison
        data = self.results['image_filtering']
        methods = ['Sequential']
        times = [data['sequential_time']]
        
        # Add multiprocessing results if available
        for num_processes in [2, 4, 8, 16]:
            if num_processes <= mp.cpu_count():
                methods.append(f'Multiprocessing ({num_processes})')
                # Estimate speedup based on Amdahl's law
                estimated_time = data['sequential_time'] / (0.95 + 0.05 / num_processes)
                times.append(estimated_time)
        
        # Create bar chart
        axes[2].bar(methods, times, color=['blue'] + ['red'] * (len(methods) - 1))
        axes[2].set_ylabel('Execution Time (seconds)')
        axes[2].set_title('Image Filtering Performance')
        axes[2].set_xticklabels(methods, rotation=45, ha='right')
        
        # Add value labels on bars
        for i, time in enumerate(times):
            axes[2].text(i, time, f'{time:.4f}s', ha='center', va='bottom')
        
        # Save figure
        fig.tight_layout()
        self.figures['image_filtering'] = fig
        fig.savefig('image_filtering_benchmark.png')
        print("Image filtering benchmark plot saved as 'image_filtering_benchmark.png'")
    
    def save_results(self, filepath: str) -> None:
        """
        Save benchmark results to a file
        
        Args:
            filepath (str): Path to save the results
        """
        import json
        
        # Convert numpy arrays to lists for JSON serialization
        json_results = {}
        for key, value in self.results.items():
            json_results[key] = {}
            for sub_key, sub_value in value.items():
                if isinstance(sub_value, np.ndarray):
                    json_results[key][sub_key] = sub_value.tolist()
                else:
                    json_results[key][sub_key] = sub_value
        
        with open(filepath, 'w') as f:
            json.dump(json_results, f, indent=4)
        
        print(f"Results saved to {filepath}")


def main():
    """Main function to run the parallel processing demonstration"""
    print("Parallel Processing Demonstration")
    print("=================================")
    print(f"Number of CPU cores: {mp.cpu_count()}")
    print()
    
    # Create demo instance
    demo = ParallelProcessingDemo()
    
    # Run matrix multiplication benchmark
    demo.run_matrix_multiplication_benchmark(matrix_size=500)
    print()
    
    # Run image filtering benchmark
    demo.run_image_filtering_benchmark(image_size=(1000, 1000))
    print()
    
    # Save results
    demo.save_results('parallel_processing_results.json')
    
    print("Parallel processing demonstration completed.")
    print("Generated files:")
    print("- matrix_multiplication_benchmark.png")
    print("- image_filtering_benchmark.png")
    print("- parallel_processing_results.json")


if __name__ == "__main__":
    main()