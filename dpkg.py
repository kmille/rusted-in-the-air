#!/usr/bin/env python
"""
    What the hack? Detect changes of installed packages!
    1. get all installed packages with dpkg -l
    2. for every installed package there are files in /var/lib/dpkg/info/pkg-name*
        root@debian-9:~# cat /var/lib/dpkg/info/openssh-server.md5sums
        6e73ff3237d90dd7368d8a6d0fad5221  lib/systemd/system/ssh.service
        3f25171928b9546beb6a67bf51694eb3  lib/systemd/system/ssh.socket
        ...
    3. check md5("/lib/systemd/system/ssh.service") == 6e73ff3237d90dd7368d8a6d0fad5221 ?

    This does not work always: /etc/ssh/sshd_config is generated dynamically by /var/lib/dpkg/info/openssh-server.postinst
    This code runs under python2 and python3.
"""


import subprocess
import os
import hashlib


cmd_all_pkgs = "dpkg -l | grep ii | cut -d ' ' -f 3"
dpkg_info_base = "/var/lib/dpkg/info/"


def cmd(cmd):
    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    p.wait()
    return p.communicate()[0].decode()


for pkg in cmd(cmd_all_pkgs).splitlines():
    # print("Checkig package {}".format(pkg))
    md5_file = os.path.join(dpkg_info_base, pkg + ".md5sums")
    with open(md5_file) as f:
        md5sums = f.read()
    for line in md5sums.splitlines():
        md5_pkg, filename = line.split()
        filename = "/" + filename
        # print(" Checking hash of {}".format(filename))
        with open(filename, "rb") as f2:
            data = f2.read()
        md5_current = hashlib.md5(data).hexdigest()
        if md5_pkg != md5_current:
            msg = "HASH MISMATCH: {} {} {} {}".format(pkg,
                                                      filename,
                                                      md5_pkg,
                                                      md5_current)
            print(msg)
