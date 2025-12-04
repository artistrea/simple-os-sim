"""
Module for reading and processing input files.
Interprets the specified format and prepares data
for the file system.
"""

import re
from typing import List, Tuple, Dict, Any


class InputReader:
    """Reader for input files in the specified format"""
    
    @staticmethod
    def read_file(file_name: str) -> Dict[str, Any]:
        """Reads input file and returns structured data"""
        print("chegou no file_system")
        try:
            with open(file_name, 'r') as file:
                lines = file.readlines()
            
            # Remove whitespace and comments
            clean_lines = []
            for line in lines:
                line = line.strip()
                if line and not line.startswith('#'):
                    # Remove comments at end of line
                    if '#' in line:
                        line = line.split('#')[0].strip()
                    clean_lines.append(line)
            
            if len(clean_lines) < 2:
                raise ValueError("File must have at least 2 lines")
            
            # Line 1: Total blocks
            total_blocks = int(clean_lines[0].strip())
            
            # Line 2: Number of occupied segments
            n = int(clean_lines[1].strip())
            
            # Validate number of lines
            if len(clean_lines) < 2 + n:
                raise ValueError(f"Expected {2 + n} lines, but file has {len(clean_lines)}")
            
            # Lines 3 to n+2: Occupied segments
            initial_files = []
            for i in range(2, 2 + n):
                parts = clean_lines[i].split(", ")
                if len(parts) != 3:
                    raise ValueError(f"Line {i+1}: Invalid format. Expected: file_id start_block size")
                
                file_id = parts[0].strip()
                start_block = int(parts[1])
                size = int(parts[2])
                
                # Validations
                if not file_id.isalpha() or len(file_id) != 1:
                    raise ValueError(f"Line {i+1}: File ID must be a single letter")
                if start_block < 0:
                    raise ValueError(f"Line {i+1}: Start block cannot be negative")
                if size <= 0:
                    raise ValueError(f"Line {i+1}: Size must be positive")
                
                initial_files.append((file_id, start_block, size))
            
            # Remaining lines: Operations
            operations = []
            for i in range(2 + n, len(clean_lines)):
                operation_line = clean_lines[i]
                operation = InputReader.parse_operation_line(operation_line, i+1)
                if operation:
                    operations.append(operation)

            
            # Check process IDs are sequential starting from 0
            process_ids = set(op.process_id for op in operations)
            if process_ids:
                max_id = max(process_ids)
                expected = set(range(max_id + 1))
                if not process_ids.issubset(expected):
                    print(f"Warning: Process IDs are not sequential starting from 0")
            
            return {
                'total_blocks': total_blocks,
                'initial_files': initial_files,
                'operations': operations,
                'total_operations': len(operations)
            }
            
        except FileNotFoundError:
            print(f"Error: File '{file_name}' not found")
            return None
        except ValueError as e:
            print(f"Format error in file: {e}")
            return None
        except Exception as e:
            print(f"Error reading file: {e}")
            return None
    
    @staticmethod
    def parse_operation_line(line: str, line_number: int):
        """
        Parses an operation line.
        
        Expected formats:
        For creation: "process_id, 1, file_name, size"
        For deletion: "process_id, 2, file_name, file_id"
        """
        # Erro aqui
        from file import FileOperation
        
        try:
            # Remove spaces and split by comma
            parts = [p.strip() for p in line.split(',')]
            
            if len(parts) < 3:
                raise ValueError(f"Line {line_number}: Too few fields")
            
            process_id = int(parts[0])
            operation_code = int(parts[1])
            file_name = parts[2]
            
            # Basic validations
            if process_id < 0:
                raise ValueError(f"Line {line_number}: Process ID cannot be negative")
            
            if operation_code not in [1, 2]:
                raise ValueError(f"Line {line_number}: Invalid operation code (must be 1 or 2)")
            
            if operation_code == 1:  # Creation
                if len(parts) != 4:
                    raise ValueError(f"Line {line_number}: Creation requires 4 fields")
                size = int(parts[3])
                if size <= 0:
                    raise ValueError(f"Line {line_number}: Size must be positive")
                return FileOperation(process_id, operation_code, file_name, size)
            
            else:  # Deletion (code 2)
                if len(parts) != 4:
                    raise ValueError(f"Line {line_number}: Deletion requires 4 fields")
                file_id = parts[3]
                if not file_id.isalpha() or len(file_id) != 1:
                    raise ValueError(f"Line {line_number}: File ID must be a single letter")
                return FileOperation(process_id, operation_code, file_name, file_id=file_id)
                
        except ValueError as e:
            print(f"Error parsing line {line_number}: {e}")
            print(f"  Line: {line}")
            return None
        except Exception as e:
            print(f"Unexpected error parsing line {line_number}: {e}")
            return None
    
    @staticmethod
    def create_example_file():
        """
        Creates an example file in the correct format.
        
        Returns:
            str: Example file content
        """
        example = """100  # Total blocks in disk
3    # Number of initially occupied segments
A 0 5      # File A occupies 5 blocks starting at block 0
B 10 8     # File B occupies 8 blocks starting at block 10
C 25 3     # File C occupies 3 blocks starting at block 25

# Operations:
# Format: process_id, operation_code, file_name, extra_parameter
# Codes: 1 = create, 2 = delete
0, 1, system.txt, 8      # Process 0 creates 8-block file
1, 1, data.bin, 15       # Process 1 creates 15-block file
0, 2, existing_file, B  # Process 0 deletes file B
2, 1, test.log, 5        # Process 2 creates 5-block file
1, 2, my_file, A      # Process 1 tries to delete file A (will it be allowed?)
99, 1, real_time.dat, 20 # Process 99 (real-time) creates file
99, 2, any_file, C        # Process 99 deletes file C (allowed for real-time)"""
        
        return example