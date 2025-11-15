import sys
import struct
import time
from pathlib import Path
import climage


class ZestFileSystem:
    # Constants
    MAX_FILES = 32
    MAX_FILENAME = 31
    FILE_ENTRY_SIZE = 64
    HEADER_SIZE = 64

    def __init__(self, filename: Path):
        self.filename = Path(filename)

    @staticmethod
    def create_new_fs(name: Path):
        name = Path(name)
        magic = b"ZVFSDSK1"
        version = 1
        flags = 0
        file_count = 0
        file_capacity = ZestFileSystem.MAX_FILES
        file_entry_size = ZestFileSystem.FILE_ENTRY_SIZE
        file_table_offset = ZestFileSystem.HEADER_SIZE
        data_start_offset = file_table_offset + file_capacity * file_entry_size
        next_free_offset = data_start_offset
        free_entry_offset = 0
        deleted_files = 0
        reserved2 = b"\x00" * 26

        # Pack header
        header = struct.pack(
            "<8s B B H H H H H I I I I H 26s",
            magic, version, flags, 0, file_count, file_capacity,
            file_entry_size, 0, file_table_offset, data_start_offset,
            next_free_offset, free_entry_offset, deleted_files, reserved2
        )

        # Empty file table
        empty_entry = b"\x00" * ZestFileSystem.FILE_ENTRY_SIZE
        file_entries = empty_entry * file_capacity

        # Write to disk
        with name.open("wb") as f:
            f.write(header)
            f.write(file_entries)

        print(f"Created new filesystem '{name}' with capacity for {file_capacity} files.")

    @staticmethod
    def get_info_fs(file_system: Path):
        file_system = Path(file_system)
        if not file_system.exists():
            print(f"File '{file_system}' does not exist!")
            sys.exit(1)

        with file_system.open("rb") as f:
            header_data = f.read(ZestFileSystem.HEADER_SIZE)

        fields = [
            "magic", "version", "flags", "reserved0", "file_count",
            "file_capacity", "file_entry_size", "reserved1",
            "file_table_offset", "data_start_offset", "next_free_offset",
            "free_entry_offset", "deleted_files", "reserved2"
        ]

        values = struct.unpack("<8s B B H H H H H I I I I H 26s", header_data)
        header = dict(zip(fields, values))

        print(f"File system: {file_system}")
        print(f"Magic: {header['magic']}")
        print(f"Version: {header['version']}")
        print(f"Files present: {header['file_count']}")
        print(f"Free entries: {header['file_capacity'] - header['file_count']}")
        print(f"Deleted files: {header['deleted_files']}")
        print(f"Total size: {file_system.stat().st_size} bytes")

    def add_file(self, fs_name: Path, file_path: Path):
        fs_name = Path(fs_name)
        file_path = Path(file_path)

        # Validate input
        if not fs_name.exists():
            print(f"File system '{fs_name}' does not exist!")
            sys.exit(1)
        if not file_path.exists():
            print(f"Source file '{file_path}' does not exist!")
            sys.exit(1)

        data = file_path.read_bytes()
        filename = file_path.name
        if len(filename) > self.MAX_FILENAME:
            print(f"Filename '{filename}' too long (max {self.MAX_FILENAME})")
            sys.exit(1)

        # Work on filesystem
        with fs_name.open("r+b") as fs:
            header = list(struct.unpack(
                "<8s B B H H H H H I I I I H 26s",
                fs.read(self.HEADER_SIZE)
            ))

            (
                magic, version, flags, reserved0, count, capacity,
                entry_size, reserved1, table_offset, data_offset,
                next_free, free_entry, deleted, reserved2
            ) = header

            if count >= capacity:
                print("ERROR: File system is full.")
                sys.exit(1)

            # Find free slot
            fs.seek(table_offset)
            free_idx = None
            empty = b"\x00" * self.FILE_ENTRY_SIZE
            for i in range(self.MAX_FILES):
                if fs.read(self.FILE_ENTRY_SIZE) == empty:
                    free_idx = i
                    break
            if free_idx is None:
                print("ERROR: No free file entry found.")
                sys.exit(1)

            # Pad file to multiple of 64 bytes
            pad_len = (64 - (len(data) % 64)) % 64
            data_padded = data + b"\x00" * pad_len

            # Build entry
            name_bytes = filename.encode() + b"\x00" * (32 - len(filename))
            entry = struct.pack(
                "<32s I I I 20s",
                name_bytes,
                len(data),
                next_free,
                0,
                b"\x00" * 20
            )

            # Write entry
            fs.seek(table_offset + free_idx * self.FILE_ENTRY_SIZE)
            fs.write(entry)

            # Append data
            fs.seek(next_free)
            fs.write(data_padded)

            # Update header
            header[4] = count + 1  # file_count
            header[10] = next_free + len(data_padded)  # next_free_offset
            fs.seek(0)
            fs.write(struct.pack(
                "<8s B B H H H H H I I I I H 26s",
                *header
            ))

        print(f"Added '{filename}' ({len(data)} bytes, padded to {len(data_padded)} bytes) at offset {next_free}.")

    def get_file(self, fs_name: Path, filename: str):
        fs_name = Path(fs_name)
        out_path = Path.cwd() / filename

        if not fs_name.exists():
            print(f"File system '{fs_name}' does not exist!")
            sys.exit(1)

        with fs_name.open("rb") as fs:
            header_data = fs.read(self.HEADER_SIZE)
            header = struct.unpack("<8s B B H H H H H I I I I H 26s", header_data)
            table_offset = header[8]

            fs.seek(table_offset)
            for _ in range(self.MAX_FILES):
                entry_data = fs.read(self.FILE_ENTRY_SIZE)
                name_bytes, file_size, file_offset, _, _ = struct.unpack("<32s I I I 20s", entry_data)
                name_str = name_bytes.split(b'\x00')[0].decode()
                if name_str == filename:
                    fs.seek(file_offset)
                    data = fs.read(file_size)
                    out_path.write_bytes(data)
                    print(f"Extracted '{filename}' to '{out_path}' ({file_size} bytes).")
                    return
            print(f"File '{filename}' not found in filesystem.")

    def cat_file(self, fs_name: Path, filename: str):
        fs_name = Path(fs_name)
        if not fs_name.exists():
            print(f"File system '{fs_name}' does not exist!")
            return

        with fs_name.open("rb") as fs:
            header_data = fs.read(self.HEADER_SIZE)
            header = struct.unpack("<8s B B H H H H H I I I I H 26s", header_data)
            table_offset = header[8]

            fs.seek(table_offset)
            for _ in range(self.MAX_FILES):
                entry_data = fs.read(self.FILE_ENTRY_SIZE)
                name_bytes, file_size, file_offset, _, _ = struct.unpack("<32s I I I 20s", entry_data)
                name_str = name_bytes.split(b'\x00')[0].decode()
                if name_str == filename:
                    fs.seek(file_offset)
                    data = fs.read(file_size).rstrip(b'\x00')

                    ext = Path(filename).suffix.lower()
                    if ext in [".png", ".jpg", ".jpeg", ".bmp", ".gif"]:
                        temp_path = Path.cwd() / filename
                        temp_path.write_bytes(data)
                        output = climage.convert(temp_path, width=60)
                        print(output)
                        temp_path.unlink()
                    else:
                        try:
                            if data.startswith(b'\xff\xfe') or data.startswith(b'\xfe\xff'):
                                text = data.decode('utf-16')
                            else:
                                text = data.decode('utf-8')
                            print(text)
                        except UnicodeDecodeError:
                            print("Warning: File is not valid text. Raw bytes output:")
                            print(data)
                    return
            print(f"File '{filename}' not found in filesystem.")


if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("Usage:")
        print("  mkfs <file>")
        print("  gifs <file>")
        print("  addfs <filesystem> <file>")
        print("  getfs <filesystem> <file>")
        print("  catfs <filesystem> <file>")
        sys.exit(1)

    cmd = sys.argv[1]

    if cmd == "mkfs":
        ZestFileSystem.create_new_fs(sys.argv[2])
    elif cmd == "gifs":
        ZestFileSystem.get_info_fs(sys.argv[2])
    elif cmd == "addfs":
        if len(sys.argv) < 4:
            print("Usage: addfs <filesystem> <file>")
            sys.exit(1)
        fs = ZestFileSystem(sys.argv[2])
        fs.add_file(sys.argv[2], sys.argv[3])
    elif cmd == "catfs":
        if len(sys.argv) < 4:
            print("Usage: catfs <filesystem> <file>")
            sys.exit(1)
        fs = ZestFileSystem(sys.argv[2])
        fs.cat_file(sys.argv[2], sys.argv[3])
    elif cmd == "getfs":
        fs = ZestFileSystem("filesystem1.zvfs")
        fs.get_file(sys.argv[2], sys.argv[3])
    else:
        print(f"This operation was not found: <{cmd}>!")
        sys.exit(1)
