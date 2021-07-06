import config
import utils
from log import logger
from utils import invokeCommand, dot2Underscore,querySqlite
import itertools


def runoneforall(domain:str):
    cmd = f"{config.oneforall_command}  --target {domain} run   "
    logger.log('INFO',f'Running oneforall with command {cmd}')
    invokeCommand(cmd)
    logger.log('INFO',f'oneforall finished')


def getUrlAliveandNoncdn(domain:str,sqlite_path:str) -> set:
    query = f"select url from {domain} where alive = 1 and cdn = 0 "
    return querySqlite(domain,sqlite_path,query)

def getUrlAlive(domain:str,sqlite_path:str) -> set:
    query = f"select url from {domain} where alive = 1"
    return querySqlite(domain,sqlite_path,query)

def getAllUrls(domain:str,sqlite_path:str) -> set:
    query = f"select url from {domain} "
    return querySqlite(domain,sqlite_path,query)

#https://stackoverflow.com/questions/10632839/transform-list-of-tuples-into-a-flat-list-or-a-matrix/35228431
# sql_reqsults  {('10.48.32.37,10.48.26.81',), ('10.22.8.0,10.22.28.78,10.22.42.7',), ('10.24.11.116,10.24.28.101,10.24.40.125',), ('10.52.43.49,10.52.12.148,10.52.22.245',), ('10.16.8.59,10.16.16.50,10.16.47.179',), ('10.19.34.16,10.19.3.232,10.19.19.162',), ('10.33.4.190,10.33.25.75',), ('10.33.15.217,10.33.31.3',), ('10.24.27.19,10.24.34.112,10.24.3.251',), ('10.33.25.75,10.33.4.190',), ('10.20.37.220,10.20.11.29,10.20.25.103',), ('10.52.22.245,10.52.43.49,10.52.12.148',), ('10.19.34.16,10.19.19.162,10.19.3.232',), ('10.24.28.26,10.24.47.42,10.24.5.216',), ('10.33.31.3,10.33.15.217',), ('10.48.46.150,10.48.18.207',), ('10.19.19.162,10.19.3.232,10.19.34.16',), ('10.52.34.161,10.52.23.29',), ('10.19.30.193,10.19.37.44',), ('10.52.25.228,10.52.47.103',), ('10.48.37.47,10.48.10.34,10.48.24.162',), ('10.48.10.34,10.48.24.162,10.48.37.47',), ('10.22.25.217,10.22.7.207',), ('10.34.42.184,10.34.1.112',), ('10.19.17.151,10.19.39.160',), ('10.20.1.46,10.20.29.202',), ('10.20.25.103,10.20.11.29,10.20.37.220',), ('3.130.4.114,3.131.113.129',), ('10.20.1.168,10.20.21.233',)}
def getIPNoncdn(domain:str,sqlite_path:str)-> set:
    query = f"select ip from {domain} where cdn = 0"
    sql_reqsults = querySqlite(domain,sqlite_path,query)
    # logger.log("INFO",f"{sql_reqsults}")

    s = set()
    for element in sql_reqsults:
        for string in element:
            s.update(string.split(","))
    return s

def oneforallWrapper():
    domain = config.domain_name
    runoneforall(domain)
    # logger.log("INFO",f"{config.alive_urls_file}")

    utils.writeFile(getUrlAlive(domain,config.sqlite3_oneforall_path),config.alive_urls_file)
    utils.writeFile(getIPNoncdn(domain,config.sqlite3_oneforall_path),config.noncdn_ips_file)
    utils.writeFile(getUrlAliveandNoncdn(domain,config.sqlite3_oneforall_path),config.alive_noncdn_urls_file)
    utils.writeFile(getAllUrls(domain,config.sqlite3_oneforall_path),config.all_urls_file)
