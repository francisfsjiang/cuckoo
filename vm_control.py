from __future__ import print_function
import subprocess
import sys
import os
import time

VBOXMANAGE_BIN = "VBoxManage"


def info_print(msg, ret, out):
    if not ret:
        print("%s %s" % (msg, ret))
    else:
        print("%s %s. %s" % (msg, ret, out))


def execute(*popenargs, **kwargs):
    process = subprocess.Popen(stdout=subprocess.PIPE, stderr=subprocess.PIPE, *popenargs, **kwargs)
    output, unused_err = process.communicate()
    retcode = process.poll()
    return retcode, output


def create_if():
    ret, out = execute([
            VBOXMANAGE_BIN,
            "hostonlyif",
            "create",
    ])
    info_print("Create Hostonlyif. ", ret, out)

    ret, out = execute([
            VBOXMANAGE_BIN,
            "hostonlyif"
            "ipconfig"
            "vboxnet0"
            "--ip",
            "192.168.56.1"
            "--netmask 255.255.255.0"
    ])
    info_print("Config Hostonlyif. ", ret, out)

    ret, out = execute([
        VBOXMANAGE_BIN,
        "dhcpserver",
        "modify",
        "--ifname",
        "vboxnet0",
        "--disable",
    ])
    info_print("Closing DHCP server. ", ret, out)


def check_if():
    ret, out = execute([
        VBOXMANAGE_BIN,
        "list",
        "hostonlyifs",
    ])
    if out == "":
        create_if()


def clone_vm(from_vm_name, new_vm_name):
    print("Cloning vm from %s to %s" % (from_vm_name, new_vm_name))

    ret, out = execute([
        VBOXMANAGE_BIN,
        "clonevm",
        from_vm_name,
        "--snapshot",
        "ReadytoRun",
        "--options",
        "link",
        "--name",
        new_vm_name,
        "--register",
    ])
    info_print("Clone VM. ", ret, out)


def config_vm(vm_name, ip_address):
    print("Configuring vm %s, %s" % (vm_name, ip_address))

    ret, out = execute([
        VBOXMANAGE_BIN,
        "startvm",
        vm_name,
        "--type",
        "headless",
    ])
    info_print("Start VM. ", ret, out)

    ret = 1
    while ret:
        time.sleep(5)
        cmd = [
            VBOXMANAGE_BIN,
            'guestcontrol',
            vm_name,
            '--username',
            'Cuckoo',
            'run',
            '--exe',
            '"c:\\Python27\\python.exe"',
            '--',
            '"/c"',
            '"c:\\Users\\cuckoo\\sudo.py"',
            '"netsh"',
            '"interface"',
            '"ipv4"',
            '"set"',
            '"address"',
            '"\\\"\\\"Local"',
            '"Area"',
            '"Connection\\\"\\\""',
            '"static"',
            '"%s"' % ip_address,
            '"255.255.255.0"',
            '"192.168.56.1"',
        ]
        cmd = " ".join(cmd)
        ret, out = execute(cmd, shell=True)

    info_print("Config VM's IP addr. ", ret, out)

    cmd = [
        VBOXMANAGE_BIN,
        'guestcontrol',
        vm_name,
        '--username',
        'Cuckoo',
        'run',
        '--exe',
        '"c:\\Python27\\python.exe"',
        '--',
        '"/c"',
        '"c:\\Users\\cuckoo\\sudo.py"',
        '"cmd"',
        '"/c"',
        '"start"',
        '"c:\\Python27\\python.exe"',
        '"c:\\Users\\cuckoo\\agent_service_starter.py"',
    ]
    cmd = " ".join(cmd)
    ret, out = execute(cmd, shell=True)
    info_print("Start VM's agent. ", ret, out)

    ret, out = execute([
        VBOXMANAGE_BIN,
        'snapshot',
        vm_name,
        'take',
        "ReadytoRun",
    ])
    info_print("Take VM's snapshot. ", ret, out)

    ret, out = execute([
        VBOXMANAGE_BIN,
        'controlvm',
        vm_name,
        "poweroff",
    ])
    info_print("Shotdown VM. ", ret, out)


def create_vm_from_vdi(vm_name, vdi_path):
    print("Creating vm %s, from vid: %s" % (vm_name, vdi_path))
    check_if()
    ret, out = execute([
        VBOXMANAGE_BIN,
        "createvm",
        "--name",
        vm_name,
        "--ostype",
        "Windows7_64",
        "--register"
    ])
    info_print("Create VM. ", ret, out)

    ret, out = execute([
        VBOXMANAGE_BIN,
        "modifyvm",
        vm_name,
        "--memory",
        "1024",
    ])
    info_print("Modify VM's memory. ", ret, out)

    ret, out = execute([
        VBOXMANAGE_BIN,
        "modifyvm",
        vm_name,
        "--vram",
        "21",
    ])
    info_print("Modify VM's video memory. ", ret, out)

    ret, out = execute([
        VBOXMANAGE_BIN,
        "storagectl",
        vm_name,
        "--name",
        "SATA",
        "--add",
        "sata",
        "--portcount",
        "1",
        "--bootable",
        "on"
    ])
    info_print("Modify VM's storage. ", ret, out)

    cmd = [
        VBOXMANAGE_BIN,
        "storageattach",
        vm_name,
        "--storagectl",
        "SATA",
        "--port",
        "0",
        "--device",
        "0",
        "--type",
        "hdd",
        "--medium",
        vdi_path,
        "--setuuid",
        '""',
    ]
    cmd = " ".join(cmd)
    ret, out = execute(cmd, shell=True)
    info_print("Attach VM's storage. ", ret, out)

    ret, out = execute([
        VBOXMANAGE_BIN,
        "modifyvm",
        vm_name,
        "--nic1",
        "hostonly",
        "--hostonlyadapter1",
        "vboxnet0",
    ])
    info_print("Modify VM's net adapter. ", ret, out)


def main():
    print("Vdi path: %s" % sys.argv[1])
    print("Creating %d vms" % int(sys.argv[2]))

    create_vm_from_vdi(
        "Cuckoo0",
        sys.argv[1]
    )
    config_vm("Cuckoo0", "192.168.56.110")

    for i in range(1, int(sys.argv[2])):
        print("-----")
        clone_vm("Cuckoo0", "Cuckoo%d" % i)
        config_vm("Cuckoo%d" % i, "192.168.56.%d" % (110 + i))


if __name__ == "__main__":
    main()