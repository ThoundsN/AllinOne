import config
from log import logger
from utils import invokeCommand
import utils

def runLfipy(urls_file:str,result_file:str) :
    cmd=f" {config.gwen_lfipy_command} -v 4 -u  {urls_file}  -O  {result_file}  "
    logger.log('INFO', f'Running lfipy with command {cmd}')
    invokeCommand(cmd)



@exception_handler
def lfiWrapper():
    runLfipy(config.merged_withqueryurl_file,config.lfipy_result_file)
    utils.filterNegativeFile(config.lfipy_result_file)
