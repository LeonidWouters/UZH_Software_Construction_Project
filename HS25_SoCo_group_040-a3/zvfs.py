import sys
import struct
from pathlib import Path
import climage
import time


class ZestFileSystem:
    # Constants
    MAX_FILES = 32
    MAX_FILENAME = 31
    FILE_ENTRY_SIZE = 64
    HEADER_SIZE = 64
    HEADER_FORMAT = "<8s B B H H H H H I I I I H 26s"
    FILE_ENTRY_FORMAT = "<32s I I B B H Q 12s"

    def __init__(self, filename: str):
        self.filename = Path(filename)

    @staticmethod
    def create_new_fs(name: str):
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
            ZestFileSystem.HEADER_FORMAT,
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
    def get_info_fs(file_system: str):
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
        values = struct.unpack(ZestFileSystem.HEADER_FORMAT, header_data)
        header = dict(zip(fields, values))
        print(f"File system: {file_system}")
        print(f"Magic: {header['magic'].decode(errors='ignore')}")
        print(f"Version: {header['version']}")
        print(f"Files present: {header['file_count']}")
        print(f"Free entries: {header['file_capacity'] - header['file_count']}")
        print(f"Deleted files: {header['deleted_files']}")
        print(f"Total size: {file_system.stat().st_size} bytes")


    def add_file(self, fs_name: str, file_path: str):
        fs_name = Path(fs_name)
        file_path = Path(file_path)
        #Check if paths exist
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
        #Open file in read binary mode
        with fs_name.open("r+b") as fs:
            # Read header
            header = list(struct.unpack(
                self.HEADER_FORMAT,
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
            # Locate free entry
            fs.seek(table_offset)
            free_idx = None
            empty_entry = b"\x00" * self.FILE_ENTRY_SIZE
            for i in range(self.MAX_FILES):
                if fs.read(self.FILE_ENTRY_SIZE) == empty_entry:
                    free_idx = i
                    break
            if free_idx is None:
                print("ERROR: No free file entry found.")
                sys.exit(1)
            # 64-byte align padding
            pad_len = (64 - (len(data) % 64)) % 64
            data_padded = data + b"\x00" * pad_len
            name_bytes = filename.encode('utf-8').ljust(32, b'\x00')
            start_offset = next_free
            file_size = len(data)
            type_field = 0
            flag_field = 0  # active
            reserved0 = 0
            created = int(time.time())
            reserved1 = b"\x00" * 12
            entry = struct.pack(
                self.FILE_ENTRY_FORMAT,
                name_bytes,
                start_offset,
                file_size,
                type_field,
                flag_field,
                reserved0,
                created,
                reserved1
            )
            # Write entry to file table
            fs.seek(table_offset + free_idx * self.FILE_ENTRY_SIZE)
            fs.write(entry)
            # Append data region
            fs.seek(start_offset)
            fs.write(data_padded)
            # Update header
            header[4] = count + 1  # file_count
            header[10] = start_offset + len(data_padded)  # next_free_offset
            fs.seek(0)
            fs.write(struct.pack(
                self.HEADER_FORMAT,
                *header
            ))
        print(f"Added '{filename}' ({file_size} bytes, padded to {len(data_padded)} bytes) at offset {start_offset}.")


    def get_file(self, fs_name: str, filename: str):
        fs_name = Path(fs_name)
        out_path = Path.cwd() / filename
        if not fs_name.exists():
            print(f"File system '{fs_name}' does not exist!")
            sys.exit(1)
        with fs_name.open("rb") as fs:
            header_data = fs.read(self.HEADER_SIZE)
            header = struct.unpack(self.HEADER_FORMAT, header_data)
            table_offset = header[8]
            fs.seek(table_offset)
            for _ in range(self.MAX_FILES):
                entry_data = fs.read(self.FILE_ENTRY_SIZE)
                if entry_data == b'\x00' * self.FILE_ENTRY_SIZE:
                    continue
                (name_bytes, start_offset, file_size, type_field, flag_field,
                 reserved0, created, reserved1) = struct.unpack(self.FILE_ENTRY_FORMAT, entry_data)
                name_str = name_bytes.split(b'\x00')[0].decode(errors='ignore')
                if name_str == filename:
                    if flag_field == 1:  # 1 means deleted
                        print(f"File '{filename}' is deleted.")
                        sys.exit(1)
                    fs.seek(start_offset)
                    data = fs.read(file_size)
                    out_path.write_bytes(data)
                    print(f"Extracted '{filename}' to '{out_path}' ({file_size} bytes).")
                    return
            print(f"File '{filename}' not found in filesystem.")


    def cat_file(self, fs_name: str, filename: str):
        fs_name = Path(fs_name)
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
                if len(entry_data) < self.FILE_ENTRY_SIZE:
                    continue  # Skip empty files
                (
                    name_bytes,
                    start_offset,
                    length,
                    type_field,
                    flag_field,
                    reserved0,
                    created_ts,
                    reserved1
                ) = struct.unpack("<32s I I B B H Q 12s", entry_data)
                name_str = name_bytes.split(b'\x00')[0].decode()
                if name_str != filename:
                    continue
                if flag_field == 1:
                    print(f"File '{filename}' is deleted.")
                    return
                fs.seek(start_offset)
                data = fs.read(length)
                ext = Path(filename).suffix.lower()
                if ext in [".png", ".jpg", ".jpeg", ".bmp", ".gif"]:
                    temp_path = Path.cwd() / filename
                    temp_path.write_bytes(data)
                    output = climage.convert(temp_path, width=60)
                    print(output)
                    temp_path.unlink()
                else:
                    try:
                        if data.startswith(b'\xff\xfe'):
                            text = data.decode('utf-16')  # UTF-16
                        elif data.startswith(b'\xfe\xff'):
                            text = data.decode('utf-16')  # UTF-16
                        else:
                            try:
                                text = data.decode('utf-8')
                            except UnicodeDecodeError:
                                text = data.decode('utf-16-le')
                        print(text)
                    except UnicodeDecodeError:
                        print("Warning: File is not valid text. Raw bytes output:")
                        print(data)
                return
            print(f"File '{filename}' not found in filesystem.")


    def rem_file(self, fs_name: str, filename: str):
        fs_name = Path(fs_name)
        if not fs_name.exists():
            print(f"File system '{fs_name}' does not exist!")
            sys.exit(1)
        with fs_name.open("r+b") as fs:
            header_data = fs.read(self.HEADER_SIZE)
            header = list(struct.unpack(self.HEADER_FORMAT, header_data))
            table_offset = header[8]
            fs.seek(table_offset)
            for i in range(self.MAX_FILES):
                entry_pos = fs.tell()
                entry_data = fs.read(self.FILE_ENTRY_SIZE)
                if entry_data == b'\x00' * self.FILE_ENTRY_SIZE:
                    continue
                (name_bytes, start_offset, length, type_field, flag_field,
                 reserved0, created_ts, reserved1) = struct.unpack(self.FILE_ENTRY_FORMAT, entry_data)
                name_str = name_bytes.split(b"\x00")[0].decode(errors='ignore')
                if name_str == filename:
                    if flag_field == 1:
                        print(f"File '{filename}' is already deleted.")
                        return
                    # Flag the file as deleted (flag=1)
                    new_entry = struct.pack(
                        self.FILE_ENTRY_FORMAT,
                        name_bytes, start_offset, length, type_field, 1,
                        reserved0, created_ts, reserved1
                    )
                    fs.seek(entry_pos)
                    fs.write(new_entry)
                    # Update header: decrement active files, increment deleted
                    header[4] -= 1  # file_count
                    header[12] += 1  # deleted_files
                    fs.seek(0)
                    fs.write(struct.pack(self.HEADER_FORMAT, *header))
                    print(f"Flagged '{filename}' as deleted.")
                    return
            print(f"File '{filename}' not found in filesystem.")


    def list_fs(self, fs_name: str):
        fs_name = Path(fs_name)
        if not fs_name.exists():
            print(f"File system '{fs_name}' does not exist!")
            sys.exit(1)
        with fs_name.open("rb") as fs:
            header_data = fs.read(self.HEADER_SIZE)
            header = struct.unpack(self.HEADER_FORMAT, header_data)
            table_offset = header[8]
            print(f"Files in filesystem '{fs_name}':\n")
            fs.seek(table_offset)
            found_any = False
            for _ in range(self.MAX_FILES):
                entry_data = fs.read(self.FILE_ENTRY_SIZE)
                if entry_data == b'\x00' * self.FILE_ENTRY_SIZE:
                    continue
                (name_bytes, start_offset, length, type_field, flag_field,
                 reserved0, created_ts, reserved1) = struct.unpack(self.FILE_ENTRY_FORMAT, entry_data)
                if flag_field == 1:  # Skip deleted files
                    continue
                found_any = True
                name_str = name_bytes.split(b"\x00")[0].decode(errors='ignore')
                try:
                    timestr = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(created_ts))
                except (OSError, ValueError):
                    timestr = "invalid timestamp"
                print(f"- Name: {name_str:<32} | Size: {length:<8} bytes | Created: {timestr}")
            if not found_any:
                print("(no active files)")


    def defrag_fs(self, fs_name: str):
        fs_name = Path(fs_name)
        if not fs_name.exists():
            print(f"File system '{fs_name}' does not exist!")
            sys.exit(1)
        #Read all valid data into memory
        valid_files = []
        with fs_name.open("rb") as fs:
            header_data = fs.read(self.HEADER_SIZE)
            header = list(struct.unpack(self.HEADER_FORMAT, header_data))
            table_offset = header[8]
            data_start_offset = header[9]
            #Capture original values
            original_next_free_offset = header[10]
            files_to_remove = header[12]
            fs.seek(table_offset)
            for _ in range(self.MAX_FILES):
                entry_data = fs.read(self.FILE_ENTRY_SIZE)
                if not entry_data or entry_data == b'\x00' * self.FILE_ENTRY_SIZE:
                    continue
                entry = struct.unpack(self.FILE_ENTRY_FORMAT, entry_data)
                (name_bytes, start, length, type_f, flag_f, res0, created, res1) = entry
                if flag_f == 0 and not name_bytes.startswith(b'\x00'):
                    current_pos = fs.tell()
                    fs.seek(start)
                    file_data = fs.read(length)
                    fs.seek(current_pos)
                    valid_files.append({"entry": entry, "data": file_data})
        #Rewrite the file with compacted data
        with fs_name.open("r+b") as fs:
            current_data_offset = data_start_offset
            # Write new data blocks and build the new file table
            new_file_table = b''
            for i, file_info in enumerate(valid_files):
                original_entry = file_info['entry']
                data = file_info['data']
                length = original_entry[2]
                fs.seek(current_data_offset)
                fs.write(data)
                pad_len = (64 - (length % 64)) % 64
                if pad_len > 0:
                    fs.write(b'\x00' * pad_len)
                new_entry_tuple = (
                    original_entry[0], current_data_offset, length,
                    original_entry[3], original_entry[4], original_entry[5],
                    original_entry[6], original_entry[7]
                )
                new_file_table += struct.pack(self.FILE_ENTRY_FORMAT, *new_entry_tuple)
                current_data_offset += length + pad_len
            # Write the new, compacted file table
            fs.seek(table_offset)
            fs.write(new_file_table)
            # Clear any remaining old entries in the file table
            remaining_table_space = (self.MAX_FILES - len(valid_files)) * self.FILE_ENTRY_SIZE
            if remaining_table_space > 0:
                fs.write(b'\x00' * remaining_table_space)
            # Update header
            header[4] = len(valid_files)
            header[10] = current_data_offset
            header[12] = 0
            fs.seek(0)
            fs.write(struct.pack(self.HEADER_FORMAT, *header))
            fs.truncate(current_data_offset)
            bytes_freed = original_next_free_offset - current_data_offset
            print(f"Defragmentation complete for '{fs_name}':")
            print(f"- Files removed: {files_to_remove}")
            print(f"- Files remaining: {len(valid_files)}")
            print(f"- Bytes freed: {bytes_freed}")
            print(f"- New next free offset: {current_data_offset}")


if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("Usage:")
        print("  mkfs <file>")
        print("  gifs <file>")
        print("  lsfs <file>")
        print("  addfs <filesystem> <file_to_add>")
        print("  getfs <filesystem> <filename_to_get>")
        print("  catfs <filesystem> <filename_to_cat>")
        print("  rmfs <filesystem> <filename_to_remove>")
        print("  dfrgfs <filesystem>")
        sys.exit(1)

    cmd = sys.argv[1]
    fs_manager = ZestFileSystem(sys.argv[2])

    if cmd == "mkfs":
        fs_manager.create_new_fs(sys.argv[2])
    elif cmd == "gifs":
        fs_manager.get_info_fs(sys.argv[2])
    elif cmd == "addfs":
        if len(sys.argv) < 4:
            print("Usage: addfs <filesystem> <filepath>")
            sys.exit(1)
        fs_manager.add_file(sys.argv[2], sys.argv[3])
    elif cmd == "catfs":
        if len(sys.argv) < 4:
            print("Usage: catfs <filesystem> <filename>")
            sys.exit(1)
        fs_manager.cat_file(sys.argv[2], sys.argv[3])
    elif cmd == "getfs":
        if len(sys.argv) < 4:
            print("Usage: getfs <filesystem> <filename>")
            sys.exit(1)
        fs_manager.get_file(sys.argv[2], sys.argv[3])
    elif cmd == "rmfs":
        if len(sys.argv) < 4:
            print("Usage: rmfs <filesystem> <filename>")
            sys.exit(1)
        fs_manager.rem_file(sys.argv[2], sys.argv[3])
    elif cmd == "lsfs":
        fs_manager.list_fs(sys.argv[2])
    elif cmd == "dfrgfs":
        if len(sys.argv) < 3:
            print("Usage: dfrgfs <filesystem>")
            sys.exit(1)
        fs_manager.defrag_fs(sys.argv[2])
    else:
        print(f"Unknown command: '{cmd}'")
        sys.exit(1)