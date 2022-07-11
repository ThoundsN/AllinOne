import config
import utils
from log import logger

from utils import invokeCommand, getAllJsfiles,downloadLinksInFile,makeDir,location2href


def checkFirebaseInJs(jsfile:str)-> str:
    with open(jsfile,'r') as f:
        if 'firebaseio' in f.read():
            return  location2href(jsfile)
            
            
@exception_handler
def jsfirebaseWrapper():
    logger.log('INFO',f'Starting to check firebaseio urls in jsfiles')
    jsfiles = getAllJsfiles(config.runtime_jsfiles_dir)
    jshrefs = [checkFirebaseInJs(jsfile) for jsfile in jsfiles]
    jshrefs = list(filter(None,jshrefs))
    if jshrefs:
        logger.log('INFO',f' {jshrefs}')

        utils.writeFile(jshrefs,config.jsfirebase_html)
        utils.notify(config.jsfirebase_html)
        logger.log('INFO',f'firebaseio results saved to {config.jsfirebase_html}')
    else:
        logger.log('INFO',f'Didn\'t  find any firebaseio urls ')

