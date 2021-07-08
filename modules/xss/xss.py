import config
from log import logger
from utils import invokeCommand, writeFile
import utils

#wasted 2 hours  one can invoke phantomjs with "-platform offscreen" options.
#https://bugs.debian.org/cgi-bin/bugreport.cgi?bug=817277
def runXsspy(urls_file:str,result_file:str) :
    # cmd=f" {config.gwen_xsspy_command} -v 4 -u  {urls_file}  -O  {result_file}  -n {config.phantomjs_command} "
    cmd=f" {config.gwen_xsspy_command} -v 4 -u  {urls_file}  -O  {result_file}   "
    logger.log('INFO', f'Running xsspy with command {cmd}')
    invokeCommand(cmd)


def runKxss(urls_file:str,file_out):
    cmd=f"cat {urls_file}  | {config.kxss_command} "
    logger.log('INFO', f'Running kxss with command {cmd}')
    invokeCommand(cmd)
    return



def xssWrapper():
    runXsspy(config.waybackurls_withquery_live_file,config.xsspy_result_file)
    logger.log('INFO', f'xsspy results saved to  {config.xsspy_result_file}')
    
    kxss_results = runKxss(config.waybackurls_withquery_live_file,config.kxss_result_file)
    logger.log('INFO', f'xsspy results saved to  {config.kxss_result_file}')


    # writeFile(kxss_results,config.kxss_result_file)
    utils.filterNegativeFile(config.xsspy_result_file)
