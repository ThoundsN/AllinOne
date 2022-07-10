from invoke import run
from pathlib import Path
import glob
import sqlite3
from log import logger
import re
import config 
import json 



#http://docs.pyinvoke.org/en/stable/api/runners.html#invoke.runners.Runner.run
#http://docs.pyinvoke.org/en/stable/api/runners.html#invoke.runners.Result
def invokeCommand(command:str,*,stop_when_exception=False,return_stdout=False,pty=False):
    '''

    :param command:
    :param stop_when_exception:
    :param return_stdout:
    :return:  str if return_stdout
    '''

    if not stop_when_exception:
        result = run(command,hide='both',pty=pty)
    else:
        try:
            result = run(command,warn=True,hide='both',pty=pty)
            if not result.ok:
                logger.log("FATAL",f"invokeCommand error: {result.stderr}")
        except Exception as e:
            logger.log('FATAL', f' exception raised: {e}  ')
            pass
    if return_stdout:
        return result.stdout  #string 


def text2set(text:str)->set:
    str_list = text.split("\n")
    str_set = set(filter(None, str_list))
    return str_set


def isEmpty(file_path:Path)->bool:
    is_empty = False
    if type(file_path) == str:
        file_path =  Path(file_path)
    if not file_path.exists():
        is_empty = True 
    if file_path.stat().st_size == 0:
        is_empty = True 
        
    if file_path.stat().st_size < 1024:
        with open(file_path,'r') as f:
            if any(line in ['\n', '\r\n'] for line in f):
                is_empty = True 
    if is_empty:
        logger.log('INFO', f' File: {file_path} is empty')
        return True
    return False


# def getCurrentTime():
#     current_time =  datetime.today().strftime('%m-%d-%H:%M')
#     return current_time


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


def getAllJsfiles(dir) -> list:
    '''
    returns absolute paths
    :param dir:
    :return:
    '''
    files = glob.glob(str(dir) + '/**/*.js', recursive=True)
    return files

def getFilesInDir(dir,commonality:str) -> list:
    '''
    returns absolute paths
    :param dir:
    :return:
    '''
    files = glob.glob(str(dir) + f'/**/*{commonality}', recursive=True)
    return files



def downloadLinksInFile(file_path:str):
    import config
    cmd = f"{config.aria2c_command} -i {file_path} -j 15"
    invokeCommand(cmd)


def location2href(filelocation:str):
    import config
    prefix = config.dataurl
    pieces = filelocation.split('/')
    del pieces[6]
    del pieces[0:5]
    suffix = "/".join(pieces)
    href = prefix + suffix
    return  href

def replaceUnderscore(domain:str):
    domain = domain.replace('/','_')
    domain = domain.replace('：','_')
    domain = domain.replace('-','_')
    return domain.replace('.','_')


def querySqlite(domain:str,sqlite_path:str,query:str)-> set:
    # logger.log("INFO",f"domain: {domain}")
    # logger.log("INFO",replaceUnderscore(domain))
    # logger.log("INFO",f"{domain in query}")
    
    query = query.replace(domain,replaceUnderscore(domain))
    logger.log("INFO",f"Querying oneforall sqlitedb {sqlite_path} with query:  {query}")
    con =  sqlite3.connect(sqlite_path)
    cursor = con.cursor()
    cursor.execute(query)
    sql_results = set(cursor.fetchall())
    return sql_results



def writeFile(lines,file):
    logger.log("INFO",f"write results to {file}")
    # logger.log("INFO",f"{type(lines)} {lines}")
    try:    
        with file.open('w') as f:
            if isinstance(lines, dict):
                f.write(json.dumps(lines))
            elif any(isinstance(i, tuple) for i in lines):
                for result_line in lines:
                    result_line = "".join(result_line)
                    f.write(result_line+'\n')
            else:
                for result_line in lines:
                # logger.log("INFO",f" {type(result_line)}{result_line}")
                    f.write(result_line+'\n')
    except:
        logger.exception("A exception happened")

#stupid bug:     with open(file,'w') as f:
def readFile(file:str):
    with open(file,'r') as f:
        lines = f.readlines()
    return lines
    
        

def filterNegativeFile(result_file:str):
    is_vulneralbe=False
    with open(result_file,'r') as r:
        text = r.read()
        if 'VULNERABLE' in text or 'vulnerable' in text:
            is_vulneralbe = True

    if is_vulneralbe:
        p= Path(result_file)
        newfilename = f"vul_{p.stem}{p.suffix}"
        p.rename(Path(p.parent, newfilename))
        notify(newfilename)


def checkOneDependency(command_path):   # exit code 126,127 of invoke.run is bad 
    test_commands = set()
    test_commands.add(f"{command_path} -h ")
    test_commands.add(f"{command_path} --help ")
    command_ok = False
    command_possilbe_ok = False
    for cmd in test_commands:
        # print(cmd)
        try:
            result = run(cmd, hide=True,warn=True,timeout=3)
        except:
            print(f"{command_path} seems to be a shell pipeline program , can't determine whether it is executable ")
            return 
        # print(result)
        if result.ok:
            command_ok =  True
            break
        if result.return_code != 126 and result.return_code != 127:
            command_possilbe_ok = True
    if command_ok:
        return
    if  command_possilbe_ok:
        print(f"{command_path} --help/-h  returns nonzero code  , better check it out manually ")
    else:
        print(f"Very likely that {command_path} have some problems, better check it out manually ")


def lineCount(fname):
    with open(fname) as f:
        for i, l in enumerate(f):
            pass
    return i + 1


def dedupeUrlsWithqeury(urls_file:str,file_out):
    cmd = f"{config.urldedupe_command} -qs -s -u {urls_file}  >  {file_out}  "
    logger.log('INFO',f'Running urldedupe with command {cmd}')
    invokeCommand(cmd)
    return 

def dedupeUrls(urls_file:str,file_out):
    cmd = f"{config.urldedupe_command} -s -u {urls_file}  >  {file_out}  "
    logger.log('INFO',f'Running urldedupe with command {cmd}')
    invokeCommand(cmd)
    return 



def notify(file_path):
    file_url = location2href(file_path)
    with open("/root/data/notify.txt","a") as f:
        f.write(file_url)
        f.write("\n")