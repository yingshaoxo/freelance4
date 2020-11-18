#!/usr/bin/env /usr/bin/python3
from auto_everything.terminal import Terminal
from auto_everything.disk import Disk
from auto_everything.base import IO
from auto_everything.base import Python
import json
t = Terminal()
disk = Disk()
io = IO()
py = Python()


def seperate():
    print()
    print("-------")
    print()


DEVICE = "/dev/ttyUSB0"
PRE_COMMAND = f"ampy -p {DEVICE} "
LS = PRE_COMMAND + "ls"
DELETE = PRE_COMMAND + "rm "
PUT = PRE_COMMAND + "put "

micropython_files = [name.strip("/") for name in t.run_command(LS).split("\n") if name.strip() != "" and name[-3:] == ".py"]
print(micropython_files)

computer_files = disk.get_files(".", recursive=False, type_limiter=[".py"])
computer_files = [name[2:] for name in computer_files if ".swp" not in name]
print(computer_files)

seperate()

hash_json = ".hash.json"
hashs = {}
if not disk.exists(hash_json):
    for file in computer_files:
        hashs.update({
            file: disk.get_hash_of_a_file(file)
        })
        t.run_command(PUT + file)
        print(f"updated: {file}")
    io.write(hash_json, json.dumps(hashs))
    print("no json found, created a new one.")
else:
    hashs = json.loads(io.read(hash_json))

for file in computer_files:
    if file not in micropython_files:
        t.run_command(PUT + file)
        print(f"updated: {file}")
    else:
        if hashs[file] != disk.get_hash_of_a_file(file):
            t.run_command(PUT + file)
            print(f"updated: {file}")
        else:
            pass

for file in micropython_files:
    if file not in computer_files:
        t.run_command(DELETE + file)
        print(f"deleted: {file}")

for file in computer_files:
    hashs.update({
        file: disk.get_hash_of_a_file(file)
    })
io.write(hash_json, json.dumps(hashs))

seperate()

print(t.run_command(LS))
py.make_it_runnable()
"""
for FILE in *; do ampy -p /dev/ttyUSB0 put $FILE; done
ampy -p /dev/ttyUSB0 ls
"""
