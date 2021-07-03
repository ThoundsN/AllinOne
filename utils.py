from invoke import run
from pathlib import Path
from datetime import datetime
import glob
import sqlite3
from log import logger
from modules.hostalive import httpx



#http://docs.pyinvoke.org/en/stable/api/runners.html#invoke.runners.Runner.run
def invokeCommand(command:str,*,stop_when_exception=True,return_stdout=False):
    '''

    :param command:
    :param stop_when_exception:
    :param return_stdout:
    :return:  str if return_stdout
    '''
    result = run(command,hide=True)
    if not result.ok and stop_when_exception:
        logger.log("FATAL",f"invokeCommand error: {result.stderr}")
        exit(1)
    if return_stdout:
        return result.stdout  #string




def getCurrentTime():
    current_time =  datetime.today().strftime('%m-%d-%H:%M')
    return current_time


# def getDatadir():
#     if not config.current_data_dir:
#         config.current_data_dir = config.root_data_dir/config.domain_name/getStartTime()
#         Path(config.current_data_dir).mkdir(parents=True, exist_ok=True)
#         return config.current_data_dir
#     return config.current_data_dir
#
# def getSubdir(subdir:str):
#     subdir_absolute = getDatadir()/subdir
#     Path(subdir_absolute).mkdir(parents=True, exist_ok=True)
#     return subdir_absolute

def makeDir(absolute_path):
    Path(absolute_path).mkdir(parents=True, exist_ok=True)
    return absolute_path


def getAllJsfiles(dir:str) -> list:
    '''
    returns absolute paths
    :param dir:
    :return:
    '''
    files = glob.glob(dir + '/**/*.js', recursive=True)
    return files

def getFilesInDir(dir:str,commonality:str) -> list:
    '''
    returns absolute paths
    :param dir:
    :return:
    '''
    files = glob.glob(dir + f'/**/*{commonality}', recursive=True)
    return files



def downloadLinksInFile(file_path:str):
    import config
    cmd = f"{config.aria2c_path} -i {file_path} "
    invokeCommand(cmd)


def location2href(location:str):
    import config
    #prefix = "http://jsrecon.ragnarokv.site/links/"
    prefix = config.collaborator+ '/links/'
    pieces = location.split('/')
    del pieces[6]
    del pieces[0:5]
    suffix = "/".join(pieces)
    href = prefix + suffix
    return  href

def dot2Underscore(domain:str):
    return domain.replace('.','_')


def querySqlite(domain:str,sqlite_path:str,query:str)-> set:
    query.replace(domain,dot2Underscore(domain))
    con =  sqlite3.connect(sqlite_path)
    cursor = con.cursor()
    cursor.execute(query)
    sql_results = set(cursor.fetchall())
    return sql_results


def testLiveUrls(urls_file)->set:
    live_urls = httpx.runHttpx(urls_file)
    return live_urls

def writeFile(lines,file:str):
    with open(file,'w') as f:
        if isinstance(lines, dict):
            for k,v in lines.items():
                f.write(f"{k}   :   {v}")
        for result_line in lines:
            f.write(result_line)

def readFile(file:str):
    with open(file,'w') as f:
        lines = f.readlines()
    return lines

def filterNegativeFile(result_file:str):
    with open(result_file,'r') as r:
        text = r.read()
        if 'VULNERABLE' in text or 'vulnerable' in text:
            is_vulneralbe = True

    if is_vulneralbe:
        p= Path(result_file)
        p.rename(Path(p.parent, f"vul_{p.stem}{p.suffix}"))


def checkOneDependency(command_path):
    test_commands = set()
    test_commands.add(f"{command_path} -h ")
    test_commands.add(f"{command_path} --help ")
    test_commands.add(f"{command_path} help ")
    command_ok = False
    for cmd in test_commands:
        result = run(cmd, hide=True)
        if result.stderr is  None:
            command_ok =  True
    if not command_ok:
        print(f"It's possible that {command_path} have some problems, better check it out manually ")