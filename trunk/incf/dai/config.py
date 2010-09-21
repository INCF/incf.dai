"""Hardcoded meta data as long as we don't get it from the central hub"""

HUBS = {'aba'  :'http://incf-dev.crbs.ucsd.edu:8080/atlas-aba?service=WPS',
        'emap' :'http://incf-dev.crbs.ucsd.edu:8080/atlas-emap?service=WPS',
        'ucsd' :'http://incf-dev.crbs.ucsd.edu:8080/atlas-ucsd?service=WPS',
        'whs'  :'http://incf-dev.crbs.ucsd.edu:8080/atlas-whs?service=WPS',
        }


# set up logging to file - straight from the Python docs

import logging

LOG_FILENAME = "./incf.dai.log"
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(name)-8s %(levelname)-8s %(message)s',
                    datefmt='%Y-%m-%d %H:%M',
                    filename=LOG_FILENAME,
                    filemode='a')
# define a Handler which writes INFO messages or higher to the sys.stderr
CONSOLE = logging.StreamHandler()
CONSOLE.setLevel(logging.INFO)
# set a format which is simpler for console use
FORMATTER = logging.Formatter('%(name)-8s: %(levelname)-8s %(message)s')
# tell the handler to use this format
CONSOLE.setFormatter(FORMATTER)
# add the handler to the root logger
logging.getLogger('').addHandler(CONSOLE)

LOGGER = logging.getLogger('incf.dai')
