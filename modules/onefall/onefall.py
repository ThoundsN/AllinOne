import config
import utils
from log import logger
from utils import invokeCommand, dot2Underscore,querySqlite
import itertools


def runoneforall(domain:str):
    cmd = f"{config.oneforall_command}  --target {domain} run   "
    logger.log('info',f'Running oneforall with command {cmd}')
    invokeCommand(cmd)
    logger.log('info',f'oneforall finished')


def getUrlAliveandNoncdn(domain:str,sqlite_path:str) -> set:
    query = f"select url from {domain} where alive = 1 and cdn = 0 "
    return querySqlite(domain,sqlite_path,query)

def getUrlAlive(domain:str,sqlite_path:str) -> set:
    query = f"select url from {domain} where alive = 1"
    return querySqlite(domain,sqlite_path,query)

def getAllUrls(domain:str,sqlite_path:str) -> set:
    query = f"select url from {domain} "
    return querySqlite(domain,sqlite_path,query)

def getIPNoncdn(domain:str,sqlite_path:str)-> set:
    query = f"select ip from {domain} where cdn = 0"
    sql_reqsults = querySqlite(domain,sqlite_path,query)
    sql_reqsults = set((itertools.chain.from_iterable(sql_reqsults)))
    return sql_reqsults

def oneforallWrapper(domain):
    runoneforall(domain)
    utils.writeFile(getUrlAlive(domain,config.sqlite3_oneforall_path),config.alive_urls_file)
    utils.writeFile(getIPNoncdn(domain,config.sqlite3_oneforall_path),config.noncdn_ips_file)
    utils.writeFile(getUrlAliveandNoncdn(domain,config.sqlite3_oneforall_path),config.alive_noncdn_urls_file)
    utils.writeFile(getUrlAliveandNoncdn(domain,config.sqlite3_oneforall_path),config.all_urls_file)
