import java.io.IOException;
import java.nio.ByteBuffer;
import java.nio.ByteOrder;
import java.nio.channels.FileChannel;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.OpenOption;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.nio.file.StandardCopyOption;
import java.nio.file.StandardOpenOption;
import java.util.ArrayList;
import java.util.Date;

public class zvfs { 
   public zvfs() {
   }

   static class Header {
      byte[] magic;
      byte version;
      byte flags;
      short reserved0;
      short fileCount;
      short fileCapacity;
      short fileEntrySize;
      short reserved1;
      int fileTableOffset;
      int dataStartOffset;
      int nextFreeOffset;
      int freeEntryOffset;
      short deletedFiles;
      byte[] reserved2;
   }

   static Header readHeader(FileChannel channel) throws IOException {
      System.out.println("reading header...");
      int headerSize = 64;
      ByteBuffer buffer = ByteBuffer.allocate(headerSize);
      buffer.order(ByteOrder.LITTLE_ENDIAN);
      channel.position(0L);

      int bytesRead = channel.read(buffer);
      if (bytesRead != headerSize) {
         throw new IOException("Could not read");
      }

      buffer.flip();
      Header header = new Header();
      header.magic = new byte[8];
      buffer.get(header.magic);
      header.version = buffer.get();
      header.flags = buffer.get();
      header.reserved0 = buffer.getShort();
      header.fileCount = buffer.getShort();
      header.fileCapacity = buffer.getShort();
      header.fileEntrySize = buffer.getShort();
      header.reserved1 = buffer.getShort();
      header.fileTableOffset = buffer.getInt();
      header.dataStartOffset = buffer.getInt();
      header.nextFreeOffset = buffer.getInt();
      header.freeEntryOffset = buffer.getInt();
      header.deletedFiles = buffer.getShort();
      header.reserved2 = new byte[26];
      buffer.get(header.reserved2);
      return header;
   }

   static void writeHeader(FileChannel channel, Header header) throws IOException {
      System.out.println("writing header...");
      int headerSize = 64;
      ByteBuffer buffer = ByteBuffer.allocate(headerSize);
      buffer.order(ByteOrder.LITTLE_ENDIAN);
      buffer.put(header.magic);
      buffer.put(header.version);
      buffer.put(header.flags);
      buffer.putShort(header.reserved0);
      buffer.putShort(header.fileCount);
      buffer.putShort(header.fileCapacity);
      buffer.putShort(header.fileEntrySize);
      buffer.putShort(header.reserved1);
      buffer.putInt(header.fileTableOffset);
      buffer.putInt(header.dataStartOffset);
      buffer.putInt(header.nextFreeOffset);
      buffer.putInt(header.freeEntryOffset);
      buffer.putShort(header.deletedFiles);
      buffer.put(header.reserved2);
      buffer.flip();
      channel.position(0L);
      channel.write(buffer);
   }

   static void mkfs(String filesystemName) throws Exception {
      System.out.println("mkfs starting...");
      Path filePath = Paths.get(filesystemName);
      if (Files.exists(filePath)) {
         System.err.println("File with the name already exists!!!!!");
      } else {
         FileChannel channel = FileChannel.open(Paths.get(filesystemName),
                 StandardOpenOption.CREATE,
                 StandardOpenOption.READ,
                 StandardOpenOption.WRITE);

         try {
            byte headerSize = 64;
            byte fileEntrySize = 64;
            byte fileCapacity = 32;
            ByteBuffer headerBuffer = ByteBuffer.allocate(headerSize);
            headerBuffer.order(ByteOrder.LITTLE_ENDIAN);
            byte[] magicAscii = "ZVFSDSK1".getBytes(StandardCharsets.US_ASCII);
            byte[] magicBytes = new byte[8];
            System.arraycopy(magicAscii, 0, magicBytes, 0, 8);
            headerBuffer.put(magicBytes);
            headerBuffer.put((byte)1);
            headerBuffer.put((byte)0);
            headerBuffer.putShort((short)0);
            headerBuffer.putShort((short)0);
            headerBuffer.putShort((short)fileCapacity);
            headerBuffer.putShort((short)fileEntrySize);
            headerBuffer.putShort((short)0);
            headerBuffer.putInt(headerSize);
            int dataStartOffset = headerSize + fileCapacity * fileEntrySize;
            headerBuffer.putInt(dataStartOffset);
            headerBuffer.putInt(dataStartOffset);
            headerBuffer.putInt(0);
            headerBuffer.putShort((short)0);
            headerBuffer.put(new byte[26]);
            headerBuffer.flip();
            channel.position(0L);
            channel.write(headerBuffer);
            ByteBuffer entryRegionBuffer = ByteBuffer.allocate(fileCapacity * fileEntrySize);
            entryRegionBuffer.order(ByteOrder.LITTLE_ENDIAN);

            while(true) {
               if (!entryRegionBuffer.hasRemaining()) {
                  entryRegionBuffer.flip();
                  channel.position((long)headerSize);
                  channel.write(entryRegionBuffer);
                  break;
               }

               entryRegionBuffer.put((byte)0);
            }
         } catch (Exception e) {
            throw new Exception("---------sth wrong: ", e);
         }
      }
   }

