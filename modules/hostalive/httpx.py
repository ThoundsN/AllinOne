import config
from log import logger
import utils

def runHttpx(urls_file) -> set:
    cmd = f"{config.httpx_command}  -l {str(urls_file)}   "
    logger.log('INFO',f'Running httpx with command {cmd}')
    httpx_result = utils.invokeCommand(cmd,return_stdout=True)
    logger.log('INFO',f'httpx finished')
    return utils.text2set(httpx_result)
