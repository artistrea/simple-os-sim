class Memory:
    def __init__(self):
        self.total_blocks = 1024
        self.blocks = [None] * self.total_blocks

    def __repr__(self):
        return str(self.blocks) # retorna lista self.blocks convertida pra string