   static FileEntry readEntry(FileChannel channel, int entryIndex, int tableOffset, int entrySize) throws IOException {
      long position = (long)tableOffset + (long)entryIndex * (long)entrySize;
      ByteBuffer buffer = ByteBuffer.allocate(entrySize);
      buffer.order(ByteOrder.LITTLE_ENDIAN);
      channel.position(position);
      int bytesRead = channel.read(buffer);
      if (bytesRead != entrySize) {
         return null;
      } else {
         buffer.flip();
         byte[] nameBytes = new byte[32];
         buffer.get(nameBytes);
         int start = buffer.getInt();
         int length = buffer.getInt();
         byte type = buffer.get();
         byte deletedFlag = buffer.get();
         buffer.getShort();
         long created = buffer.getLong();
         byte[] reservedBytes = new byte[12];
         buffer.get(reservedBytes);
         boolean allZero = true;

         for(int i = 0; i < nameBytes.length; ++i) {
            if (nameBytes[i] != 0) {
               allZero = false;
               break;
            }
         }

         String fileName = allZero ? "" : (new String(nameBytes, StandardCharsets.UTF_8)).split("\u0000", 2)[0];
         FileEntry entry = new FileEntry();
         entry.name = fileName;
         entry.start = start;
         entry.length = length;
         entry.type = type;
         entry.deleted = deletedFlag == 1;
         entry.created = created;
         return entry;
      }
   }

   static void writeEntry(FileChannel channel, int entryIndex, int tableOffset, int entrySize, FileEntry entry) throws IOException {
      long position = (long)tableOffset + (long)entryIndex * (long)entrySize;
      ByteBuffer buffer = ByteBuffer.allocate(entrySize);
      buffer.order(ByteOrder.LITTLE_ENDIAN);
      byte[] nameBytes = new byte[32];
      byte[] encodedName = entry.name == null ? new byte[0] : entry.name.getBytes(StandardCharsets.UTF_8);
      int copyLength = Math.min(31, encodedName.length);
      System.arraycopy(encodedName, 0, nameBytes, 0, copyLength);
      buffer.put(nameBytes);
      buffer.putInt(entry.start);
      buffer.putInt(entry.length);
      buffer.put(entry.type);
      buffer.put((byte)(entry.deleted ? 1 : 0));
      buffer.putShort((short)0);
      buffer.putLong(entry.created);
      buffer.put(new byte[12]);
      buffer.flip();
      channel.position(position);
      channel.write(buffer);
   }

