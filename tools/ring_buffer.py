
import numpy as np
from multiprocessing import shared_memory
import struct

class RingBuffer:
    def __init__(self, name, capacity, message_size, create=False):
        self.capacity = capacity
        self.message_size = message_size
        self.total_size = 8 + 8 + (capacity * message_size)  # 8 bytes each for write_ptr and read_ptr
        
        if create:
            self.shm = shared_memory.SharedMemory(create=True, size=self.total_size, name=name)
            self.buffer = self.shm.buf
            # Initialize pointers
            struct.pack_into('q', self.buffer, 0, 0)  # write_ptr
            struct.pack_into('q', self.buffer, 8, 0)  # read_ptr
        else:
            self.shm = shared_memory.SharedMemory(name=name)
            self.buffer = self.shm.buf

    def write(self, message: bytes):
        if len(message) > self.message_size:
            raise ValueError("Message size exceeds buffer capacity.")
        
        write_ptr = struct.unpack_from('q', self.buffer, 0)[0]
        read_ptr = struct.unpack_from('q', self.buffer, 8)[0]

        # Check if buffer is full
        next_write_ptr = (write_ptr + 1) % self.capacity
        if next_write_ptr == read_ptr:
            print("Buffer is full, dropping message.")
            return False

        # Write message
        start_idx = 16 + (write_ptr * self.message_size)
        self.buffer[start_idx:start_idx + self.message_size] = message
        # Update write_ptr
        struct.pack_into('q', self.buffer, 0, next_write_ptr)
        return True

    def read(self):
        write_ptr = struct.unpack_from('q', self.buffer, 0)[0]
        read_ptr = struct.unpack_from('q', self.buffer, 8)[0]

        if write_ptr == read_ptr:
            return None

        # Read message
        start_idx = 16 + (read_ptr * self.message_size)
        message = self.buffer[start_idx:start_idx + self.message_size]
        # Update read_ptr
        next_read_ptr = (read_ptr + 1) % self.capacity
        struct.pack_into('q', self.buffer, 8, next_read_ptr)
        return bytes(message)
    
    def close(self):
        self.shm.close()
        self.shm.unlink()

