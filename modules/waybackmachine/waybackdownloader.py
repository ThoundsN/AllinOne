import config
import utils
from log import logger
import os
from utils import invokeCommand,getAllJsfiles,makeDir
import shutil



def runWaybackDownloader(domain_url:str):
    '''
    download old js files
    :param domain:  https://example.com
    :return:
    '''
    cmd = f'{config.waybackmachine_downloader_command} {domain_url} --only "/\.js/i"    '
    logger.log('INFO',f'Running waybackmachine downloader  with command {cmd}')
    invokeCommand(cmd)
    logger.log('INFO',f'waybackmachine downloader finished')


def waybackDownloaderWrapper():
    '''
    :param domain_urls:
    :return:
    '''
    domain_urls = utils.readFile(config.all_urls_file)
    os.chdir(config.wayback_subdir)

    logger.log('INFO',"Starting running waybackmachine downloader...........")
    for domain_url in domain_urls:
        runWaybackDownloader(domain_url)

    jsfiles = getAllJsfiles(config.wayback_subdir)
    logger.log('DEBUG',"Starting processing jsfiles ...........")

    for jsfile in jsfiles:    #maybe you need to process jsfilename
        shutil.move(jsfile,config.runtime_jsfiles_dir)          #https://stackoverflow.com/questions/41826868/moving-all-files-from-one-directory-to-another-using-python

    os.chdir(config.runtime_jsfiles_dir)
    cmd = f'fdupes . -r -f -1 -S -d -N  > /dev/null"    '
    logger.log('INFO',f'Remove duplicate js files from waybackmachine with command {cmd}')
    invokeCommand(cmd)