   static void gifs(String filesystemName) throws IOException {
      Path filePath = Paths.get(filesystemName);
      if (!Files.exists(filePath)) {
         System.err.println("Does not exist!!!!");
      } else {
         FileChannel channel = FileChannel.open(filePath, StandardOpenOption.READ);

         try {
            Header header = readHeader(channel);
            // String magic = new String(header.magic, StandardCharsets.US_ASCII);
            long size = Files.size(filePath);
            int remaining = header.fileCapacity - header.fileCount - header.deletedFiles;
            System.out.println("*****GIFS*****");
            System.out.println("name: " + filesystemName);
            System.out.println("number of files present: " + (header.fileCount - header.deletedFiles));
            System.out.println("remaining free entries: " + remaining);
            System.out.println("Deleted files - marked: " + header.deletedFiles);
            System.out.println("Total size: " + size);
         } finally {
            if (channel != null) {
               channel.close();
            }
         }
      }
   }

   static void lsfs(String filesystemName) throws IOException {
      Path filePath = Paths.get(filesystemName);
      if (!Files.exists(filePath)) {
         System.err.println("Does not exist!!!!");
      } else {
         FileChannel channel = FileChannel.open(filePath, StandardOpenOption.READ);

         try {
            Header header = readHeader(channel);
            for(int i = 0; i < header.fileCapacity; ++i) {
               FileEntry entry = readEntry(channel, i, header.fileTableOffset, header.fileEntrySize);
               if (entry != null && entry.name != null && !entry.name.isEmpty() && !entry.deleted) {
                  Date date = new Date(entry.created * 1000L);
                  System.out.println("*****LSFS*****");
                  System.out.println("name: " + entry.name);
                  System.out.println("size: " + entry.length);
                  System.out.println("created: " + date);
               }
            }
         } finally {
            if (channel != null) {
               channel.close();
            }
         }
      }
   }

   static void rmfs(String filesystemName, String fileName) throws IOException {
      if (fileName != null && !fileName.isEmpty()) {
         Path filePath = Paths.get(filesystemName);
         if (!Files.exists(filePath)) {
            System.err.println("Does not exist");
         } else {
            FileChannel channel = FileChannel.open(Paths.get(filesystemName),
                    StandardOpenOption.CREATE,
                    StandardOpenOption.READ,
                    StandardOpenOption.WRITE);

            try {
               Header header = readHeader(channel);
               int targetIndex = -1;
               FileEntry targetEntry = null;

               for(int i = 0; i < header.fileCapacity; ++i) {
                  FileEntry candidate = readEntry(channel, i, header.fileTableOffset, header.fileEntrySize);
                  if (candidate != null && candidate.name != null && !candidate.name.isEmpty() && !candidate.deleted && candidate.name.equals(fileName)) {
                     targetIndex = i;
                     targetEntry = candidate;
                     break;
                  }
               }

               if (targetIndex != -1 && targetEntry != null) {
                  targetEntry.deleted = true;
                  writeEntry(channel, targetIndex, header.fileTableOffset, header.fileEntrySize, targetEntry);
                  header.fileCount--;
                  header.deletedFiles++;
                  header.flags = 0;
                  writeHeader(channel, header);
               } else {
                  System.err.println("FFNF!!");
               }
            } finally {
               if (channel != null) {
                  channel.close();
               }
            }
         }
      } else {
         System.err.println("Invvalid");
      }
   }

