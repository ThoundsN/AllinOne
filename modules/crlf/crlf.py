import config
import utils
from log import logger
from utils import invokeCommand

def runcrlfpy(urls_file:str,result_file:str) :
    cmd=f" {config.gwen_crlfpy_command} -v 4 -u  {urls_file}  -O  {result_file}  -t 80"
    logger.log('INFO', f'Running crlfpy with command {cmd}')
    invokeCommand(cmd)



@exception_handler
def crlfWrapper():
    runcrlfpy(config.merged_withqueryurl_file,config.crlfpy_result_file)
    utils.filterNegativeFile(config.crlfpy_result_file)
