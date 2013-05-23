# -*- encoding: utf-8 -*-

import sys

from .common import exit_codes
from .api import setup_app

def main():
    _, _, _, svc = setup_app(
        usage = "%prog [options]",
        description = """Print the pilot server version.""",
        argstest = lambda args: len(args) == 0,
        logname = "pilot-server-version")

    print svc.server_version()
    sys.exit(exit_codes.success)

if __name__ == '__main__':
    main()