   static void addfs(String filesystemName, String sourceName) throws IOException {
      if (sourceName != null && !sourceName.isEmpty()) {
         Path filePath = Paths.get(filesystemName);
         if (!Files.exists(filePath)) {
            System.err.println("does not exist");
         } else {
            Path sourceFilePath = Paths.get(sourceName);
            if (!Files.exists(sourceFilePath)) {
               System.err.println("Source does not exist!!");
            } else {
               FileChannel channel = FileChannel.open(Paths.get(filesystemName),
                       StandardOpenOption.CREATE,
                       StandardOpenOption.READ,
                       StandardOpenOption.WRITE);

               try {
                  Header header = readHeader(channel);
                  if (header.fileCount + header.deletedFiles >= header.fileCapacity) {
                     System.err.println("No free slots");
                     return;
                  }

                  int freeIndex = -1;

                  for(int i = 0; i < header.fileCapacity; ++i) {
                     FileEntry candidate = readEntry(channel, i, header.fileTableOffset, header.fileEntrySize);
                     if (candidate == null || candidate.name == null || candidate.name.isEmpty() || candidate.deleted) {
                        freeIndex = i;
                        break;
                     }
                  }

                  if (freeIndex == -1) {
                     System.err.println("No free entry slots");
                     return;
                  }

                  byte[] fileData = Files.readAllBytes(sourceFilePath);
                  int alignedStart = (header.nextFreeOffset + 63) / 64 * 64;
                  ByteBuffer dataBuffer = ByteBuffer.wrap(fileData);
                  channel.position((long)alignedStart);

                  while(dataBuffer.hasRemaining()) {
                     channel.write(dataBuffer);
                  }

                  FileEntry newEntry = new FileEntry();
                  newEntry.name = sourceFilePath.getFileName().toString();
                  newEntry.start = alignedStart;
                  newEntry.length = fileData.length;
                  newEntry.type = 0;
                  newEntry.deleted = false;
                  newEntry.created = System.currentTimeMillis() / 1000L;
                  writeEntry(channel, freeIndex, header.fileTableOffset, header.fileEntrySize, newEntry);
                  header.fileCount++;
                  header.nextFreeOffset = alignedStart + fileData.length;
                  header.flags = (byte)((header.fileCount + header.deletedFiles >= header.fileCapacity) ? 1 : 0);
                  writeHeader(channel, header);
               } finally {
                  if (channel != null) {
                     channel.close();
                  }
               }
            }
         }
      } else {
         System.err.println("Invalid");
      }
   }

   static void getfs(String filesystemName, String fileName) throws IOException {
      if (fileName != null && !fileName.isEmpty()) {
         Path filePath = Paths.get(filesystemName);
         if (!Files.exists(filePath)) {
            System.err.println("-does not exist");
         } else {
            FileChannel channel = FileChannel.open(filePath, StandardOpenOption.READ);

            try {
               Header header = readHeader(channel);
               FileEntry target = null;

               for(int i = 0; i < header.fileCount; ++i) {
                  FileEntry candidate = readEntry(channel, i, header.fileTableOffset, header.fileEntrySize);
                  if (candidate != null && candidate.name != null && !candidate.name.isEmpty() && !candidate.deleted && candidate.name.equals(fileName)) {
                     target = candidate;
                     break;
                  }
               }

               if (target != null) {
                  ByteBuffer dataBuffer = ByteBuffer.allocate(target.length);
                  channel.position((long)target.start);
                  int bytesRead = channel.read(dataBuffer);
                  if (bytesRead != target.length) {
                     System.err.println("Could not read file!!");
                     return;
                  }

                  dataBuffer.flip();
                  byte[] fileBytes = new byte[target.length];
                  dataBuffer.get(fileBytes);
                  Files.write(Paths.get(target.name), fileBytes, new OpenOption[0]);
               } else {
                  System.err.println("Not found!!!!");
               }
            } finally {
               if (channel != null) {
                  channel.close();
               }
            }
         }
      } else {
         System.err.println("Invalid--");
      }
   }

   static void catfs(String fsPath, String fileName) throws IOException {
      if (fileName == null || fileName.isEmpty()) {
         System.err.println("Invalid--");
         return;
      }

      Path fs = Paths.get(fsPath);
      if (!Files.exists(fs)) {
         System.err.println("--Does not exist!!");
         return;
      }

      try (FileChannel ch = FileChannel.open(fs, StandardOpenOption.READ)) {
         Header header = readHeader(ch);
         FileEntry target = null;
         for (int i = 0; i < header.fileCapacity; i++) {
            FileEntry e = readEntry(ch, i, header.fileTableOffset, header.fileEntrySize);
            if (e != null && e.name != null && !e.name.isEmpty() && !e.deleted && e.name.equals(fileName)) {
               target = e;
               break;
            }
         }

         if (target == null) {
            System.err.println("FNF!!");
            return;
         }

   ByteBuffer dataBuf = ByteBuffer.allocate(target.length);
   ch.position((long) target.start);
   int bytesRead = ch.read(dataBuf);
   if (bytesRead != target.length) {
      System.err.println("--DBG!");
      return;
   }
   dataBuf.flip();
   byte[] data = new byte[target.length];
   dataBuf.get(data);
   String content = new String(data, StandardCharsets.UTF_8);
   System.out.print(content);

      }
   }

