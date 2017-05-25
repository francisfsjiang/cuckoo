#! encoding=utf-8

"""
Disable UAC before using this script.
"""


import sys
import os
import tempfile


CSRIPT_TEMPLATE = \
"""
Set objShell = CreateObject("Shell.Application")\n\r
args = Right("{args}", (Len("{args}") - Len("{command}")))\n\r
objShell.ShellExecute "{command}", args, "", "runas"\n\r
"""

if __name__ == "__main__":

    cmd = sys.argv[1:]
    cmd_joined = " ".join(cmd)

    csript_content = CSRIPT_TEMPLATE.format(args=cmd_joined, command=cmd[0])

    temp_file_fd, temp_file_path = tempfile.mkstemp(suffix=".vbs", prefix="sudo_")
    temp_file = os.fdopen(temp_file_fd, "w")
    temp_file.write(csript_content)
    temp_file.close()

    ret = os.system("cscript " + temp_file_path)
    print "Execute status: %d" % ret

    os.remove(temp_file_path)
