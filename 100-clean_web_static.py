#!/usr/bin/python3
# Fabfile to delete out-of-date archives.
import os
from fabric.api import *

<<<<<<< HEAD
env.hosts = ["54.144.156.108", "54.84.62.16"]
=======
env.hosts = ["18.235.233.45", "100.25.160.122"]
>>>>>>> 457b054fff60216218c98c013416902f25227d91


def do_clean(number=0):
    """Delete out-of-date archives.

    Args:
        number (int): The number of archives to keep.

    If number is 0 or 1, keeps only the most recent archive. If
    number is 2, keeps the most and second-most recent archives,
    etc.
    """
    number = 1 if int(number) == 0 else int(number)

    archives = sorted(os.listdir("versions"))
    [archives.pop() for i in range(number)]
    with lcd("versions"):
        [local("rm ./{}".format(a)) for a in archives]

    with cd("/data/web_static/releases"):
        archives = run("ls -tr").split()
        archives = [a for a in archives if "web_static_" in a]
        [archives.pop() for i in range(number)]
        [run("rm -rf ./{}".format(a)) for a in archives]