   static void dfrgfs(String fsPath) throws Exception {
      /// DEFRAGMENTATION logic ---- MOSTLY WITH CHATGPT!, see readme
      Path src = Paths.get(fsPath);
      if (!Files.exists(src)) {
         System.err.println("does not exist");
         return;
      }

      try (FileChannel in = FileChannel.open(src, StandardOpenOption.READ)) {
         Header header = readHeader(in);
         if (header.deletedFiles == 0) {
            System.out.println("defragmented 0 files, freed 0 bytes");
            return;
         }

         ArrayList<FileEntry> active = new ArrayList<>();
         for (int i = 0; i < header.fileCapacity; i++) {
            FileEntry e = readEntry(in, i, header.fileTableOffset, header.fileEntrySize);
            if (e != null && e.name != null && !e.name.isEmpty() && !e.deleted) {
               active.add(e);
            }
         }

         long oldUsed = (long) header.nextFreeOffset - (long) header.dataStartOffset;

         String tmpName = fsPath + ".tmp";
         Path tmpPath = Paths.get(tmpName);
         Files.deleteIfExists(tmpPath);
         mkfs(tmpName);

         try (FileChannel out = FileChannel.open(Paths.get(tmpName),
                 StandardOpenOption.CREATE,
                 StandardOpenOption.READ,
                 StandardOpenOption.WRITE)) {

            Header tempHeader = readHeader(out);
            int writePos = tempHeader.dataStartOffset;
            int index = 0;

            for (FileEntry e : active) {
               int aligned = ((writePos + 63) / 64) * 64;
               ByteBuffer dataBuf = ByteBuffer.allocate(e.length);
               in.position((long) e.start);
               int read = in.read(dataBuf);
               if (read != e.length) {
                  System.err.println("Error reading file data during defrag");
                  return;
               }
               dataBuf.flip();
               out.position((long) aligned);
               while (dataBuf.hasRemaining()) {
                  out.write(dataBuf);
               }
               FileEntry ne = new FileEntry();
               ne.name = e.name;
               ne.start = aligned;
               ne.length = e.length;
               ne.type = e.type;
               ne.deleted = false;
               ne.created = e.created;
               writeEntry(out, index, tempHeader.fileTableOffset, tempHeader.fileEntrySize, ne);
               index++;
               writePos = aligned + e.length;
            }

            tempHeader.fileCount = (short) active.size();
            tempHeader.deletedFiles = 0;
            tempHeader.nextFreeOffset = ((writePos + 63) / 64) * 64;
            tempHeader.flags = (byte) ((tempHeader.fileCount == tempHeader.fileCapacity) ? 1 : 0);
            writeHeader(out, tempHeader);

            long newUsed = (long) tempHeader.nextFreeOffset - (long) tempHeader.dataStartOffset;
            long freed = oldUsed - newUsed;

            Files.move(tmpPath, src, StandardCopyOption.REPLACE_EXISTING);
            System.out.println("# " + header.deletedFiles + "defragmented files, empty " + freed + " bytes");
         }
      }
   }

   public static void main(String[] args) throws Exception {
      if (args.length < 1) {
         System.err.println("Needs args!!");
      } else {
         switch (args[0]) {
            case "mkfs":
               mkfs(args[1]);
               break;
            case "gifs":
               gifs(args[1]);
               break;
            case "lsfs":
               lsfs(args[1]);
               break;
            case "rmfs":
               rmfs(args[1], args[2]);
               break;
            case "addfs":
               addfs(args[1], args[2]);
               break;
            case "getfs":
               getfs(args[1], args[2]);
               break;
            case "catfs":
               catfs(args[1], args[2]);
               break;
            case "dfrgfs":
               dfrgfs(args[1]);
               break;
            default:
               System.err.println("Unknown command!!!");
         }

      }
   }

   static class FileEntry {
      String name;
      int start;
      int length;
      byte type;
      boolean deleted;
      long created;

      FileEntry() {
      }
   }
}
