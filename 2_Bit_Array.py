class BitArray:
    def __init__(self, length):
        self.length = length
        self.array = [0] * ((length + 31) // 32) 

    def set(self, i):
        if 0 <= i < self.length:
            self.array[i // 32] |= (1 << (i % 32))

    def clear(self, i):
        if 0 <= i < self.length:
            self.array[i // 32] &= ~(1 << (i % 32))
