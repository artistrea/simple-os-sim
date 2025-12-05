"""
Module for managing file system operations.
Responsible for coordinating operation execution
and managing real-time processes.
"""

from typing import List, Dict, Any
from simple_os.files.system import FileSystem


class FileSystemManager:
    """Main file system manager"""
    
    def __init__(self, total_blocks: int):
        """Initializes the file system manager"""
        
        # Create file system
        self.system = FileSystem(total_blocks)
        
        # List of real-time processes
        self.real_time_processes = set()

        # List of processes
        self.processes = set()
        
        # Queue of operations to execute
        self.pending_operations = []
    
    def add_real_time_process(self, process_id: int):
        """Adds a process to the real-time process list"""
        self.real_time_processes.add(process_id)
        self.system.add_real_time_process(process_id)
    
    def add_process(self, process_id: int):
        """Adds a process to the process list"""
        self.processes.add(process_id)
        self.system.add_process(process_id)
    
    def add_operation(self, operation):
        """Adds an operation to the execution queue"""
        self.pending_operations.append(operation)
    
    def load_initial_files(self, initial_files: List[tuple]) -> bool:
        """Loads initial files into the system"""
        return self.system.load_initial_state(initial_files)
    
    def execute_all_operations(self):
        """Executes all pending operations in the system"""
        if not self.pending_operations:
            print("No pending operations to execute.")
            return
        
        print(f"\nExecuting {len(self.pending_operations)} pending operations...")
        self.system.execute_operations(self.pending_operations)
        
        # Clear operation queue after execution
        self.pending_operations = []
    
    def get_report(self) -> Dict[str, Any]:
        """Returns a complete report of current state"""
        disk_state = self.system.get_disk_state()
        
        # Count free and occupied blocks
        free_blocks = disk_state.count('0')
        occupied_blocks = len(disk_state) - free_blocks
        
        report = {
            'total_blocks': self.system.disk.total_blocks,
            'free_blocks': free_blocks,
            'occupied_blocks': occupied_blocks,
            'occupied_percent': (occupied_blocks / self.system.disk.total_blocks) * 100,
            'total_files': len(self.system.files),
            'real_time_processes': sorted(self.real_time_processes),
            'processes': sorted(self.processes),
            'disk_state': disk_state,
            'files': {id: str(file) for id, file in self.system.files.items()}
        }
        
        return report
    
    def show_current_state(self):
        """hows current file system state"""
        print("\n" + "="*60)
        print("CURRENT FILE SYSTEM STATE")
        print("="*60)
        
        report = self.get_report()
        
        print("\nDisk Configuration:")
        print(f"  • Total blocks: {report['total_blocks']}")
        print(f"  • Free blocks: {report['free_blocks']}")
        print(f"  • Occupied blocks: {report['occupied_blocks']} "
              f"({report['occupied_percent']:.1f}%)")
        print(f"  • Total files: {report['total_files']}")
        
        if report['real_time_processes']:
            print(f"\nReal-time processes: {report['real_time_processes']}")

        if report['processes']:
            print(f"\nProcesses: {report['processes']}")
        
        if report['files']:
            print("\nFiles in system:")
            for file_id, info in report['files'].items():
                print(f"  • {info}")
        
        print("="*60)

        self.system.generate_disk_map()