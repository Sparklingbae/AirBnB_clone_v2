#!/usr/bin/python3
from fabric.api import local
from time import strftime
from datetime import date


def do_pack():
    """ A script that generates archive the contents of web_static folder"""

    filename = strftime("%Y%m%d%H%M%S")
    try:
        local("sudo mkdir -p versions")
        local("sudo tar -czvf versions/web_static_{}.tgz web_static/"
              .format(filename))
        if result.succeeded:
            return "versions/web_static_{}.tgz".format(filename)
        else:
            return None

    except Exception as e:
        return None
