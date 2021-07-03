import config
from log import logger
from utils import invokeCommand, writeFile
import utils

def runXsspy(urls_file:str,result_file:str) :
    cmd=f" {config.gwen_xsspy_command} -v 4 -u  {urls_file}  -O  {result_file}  -n {config.phantomjs_command} "
    logger.log('info', f'Running xsspy with command {cmd}')
    invokeCommand(cmd)


def runKxss(urls_file:str):
    cmd=f"cat {urls_file}  | {config.kxss_command} "
    logger.log('info', f'Running kxss with command {cmd}')
    result = invokeCommand(cmd,return_stdout=True)
    return set(result.split('\n'))

def xssWrapper():
    runXsspy(config.waybackurls_withquery_live_file,config.xsspy_result_file)
    kxss_results = runKxss(config.waybackurls_withquery_live_file)
    utils.filterNegativeFile(config.xsspy_result_file)


    writeFile(kxss_results,config.kxss_result_file)