# rusted-in-the-air
## What the heck?
- [rusted from the rain](https://www.youtube.com/watch?v=RAOnUF8t20w)
- "in the air" => something uncertain
- todo: [learn and rewrite in Rust](https://www.rust-lang.org/)


## Why
Some scripts to find inconsistencies on a system:

dpkg.py: 
```
    What the hack? Detect changes of installed packages!
    1. get all installed packages with dpkg -l
    2. for every installed package there are files in /var/lib/dpkg/info/pkg-name*
        root@debian-9:~# cat /var/lib/dpkg/info/openssh-server.md5sums
        6e73ff3237d90dd7368d8a6d0fad5221  lib/systemd/system/ssh.service
        3f25171928b9546beb6a67bf51694eb3  lib/systemd/system/ssh.socket
        ...
    3. check md5("/lib/systemd/system/ssh.service") == 6e73ff3237d90dd7368d8a6d0fad5221 ?
```

lauf.py
```
    python lauf.py <file abs> <root dir>"
    -  Run recursively throuth <root dir>
    -  save owner, group, permissions and md5 sum of each file/directory to <file abs>  (json)
```

geh.py
```
  python geh.py <json1> <json2>
  - Take two outputs from lauf.py
  - Compare two systems (md5 sums, permissoins, ...)
  ```
  
## Use cases
Forensics: Someone overwrite a binary or so or pam module, ...
Privilege Escalation: Find a misconfiguration (chmod 777, setuid, in general: which files changed from default)

## TODO
 - build a test system based vuln box (dpkg -l)  
 - Rewrite in Rust to learn rust  

