import config
from log import logger
from utils import invokeCommand

def runWebScreenshot(urls_file,result_dir:str):
    cmd=f"{config.webscreenshot_command}  -i  {urls_file} -r phantomjs  -o {result_dir}  "
    logger.log('info', f'Screenshot urls webscreenshot with command {cmd}')
    invokeCommand(cmd)


def webscreenshotWrapper():
    runWebScreenshot(config.all_urls_file,config.result_screenshots_dir)