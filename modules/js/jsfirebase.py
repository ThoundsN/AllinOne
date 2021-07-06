import config
import utils
from log import logger

from utils import invokeCommand, getAllJsfiles,downloadLinksInFile,makeDir,location2href


def checkFirebaseInJs(jsfile:str)-> str:
    with open(jsfile,'r') as f:
        if 'firebaseio' in f.read():
            return  location2href(jsfile)

def jsfirebaseWrapper():
    logger.log('INFO',f'Starting to check firebaseio urls in jsfiles')
    jsfiles = getAllJsfiles(config.runtime_jsfiles_dir)
    jshrefs = [checkFirebaseInJs(jsfile) for jsfile in jsfiles]
    utils.writeFile(jshrefs,config.jsfirebase_html)
    logger.log('INFO',f'firebaseio results saved to {config.jsfirebase_html}')
