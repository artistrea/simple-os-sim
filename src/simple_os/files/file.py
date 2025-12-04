"""
Module that defines the File class and related operations.
Manages file metadata and permissions.
"""

class File:
    """Represents a file in the file system"""
    
    def __init__(self, file_id, name, size, owner_process, start_block):
        """Initializes a new file"""
        self.id = file_id  # File identifier (a single letter)
        self.name = name  # File name
        self.size = size  # Size in blocks
        self.owner_process = owner_process  # Process that created the file
        self.start_block = start_block  # First occupied block
        
        # List of all blocks occupied by this file
        self.blocks = list(range(start_block, start_block + size))
    
    def __str__(self):
        """Returns string representation of the file"""
        return (f"File '{self.id}' ('{self.name}'): "
                f"Owner: P{self.owner_process}, "
                f"Size: {self.size} blocks, "
                f"Start block: {self.start_block}, "
                f"Blocks: {self.blocks}")
    
    def get_blocks(self):
        """Returns the list of blocks occupied by the file"""
        return self.blocks
    
    def belongs_to_process(self, process_id):
        """hecks if the file belongs to a specific process"""
        return self.owner_process == process_id


class FileOperation:
    """Represents an operation to be executed in the file system"""
    
    # Constants for operation types
    CREATE = 0
    DELETE = 1
    
    def __init__(self, process_id, operation_type, file_name, size=0, file_id=None):
        """Initializes a file operationInitializes a file operation"""
        self.process_id = process_id
        self.type = operation_type
        self.file_name = file_name
        self.size = size
        self.file_id = file_id
    
    def __str__(self):
        """Returns string representation of the operation"""
        if self.type == self.CREATE:
            return (f"CREATE operation: Process P{self.process_id}, "
                    f"File '{self.file_name}', Size: {self.size} blocks")
        else:
            return (f"DELETE operation: Process P{self.process_id}, "
                    f"File '{self.file_name}' (ID: {self.file_id})")
    
    def is_creation(self):
        """Checks if it's a create operation"""
        return self.type == self.CREATE
    
    def is_deletion(self):
        """Checks if it's a delete operation"""
        return self.type == self.DELETE
