import config
from log import logger
import utils
from invoke import run 

# this httpx program only accepts cat | pipeline mode when invoked by python 
def runHttpx(urls_file,file_out) -> set:
    cmd = f"cat {urls_file}  |{config.httpx_command}  -threads 100  -silent >  {file_out}  "
    logger.log('INFO',f'Running httpx with command {cmd}')
    utils.invokeCommand(cmd,pty=True)
    logger.log('INFO',f'httpx finished')
    return 

# def runHttpx(urls_file,file_out) -> set:
#     cmd = f"cat {urls_file}  |{config.httpx_command}  -threads 100  -silent   "
#     logger.log('INFO',f'Running httpx with command {cmd},  result will be saved to {file_out}')
#     with open(file_out,'w') as f:
#         run(cmd,out_stream=f)
#     logger.log('INFO',f'httpx finished')
#     return 


# def runHttpx(urls_file,file_out) -> set:
#     cmd = f"cat {urls_file}  |{config.httprobe_command}  -c 100   "
#     logger.log('INFO',f'Running httprobe with command {cmd},  result will be saved to {file_out}')
#     with open(file_out,'w') as f:
#         run(cmd,out_stream=f)
#     logger.log('INFO',f'httprobe finished')
#     return 