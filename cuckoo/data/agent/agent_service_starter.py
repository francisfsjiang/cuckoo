import subprocess

if __name__ == "__main__":

    cmd = [
        "C://Python27/python.exe",
        "C://Users/cuckoo/agent.py"
    ]
    DETACHED_PROCESS = 8
    subprocess.Popen(cmd, creationflags=DETACHED_PROCESS, close_fds=True)
