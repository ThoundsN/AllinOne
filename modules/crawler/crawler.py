import config
import utils
from log import logger
from utils import invokeCommand, readFile,writeFile
import random

def runcrawler(url:str,outfile:str) :
    cmd=f" {config.crawler_command} -u {url}  -o {outfile}"
    logger.log('INFO', f'Running crawler  with command {cmd}')
    invokeCommand(cmd)

def crawlHistoryurls():
    try:
        wayback_query_live_urls = utils.readFile(config.waybackurls_withquery_live_file)
    except:
        return
    if len(wayback_query_live_urls) < 15 :
        return
    elif len(wayback_query_live_urls) < 15 :
        lucky_urls = wayback_query_live_urls
    elif len(wayback_query_live_urls) < 100:
        num = len(wayback_query_live_urls) // 4
        lucky_urls = random.sample(wayback_query_live_urls,num)
    else:
        num = len(wayback_query_live_urls) // 10
        lucky_urls = random.sample(wayback_query_live_urls,num)

    for url in lucky_urls:
        runcrawler(url,config.crawler_output)

def crawlerWrapper():
    urls = readFile(config.alive_urls_file)
    logger.log('INFO',f'Starting crawler urls ')
    for url in urls:
        runcrawler(url,config.crawler_output)

    crawlHistoryurls()

    result_urls = readFile(config.crawler_output)
    result_urls = set(result_urls)
    writeFile(result_urls, config.crawler_output)
    
