# Step 01 - Python

__Prompts in Google Gemini:__
- I have created a filesystem-file with some entries. How can I read the binary data (like for example a .jpg) and show the output as a picture in the commandline?
- Give me a brief introducion about the struct module in python, including its methods

## Commands and Terminal Output for Python:

__1. Create a new filesystem called filesystem1.zvfs:__
- python.exe zvfs.py mkfs filesystem1.zvfs
```
Created a new filesystem 'filesystem1.zvfs' with capacity for 32 files.
```

__2. Create two test text files:__
- echo Hello, world! > test_file1.txt
- echo The weather is nice today > test_file2.txt

__3. Add files to filesystem:__
- python zvfs.py addfs filesystem1.zvfs example_data\test_file1.txt
- python zvfs.py addfs filesystem1.zvfs example_data\test_file2.txt
- python zvfs.py addfs filesystem1.zvfs example_data\images.jpg
- python zvfs.py addfs filesystem1.zvfs example_data\images2.jpg
```
Added 'test_file1.txt' (28 bytes, padded to 64 bytes) at offset 2112.
----------------------------------------------
Added 'test_file2.txt' (25 bytes, padded to 64 bytes) at offset 2176.
----------------------------------------------
Added 'images.jpg' (3642 bytes, padded to 3648 bytes) at offset 2240.
----------------------------------------------
Added 'images2.jpg' (5893 bytes, padded to 5952 bytes) at offset 5888.
```

__4. List all filesystem files:__
- python zvfs.py lsfs filesystem1.zvfs
```
- Name: test_file1.txt                   | Size: 28       bytes | Created: 2025-11-28 09:55:55
- Name: test_file2.txt                   | Size: 25       bytes | Created: 2025-11-28 09:56:12
- Name: images.jpg                       | Size: 3642     bytes | Created: 2025-11-28 09:56:35
- Name: images2.jpg                      | Size: 5893     bytes | Created: 2025-11-28 09:56:48
```

__5. Print contents of test file1.txt from the filesystem:__
- python zvfs.py catfs filesystem1.zvfs test_file1.txt
```
Hello, World!
```
> ![alt text](image-1.png)

__6. Delete file test file1.txt from your disk, and restore it from the filesystem:__
- rm test_file1.txt
- python zvfs.py getfs filesystem1.zvfs test_file1.txt
```
Extracted 'test_file1.txt' to '...\HS25_SoCo_group_040-a3\test_file1.txt' with (28 bytes).
```

__7. Get the information of the filesystem:__
- python zvfs.py gifs filesystem1.zvfs
```
File system: filesystem1.zvfs
Magic: ZVFSDSK1
Version: 1
Files present: 4
Free entries: 28
Deleted files: 0
Total size: 11840 bytes
```

__8. Delete test file1.txt from the filesystem, and then get the information of the filesystem and list all
filesystem files:__
- python zvfs.py rmfs filesystem1.zvfs test_file1.txt
- python zvfs.py gifs filesystem1.zvfs
- python zvfs.py lsfs filesystem1.zvfs

```
Flagged 'test_file1.txt' as deleted.
----------------------------------------------
File system: filesystem1.zvfs
Magic: ZVFSDSK1
Version: 1
Files present: 3
Free entries: 29
Deleted files: 1
Total size: 11840 bytes
----------------------------------------------
- Name: test_file2.txt                   | Size: 25       bytes | Created: 2025-11-28 09:56:12
- Name: images.jpg                       | Size: 3642     bytes | Created: 2025-11-28 09:56:35
- Name: images2.jpg                      | Size: 5893     bytes | Created: 2025-11-28 09:56:48

```
__9. Defragment the filesystem, and then get the information of the filesystem and list all filesystem files:__
- python zvfs.py dfrgfs filesystem1.zvfs
- python zvfs.py gifs filesystem1.zvfs
- python zvfs.py lsfs filesystem1.zvfs
```
Defragmentation complete for 'filesystem1.zvfs':
- Files removed: 1
- Files remaining: 3
- Bytes freed: 64
- New next free offset: 11776
----------------------------------------------
File system: filesystem1.zvfs
Magic: ZVFSDSK1
Version: 1
Files present: 3
Free entries: 29
Deleted files: 0
Total size: 11776 bytes
----------------------------------------------
- Name: test_file2.txt                   | Size: 25       bytes | Created: 2025-11-28 09:56:12
- Name: images.jpg                       | Size: 3642     bytes | Created: 2025-11-28 09:56:35
- Name: images2.jpg                      | Size: 5893     bytes | Created: 2025-11-28 09:56:48
```
<br>
<br>

# Step 02 - Java

- how to copy fixed size of bytes in java
- teach me the basics of bytebuffer in java
- help me with structured read and write in headers, still only using byte buffer in "..."
- alternative of python's "with open" read write in java
- teach me the basics of FileChannel
in java how to write specific byte offsets inside one big file using byte buffer
- in python we create the entry object as in "...", what would be the corresponding thing in java
- how to open a file for reading and writing in java using file channel
- how to read 64 bytes from file channel at a specific offset with ByteBuffer
- In my code "..." I have the header reading too many times, how can I avoid the repetitive header calls?
- How to create and the command options in the command in a custom java code
- How to avoid the repetitive header access in this code "..."
- walk me through intuitively what steps are needed to immplement the defragmentation as explained in ""

## Commands and Terminal Output for Java

1. **Create**
   java zvfs mkfs filesystem2.zvfs

2. **Text files**
   echo 'Hello, world!' > test_file1.txt
   echo 'The weather is nice today' > test_file2.txt

3. **Add files**
   java zvfs addfs filesystem2.zvfs test_file1.txt
   java zvfs addfs filesystem2.zvfs test_file2.txt

4. **List**
   java zvfs lsfs filesystem2.zvfs

    Output:
```
*****LSFS*****
name: test_file1.txt
size: 14
created: Wed Nov 26 15:08:02 CET 2025
*****LSFS*****
name: test_file2.txt
size: 26
created: Wed Nov 26 15:08:06 CET 2025
```

5. **Contents**
   java zvfs catfs filesystem2.zvfs test_file1.txt

```
Hello, world!
```

6. **Remove and get**
   rm test_file1.txt
   java zvfs getfs filesystem2.zvfs test_file1.txt

7. **Get**
   java zvfs gifs filesystem2.zvfs

```
*****GIFS*****
name: filesystem2.zvfs
number of files present: 2
remaining free entries: 30
Deleted files - marked: 0
Total size: 2202
```

8. **Remove, get, list**
   java zvfs rmfs filesystem2.zvfs test_file1.txt
   java zvfs gifs filesystem2.zvfs
   java zvfs lsfs filesystem2.zvfs

```
*****LSFS*****
name: test_file2.txt
size: 26
created: Wed Nov 26 15:08:06 CET 2025
```

9. **Defragment, get, list**
   java zvfs dfrgfs filesystem2.zvfs
   java zvfs gifs filesystem2.zvfs
   java zvfs lsfs filesystem2.zvfs

```
# 1defragmented files, empty 26 bytes
*****GIFS*****
name: filesystem2.zvfs
number of files present: 1
remaining free entries: 31
Deleted files - marked: 0
Total size: 2138
*****LSFS*****
name: test_file2.txt
size: 26
created: Wed Nov 26 15:08:06 CET 2025
```
