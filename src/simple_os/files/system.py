"""
Main file system module.
Implements contiguous allocation with First-Fit algorithm.
Manages files, blocks, and process permissions.
"""

from typing import List, Tuple
from simple_os.files.disk import Disk
from simple_os.files.file import File


class FileSystem:
    """File system with contiguous allocation and First-Fit algorithm"""
    
    def __init__(self, total_blocks: int):
        """Initializes the file system"""

        # Create disk with specified number of blocks
        self.disk = Disk(total_blocks)
        
        # Dictionary to store file information
        # Key: File ID (letter), Value: File object
        self.files = {}
        
        # Set of real-time processes
        self.real_time_processes = set()

        # Set of processes
        self.processes = set()
        
        # Mapping for unique IDs (for internal control)
        self.next_id = 1
    
    def add_real_time_process(self, process_id: int):
        """Marks a process as real-time"""
        self.real_time_processes.add(process_id)
        print(f"Process P{process_id} marked as real-time")

    def add_process(self, process_id: int):
        """Adds a process to the set of processes"""
        self.processes.add(process_id)
        print(f"Process P{process_id} added to the set of processes")
    
    def is_real_time_process(self, process_id: int) -> bool:
        """Checks if a process is real-time"""
        return process_id in self.real_time_processes
    
    def first_fit(self, size: int) -> int:
        """Implements First-Fit algorithm to find contiguous space"""
        start = -1  # Index of free space start
        count = 0  # Counter of consecutive free blocks
        
        # Traverse all disk blocks
        for i in range(self.disk.total_blocks):
            if self.disk.is_free(i):
                # If it's the start of a free sequence
                if start == -1:
                    start = i
                
                count += 1
                
                # If sufficient space found
                if count == size:
                    return start
            else:
                # Reset counters when finding occupied block
                start = -1
                count = 0
        
        # No sufficient contiguous space found
        return -1
    
    def create_file(self, process_id: int, file_name: str, 
                   size_blocks: int, file_id: str) -> bool:
        """Creates a new file in the system"""
        # Initial validations
        if size_blocks <= 0:
            print(f"Error: Invalid size for file '{file_name}'")
            return False
        
        if file_id in self.files:
            print(f"Error: ID '{file_id}' already in use")
            return False
        
        if process_id not in self.processes and process_id not in self.real_time_processes:
            print(f"Error: Process P{process_id} not found")
            return False
        
        # Find space using First-Fit algorithm
        start = self.first_fit(size_blocks)
        
        if start == -1:
            print(f"Error: Insufficient space for file '{file_name}' "
                  f"({size_blocks} blocks)")
            return False
        
        # Create File object
        file = File(file_id, file_name, size_blocks, 
                   process_id, start)
        
        # Occupy blocks on disk
        for i in range(start, start + size_blocks):
            if not self.disk.occupy_block(i, file_name):
                # If fails, free already allocated blocks
                for j in range(start, i):
                    self.disk.free_block(j)
                print(f"Error: Failed to allocate block {i}")
                return False
        
        # Store file in system
        self.files[file_name] = file
        
        print(f"Success: File '{file_name}' (ID: {file_id}) created "
              f"by process P{process_id}")
        print(f"  Allocated blocks: {start} to {start + size_blocks - 1} "
              f"({size_blocks} blocks)")
        
        return True
    
    def delete_file(self, process_id: int, file_id: str) -> bool:
        """Deletes a file from the system"""
        # Check if file exists
        if file_id not in self.files:
            print(f"Error: File with ID '{file_id}' not found")
            return False
        
        file = self.files[file_id]
        
        # Check permissions
        if not self.is_real_time_process(process_id):
            # Regular process can only delete its own files
            if not file.belongs_to_process(process_id):
                print(f"Error: Regular process P{process_id} not allowed "
                      f"to delete file '{file_id}' (owner: P{file.owner_process})")
                return False
        
        # Free all blocks occupied by the file
        for block in file.get_blocks():
            self.disk.free_block(block)
        
        # Remove file from system
        del self.files[file_id]
        
        print(f"Success: File '{file_id}' ('{file.name}') deleted "
              f"by process P{process_id}")
        
        return True
    
    def load_initial_state(self, initial_files: List[Tuple]) -> bool:
        """Loads initial disk state"""
        print("Loading initial disk state...")
        file_id = 0
        for file_name, start_block, size in initial_files:
            # Check if blocks are within disk
            if start_block + size > self.disk.total_blocks:
                print(f"Error: File '{file_name}' exceeds disk size")
                return False
            
            # Check if blocks are free
            for i in range(start_block, start_block + size):
                if not self.disk.is_free(i):
                    print(f"Error: Conflict at block {i} for file '{file_name}'")
                    return False

            file = File(file_id, file_name,
                       size, 0, start_block)
            
            # Occupy blocks
            for i in range(start_block, start_block + size):
                self.disk.occupy_block(i, file_name)
            
            # Store file
            self.files[file_name] = file
            file_id += 1
        
        self.next_id = file_id
        print(f"Initial state loaded: {len(initial_files)} files")
        return True
    
    def execute_operations(self, operations: List):
        """Executes a list of operations in the file system"""
        print(f"\nExecuting {len(operations)} operations...")
        
        for i, operation in enumerate(operations, 1):
            print(f"\n[{i}] {operation}")
            
            if operation.is_creation():
                # For creation, we need to generate a unique ID (letter)
                # Based on the next numeric ID
                file_id = self.next_id
                self.next_id += 1
                
                self.create_file(operation.process_id, operation.file_name,
                               operation.size, file_id)
            else:
                # For deletion, file_id is in the operation
                self.delete_file(operation.process_id, operation.file_id)
    
    def generate_disk_map(self):
        """Generates a visual map of disk occupation"""
        print("\n" + "="*70)
        print("DISK OCCUPATION MAP")
        print("="*70)
        
        # Legend
        print("\nLEGEND:")
        print("  0 = Free block")
        print("  Letter = name of file occupying the block")
        print("-"*70)
        
        # Map configuration
        blocks_per_line = 20
        total_lines = (self.disk.total_blocks + blocks_per_line - 1) // blocks_per_line
        
        # Generate map
        for line in range(total_lines):
            start = line * blocks_per_line
            end = min(start + blocks_per_line, self.disk.total_blocks)
            
            # Line header
            print(f"\nBlocks {start:3d} to {end-1:3d}: ", end="")
            
            # Block values
            for i in range(start, end):
                file_name = self.disk.get_block(i).get_file_name()
                print(f"{file_name}", end=" ")

            print("")

        print("")
        print("-"*70)
    
    def get_disk_state(self) -> List[str]:
        """Returns current disk state"""
        return self.disk.get_state()