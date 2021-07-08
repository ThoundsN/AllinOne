import config
import utils
from log import logger
import re
import os
from utils import invokeCommand,downloadLinksInFile,makeDir,text2set,isEmpty,lineCount
from modules.hostalive import httpx

def runGau(domain:str,file_out) -> set:
    cmd = f"{config.gau_command} -subs -b jpg,png,gif,woff,woff2,svg  {domain}  >  {file_out} "
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

def dedupeUrlsWithqeury(urls_file:str,file_out)->set:
    cmd = f"{config.urldedupe_command} -qs -s -u {urls_file}  >  {file_out}  "
    logger.log('INFO',f'Running urldedupe with command {cmd}')
    invokeCommand(cmd)
    return 

def dedupeUrls(urls_file:str,file_out)->set:
    cmd = f"{config.urldedupe_command} -s -u {urls_file}  >  {file_out}  "
    logger.log('INFO',f'Running urldedupe with command {cmd}')
    invokeCommand(cmd)
    return 

def gauWrapper():
    # runGau(config.domain_name,config.waybackurls_file)
    # if isEmpty(config.waybackurls_file):
    #     logger.log('INFO',f"Didn't find any waybackurls, skip operation related to wayback machine   ")
    #     config.skip_wayback = True
    #     return        
    # logger.log('INFO',f'Found {lineCount(config.waybackurls_file)} raw  waybackurls ')
    

    # logger.log('INFO',f'Starting to dedupe waybackurls , only leaves unique urls and  with query urls')
    # dedupeUrlsWithqeury(config.waybackurls_file,config.waybackurls_withquery_file)
    dedupeUrls(config.waybackurls_file,config.waybackurls_unique_file)
    # if isEmpty(config.waybackurls_withquery_file):
    #     logger.log('INFO',f"Didn't find any unique waybackurls with querystring , skip operation related to wayback machine   ")
    #     config.skip_wayback = True
    #     return       
    # logger.log('INFO',f'Found {lineCount(config.waybackurls_withquery_file)}  unique waybackurls with query strings after dedupe')

    # logger.log('INFO',f'Starting to check live waybackurls ')
    # httpx.runHttpx(config.waybackurls_withquery_file,config.waybackurls_withquery_live_file)
    # if isEmpty(config.waybackurls_withquery_live_file):
    #     logger.log('INFO',f"Didn't find any live unique waybackurls with querystring , skip operation related to wayback machine   ")
    #     config.skip_wayback = True
    #     return      
    # logger.log('INFO',f'Found {lineCount(config.waybackurls_withquery_live_file)}  unique waybackurls with query strings after dedupe')
    # logger.log('INFO',f'Live withquery waybackurls saved to   {config.waybackurls_withquery_live_file} ')
    
    waybackurls_unique = utils.readFile(config.waybackurls_unique_file)
    jsurls = extractJsurls(waybackurls_unique)
    if len(jsurls) == 0:
        logger.log('INFO',f"Didn't find any  jsurl from internet archive, skip operation related to wayback machine   ")
        config.skip_wayback_jsfiles = True
        return  
    logger.log('INFO',f'Found {len(jsurls)}  js urls  ')

    utils.writeFile(jsurls,config.waybackjsurls_file)
    os.chdir(config.runtime_jsfiles_dir)
    logger.log('INFO',f'Downloading js files from  {config.waybackjsurls_file},  results will be saved to {config.runtime_jsfiles_dir}')
    downloadLinksInFile(config.waybackjsurls_file)


