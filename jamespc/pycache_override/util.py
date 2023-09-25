import subprocess


def checkmem():
    print(subprocess.run("free", shell=True, text=True, stdout=subprocess.PIPE).stdout)


def checkproc():
    print(
        subprocess.run(
            "cat /proc/cpuinfo", shell=True, text=True, stdout=subprocess.PIPE
        ).stdout
    )


def checkdisk():
    print(subprocess.run("df", shell=True, text=True, stdout=subprocess.PIPE).stdout)
