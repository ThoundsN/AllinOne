import config
import utils
from log import logger
import re
import os
from utils import invokeCommand,downloadLinksInFile,makeDir,text2set,isEmpty
from modules.hostalive import httpx

def runGau(domain:str) -> set:
    cmd = f"{config.gau_command} -subs -b jpg,png,gif,woff,woff2,svg  {domain} "
    logger.log('INFO',f'Running gau with command {cmd}')
    gau_result = invokeCommand(cmd,return_stdout=True)
    logger.log('INFO',f'gau finished')
    return text2set(gau_result)

def extractJsurls(waybackurls:set) -> set:
    jsurls = set()
    for url in waybackurls:
        if re.search("\.js(\?|$)",url):
            jsurls.add(url)
    return jsurls

def dedupeUrls(urls_file:str)->set:
    cmd = f"{config.urldedupe_command} -qs -u  {urls_file} "
    logger.log('INFO',f'Running urldedupe with command {cmd}')
    urldedupe_results = invokeCommand(cmd,return_stdout=True)
    return text2set(urldedupe_results)

def gauWrapper():
    waybackurls = runGau(config.domain_name)
    if len(waybackurls) == 0:
        logger.log('INFO',f"Didn't find any waybackurls, skip operation related to wayback machine   ")
        config.skip_wayback = True
        return        
    logger.log('INFO',f'Found {len(waybackurls)}  waybackurls  ')
    utils.writeFile(waybackurls,config.waybackurls_file)


    urldedupe_results = dedupeUrls(config.waybackurls_file)
    if len(urldedupe_results) == 0:
        logger.log('INFO',f"Didn't find any unique waybackurls with querystring , skip operation related to wayback machine   ")
        config.skip_wayback = True
        return       
    logger.log('INFO',f'Found {len(urldedupe_results)}  unique waybackurls with query strings after dedupe')
    utils.writeFile(urldedupe_results,config.waybackurls_withquery_file)


    live_withquery_urls = httpx.runHttpx(config.waybackurls_withquery_file)
    if len(live_withquery_urls) == 0:
        logger.log('INFO',f"Didn't find any live unique waybackurls with querystring , skip operation related to wayback machine   ")
        config.skip_wayback = True
        return      
    logger.log('INFO',f'Found {len(live_withquery_urls)}  alive unique waybackurls with querystring using httpx ')
    utils.writeFile(live_withquery_urls,config.waybackurls_withquery_live_file)
    
    jsurls = extractJsurls(waybackurls)
    if len(jsurls) == 0:
        logger.log('INFO',f"Didn't find any  jsurl from internet archive, skip operation related to wayback machine   ")
        config.skip_wayback_jsfiles = True
        return  
    logger.log('INFO',f'Found {len(jsurls)}  js urls  ')
    utils.writeFile(jsurls,config.waybackjsurls_file)
    os.chdir(config.runtime_jsfiles_dir)
    logger.log('INFO',f'Downloading js files from  {config.waybackjsurls_file}')
    downloadLinksInFile(config.waybackjsurls_file)


