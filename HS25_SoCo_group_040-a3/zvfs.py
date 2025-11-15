import sys
import struct
import time
import os

class ZestFileSystem:
    MAX_FILES = 32
    MAX_FILENAME = 31
    FILE_ENTRY_SIZE = 64
    HEADER_SIZE = 64

    def __init__(self, filename):
        self.filename = filename
        self.magic = b"ZVFSDSK1"
        self.version = 1
        self.flags = 0
        self.file_count = 0
        self.file_capacity = self.MAX_FILES
        self.file_entry_size = self.FILE_ENTRY_SIZE
        self.file_table_offset = self.HEADER_SIZE
        self.data_start_offset = self.HEADER_SIZE + self.MAX_FILES * self.FILE_ENTRY_SIZE
        self.next_free_offset = self.data_start_offset
        self.free_entry_offset = 0
        self.deleted_files = 0
        self.file_entries = [self._empty_file_entry() for _ in range(self.MAX_FILES)]


    def _empty_file_entry(self):
        """Return a dictionary representing an empty file entry"""
        return {
            "name": b"",
            "start": 0,
            "length": 0,
            "type": 0,
            "flag": 0,
            "created": 0
        }

    @staticmethod
    def create_new_fs(name):
        """Create a new empty .zvfs filesystem"""
        magic = b"ZVFSDSK1"
        version = 1
        flags = 0
        file_count = 0
        file_capacity = ZestFileSystem.MAX_FILES
        file_entry_size = ZestFileSystem.FILE_ENTRY_SIZE
        file_table_offset = ZestFileSystem.HEADER_SIZE
        data_start_offset = file_table_offset + ZestFileSystem.MAX_FILES * ZestFileSystem.FILE_ENTRY_SIZE
        next_free_offset = data_start_offset
        free_entry_offset = 0
        deleted_files = 0
        reserved2 = b"\x00" * 26  # padding

        # Pack header
        header = struct.pack(
            "<8s B B H H H H I I I H H 26s",
            magic, version, flags, file_count, file_capacity, file_entry_size,
            file_table_offset, data_start_offset, next_free_offset,
            free_entry_offset, deleted_files, 0, reserved2
        )
        # 32 empty file entries
        empty_entry = b"\x00" * ZestFileSystem.FILE_ENTRY_SIZE
        file_entries = empty_entry * ZestFileSystem.MAX_FILES
        # Write to disk
        with open(name, "wb") as f:
            f.write(header)
            f.write(file_entries)

        print(f"Created new filesystem '{name}' with capacity for {ZestFileSystem.MAX_FILES} files.")

    @staticmethod
    def get_info_fs(name):
        # Check if file exists
        if not os.path.exists(name):
            print(f"File '{name}' does not exist!")
            # Exit the programme if file does not exist
            sys.exit(1)

        with open(name, "rb") as f:
            header_data = f.read(ZestFileSystem.HEADER_SIZE)

            fields = ["magic", "version", "flags", "reserved0", "file_count", "file_capacity",
                      "file_entry_size", "reserved1", "file_table_offset", "data_start_offset",
                      "next_free_offset", "free_entry_offset", "deleted_files", "reserved2"]

            values = struct.unpack("<8s B B H H H H H I I I I H 26s", header_data)
            header = dict(zip(fields, values))

            print(f"File system: {name}")
            print(f"Magic: {header['magic']}")
            print(f"Version: {header['version']}")
            print(f"Files present: {header['file_count']}")
            print(f"Free entries: {header['file_capacity'] - header['file_count']}")
            print(f"Deleted files: {header['deleted_files']}")
            print(f"Total size: {os.path.getsize(name)} bytes")


if __name__ == '__main__':
    if sys.argv[1] == "mkfs":
        ZestFileSystem.create_new_fs(sys.argv[2])
    elif sys.argv[1] == "gifs":
        ZestFileSystem.get_info_fs(sys.argv[2])

    # with open("filesystem1.zvfs", "rb") as file:
    #     content = file.read()
    #     print(content)
