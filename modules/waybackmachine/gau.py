import config
import utils
from log import logger
import re
import os
from utils import invokeCommand,downloadLinksInFile,makeDir
from modules.hostalive import httpx

def runGau(domain:str) -> set:
    cmd = f"{config.gau_command} -subs -b jpg,png,gif,woff,woff2,svg -o {domain} "
    logger.log('info',f'Running gau with command {cmd}')
    gau_result = invokeCommand(cmd,return_stdout=True)
    logger.log('info',f'gau finished')
    return set(gau_result.split('\n'))

def extractJsurls(waybackurls:set) -> set:
    jsurls = set()
    for url in waybackurls:
        if re.search("\.js(\?|$)",url):
            jsurls.add(url)
    return jsurls

def dedupeUrls(urls_file:str)->set:
    cmd = f"{config.urldedupe_command} -qs -u  {urls_file} "
    logger.log('info',f'Running urldedupe with command {cmd}')
    urldedupe_results = set(invokeCommand(cmd,return_stdout=True).split('\n'))
    return urldedupe_results

def gauWrapper(domain):
    waybackurls = runGau(domain)
    jsurls = extractJsurls(waybackurls)


    with open(config.waybackurls_file,'w' ) as f:
        for url in waybackurls:
            f.write(url)

    with open(config.waybackjsurls_file,'w' ) as f:
        for jsurl in jsurls:
            f.write(jsurl)

    urldedupe_results = dedupeUrls(config.waybackurls_file)

    with open(config.waybackurls_withquery_file,'w') as f:
        for url in urldedupe_results:
            f.write(url)

    live_withquery_urls = httx.runHttpx({config.waybackurls_withquery_file})
    with open(config.waybackurls_withquery_live_file,'w') as f:
        for url in live_withquery_urls:
            f.write(url)

    os.chdir(config.runtime_jsfiles_dir)
    logger.log('info',f'Downloading js files from  {config.waybackjsurls_file}')
    downloadLinksInFile(config.waybackjsurls_file)


