"""
Module that defines basic structures for disk and block representation.
Each disk block is represented by a DiskBlock object.
The entire disk is represented as a collection of blocks.
"""

class DiskBlock:
    """Represents an individual disk block"""
    
    def __init__(self, index, file_name='0'):
        """Initializes a disk block"""
        self.index = index  # Block position in the disk
        self.file_name = file_name  # '0' = free block, letter = file occupying
    
    def __str__(self):
        """Returns string representation of the block"""
        if self.file_name == '0':
            return f"Block {self.index}: Free"
        else:
            return f"Block {self.index}: File '{self.file_name}'"
        
    def get_file_name(self):
        """Returns the file name of the block"""
        return self.file_name
    
    def free(self):
        """Frees the block, making it available"""
        self.file_name = '0'
    
    def occupy(self, file_name):
        """Occupies the block with a specific file"""
        if self.file_name != '0':
            return False  # Block already occupied
        self.file_name = file_name
        return True


class Disk:
    """Represents the entire disk as a collection of blocks"""
    
    def __init__(self, total_blocks):
        """Initializes the disk with all blocks free"""
        self.total_blocks = total_blocks
        
        # Initialize all blocks as free
        self.blocks = [DiskBlock(i) for i in range(total_blocks)]
        
        # Dictionary to map files (ID -> information)
        self.files = {}
    
    def get_block(self, index):
        """Returns the block at the specified index"""
        if 0 <= index < self.total_blocks:
            return self.blocks[index]
        return None
    
    def is_free(self, index):
        """Checks if a block is free"""
        block = self.get_block(index)
        return block is not None and block.file_name == '0'
    
    def occupy_block(self, index, file_name):
        """Occupies a specific block with a file"""
        block = self.get_block(index)
        if block:
            return block.occupy(file_name)
        return False
    
    def free_block(self, index):
        """Frees a specific block"""
        block = self.get_block(index)
        if block:
            block.free()
            return True
        return False
    
    def get_state(self):
        """Returns current disk state as a list"""
        return [block.file_name for block in self.blocks]
    
    def __str__(self):
        """Returns string representation of the disk"""
        state = self.get_state()
        return f"Disk with {self.total_blocks} blocks. State: {state}"
