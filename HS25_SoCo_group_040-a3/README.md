## Step 02 - Java

how to copy fixed size of bytes in java
teach me the basics of bytebuffer in java
help me with structured read and write in headers, still only using byte buffer in "..."
alternative of python's "with open" read write in java
teach me the basics of FileChannel
in java how to write specific byte offsets inside one big file using byte buffer
in python we create the entry object as in "...", what would be the corresponding thing in java
how to open a file for reading and writing in java using file channel
how to read 64 bytes from file channel at a specific offset with ByteBuffer
In my code "..." I have the header reading too many times, how can I avoid the repetitive header calls?
How to create and the command options in the command in a custom java code
How to avoid the repetitive header access in this code "..."
walk me through intuitively what steps are needed to immplement the defragmentation as explained in ""

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
