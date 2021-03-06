import sys
import os
import logging

top_dir = os.path.normpath(os.path.join(os.path.abspath(sys.argv[0]), os.pardir, os.pardir))
if os.path.exists(os.path.join(top_dir, 'techslate', '__init__.py')):
    sys.path.insert(0, top_dir)

from techslate.utils import logger # do not remove it, as it is the initializer for logger
from techslate import app

LOG = logging.getLogger(__name__)

if __name__ == '__main__':
    try:
        app.app.run('0.0.0.0', 5555, threaded=True)
    except Exception as e:
        sys.stderr.write("E R R O R: %s" % e)
        sys.exit(1)
