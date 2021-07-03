import config
from log import logger
from utils import invokeCommand

def runHttpx(urls_file) -> set:
    cmd = f"{config.httpx_command}  -l {urls_file}   "
    logger.log('info',f'Running httpx with command {cmd}')
    httpx_result = invokeCommand(cmd,return_stdout=True)
    logger.log('info',f'httpx finished')
    return set(httpx_result.split('\n'))



