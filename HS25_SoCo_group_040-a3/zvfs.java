
import java.io.IOException;
import java.nio.ByteBuffer;
import java.nio.ByteOrder;
import java.nio.channels.FileChannel;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.nio.file.StandardOpenOption;

// – Creating a new .zvfs file: mkfs.
// – Get info about a .zvfs file: gifs.
// – Adding files to the .zvfs file: addfs.
// – Extracting files from the .zvfs file: getfs. 
// – Removing files from the .zvfs file: rmfs.
// – Listing the files contained in the .zvfs file: lsfs. – Defragmenting the .zvfs file: dfrgfs.
// – Viewing files in the .zvfs file: catfs.

// requirements...
// all commands should check if the provided file system or file exist
// provide a respective error message in case the file names are empty or point to non-existant files.

// prompts used:
//how to copy fixed size of bytes in java
//in java how to write specific byte offsets inside one big file using byte buffer
//in python we create the entry object as in "...", what would be the corresponding thing in java
//how to open a file for reading and writing in java using file channel
//how to read 64 bytes from file channel at a specific offset with ByteBuffer


class Zvfs {

    static void mkfs(String filename) throws IOException {
        Path p = Paths.get(filename);
        if (Files.exists(p)) {
            System.err.println("Cannot create file, file with the same name already exists!!!!!");
            return;
        }

        try (FileChannel fc = openRW(filename)) {
            int headerSize = 64;
            int fileSize = 64;
            int maxNoOfFiles = 32;

            ByteBuffer header = ByteBuffer.allocate(headerSize);
            header.order(ByteOrder.LITTLE_ENDIAN);

            byte[] magicBytes = "ZVFSDSK1".getBytes(StandardCharsets.US_ASCII);
            byte[] magicBuf = new byte[8];
            System.arraycopy(magicBytes, 0, magicBuf, 0, 8);
            header.put(magicBuf);

            header.put((byte)1);
            header.put((byte)0);
            header.putShort((short)0);
            header.putShort((short)0);
            header.putShort((short)maxNoOfFiles);
            header.putShort((short)fileSize);
            header.putShort((short)0);

            header.putInt(headerSize);

            int dataStart = headerSize + maxNoOfFiles * fileSize;
            header.putInt(dataStart);
            header.putInt(dataStart);
            header.putInt(0);
            header.putShort((short)0);
            header.put(new byte[26]);

            header.flip();
            fc.position(0);
            fc.write(header);

            ByteBuffer entries = ByteBuffer.allocate(maxNoOfFiles * fileSize);
            entries.order(ByteOrder.LITTLE_ENDIAN);
            while (entries.hasRemaining()) {
                entries.put((byte)0);
            }
            entries.flip();

            fc.position(headerSize);
            fc.write(entries);
        }
    }

    private static FileChannel openRW(String filename) throws IOException {
        return FileChannel.open(
                Paths.get(filename),
                StandardOpenOption.CREATE,
                StandardOpenOption.READ,
                StandardOpenOption.WRITE
        );
    }

    static class FileEntry {
        String name;
        int start;
        int length;
        byte type;
        boolean deleted;
        long created;
    }

    static FileEntry readEntry(FileChannel fc, int index, int headerSize, int fileSize) throws IOException {
        long offset = headerSize + (long) index * fileSize;
        ByteBuffer buf = ByteBuffer.allocate(fileSize);
        buf.order(ByteOrder.LITTLE_ENDIAN);

        fc.position(offset);
        int read = fc.read(buf);
        if (read != fileSize) {
            return null;
        }

        buf.flip();
        byte[] nameBytes = new byte[32];
        buf.get(nameBytes);
        int start = buf.getInt();
        int length = buf.getInt();
        byte type = buf.get();
        byte flag = buf.get();
        buf.getShort();
        long created = buf.getLong();
        byte[] r1 = new byte[12];
        buf.get(r1);

        boolean allZero = true;
        for (int i = 0; i < nameBytes.length; i++) {
            if (nameBytes[i] != 0) {
                allZero = false;
                break;
            }
        }
        String name = allZero? "": new String(nameBytes, StandardCharsets.UTF_8).split("\0", 2)[0];

        FileEntry e = new FileEntry();
        e.name = name;
        e.start = start;
        e.length = length;
        e.type = type;
        e.deleted = (flag == 1);
        e.created = created;
        return e;
    }

    static void writeEntry(FileChannel fc, int index, int headerSize, int fileSize, FileEntry e) throws IOException {
        long offset = headerSize + (long) index * fileSize;
        ByteBuffer buf = ByteBuffer.allocate(fileSize);
        buf.order(ByteOrder.LITTLE_ENDIAN);

        byte[] nameBytes = new byte[32];
        byte[] src = e.name == null ? new byte[0] : e.name.getBytes(StandardCharsets.UTF_8);
        int len = Math.min(31, src.length);
        System.arraycopy(src, 0, nameBytes, 0, len);

        buf.put(nameBytes);
        buf.putInt(e.start);
        buf.putInt(e.length);
        buf.put(e.type);
        buf.put((byte)(e.deleted ? 1 : 0));
        buf.putShort((short)0);
        buf.putLong(e.created);
        buf.put(new byte[12]);

        buf.flip();
        fc.position(offset);
        fc.write(buf);
    }
}
