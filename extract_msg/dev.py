"""
Module for collecting data to be sent to the developer.
"""

# NOTE: Order of tasks:
#    1. Check for exceptions:
#        * Check the entire process for exceptions raised by a specific file and log them. If none occur,
#        log something like "No exceptions were detected."
#    2. Run the file through the developer versions of the classes


import logging
import os

from . import dev_classes
from . import utils
from .message import Message


logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())


def setupDevLogger(defaultPath=None, logfile = None, envKey='EXTRACT_MSG_LOG_CFG'):
    utils.setupLogging(defaultPath, 5, logfile, True, envKey)


def main(args, argv):
    """
    Please only run this from the command line. Attempting to use this
    otherwise is likely to fail. :param args: is the class instance
    returned by `extract_msg.utils.get_command_args`. :param argv: is
    the list of arguments that were the input to the aforementioned
    function.
    """
    setupDevLogger(args.config_path, args.log)
    currentdir = os.getcwd() # Store this just in case the paths that have been given are relative
    if args.out_path:
        if not os.path.exists(args.out_path):
            os.makedirs(args.out_path)
        out = args.out_path
    else:
        out = currentdir
    logger.log(5, f'ARGV: {argv}')
    for y, x in enumerate(args.msgs):
        logger.log(5, f'---- RUNNING DEVELOPER MODE ON FILE {x[0]} ----')
        logger.log(5, 'EXCEPTION CHECK:')
        try:
            with Message(x[0]) as msg:
                # Right here we should still be in the path in currentdir
                os.chdir(out)
                msg.save(toJson = args.json, useFileName = args.use_filename, ContentId = args.cid)
        except Exception as e:
            logger.exception(e)
        else:
            logger.log(5, 'No exceptions raised.')
        logger.log(5, 'DEVELOPER CLASS OUTPUT:')
        os.chdir(currentdir)
        dev_classes.Message(x[0])
        logger.log(5, '---- END OF DEVELOPER LOG ----')
        logpath = None;
        for x in logging.root.handlers:
            try:
                logpath = x.baseFilename
            except AttributeError:
                pass;
        print(g'Logging complete. Log has been saved to {logpath}')
