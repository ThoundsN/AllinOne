import config
from log import logger
import re
import os
from utils import invokeCommand,downloadLinksInFile,location2href
import json


def runDumpsterDriver(output_file:str):
    cmd = f"python3 {config.dumpsterdriver_command}  -p . -o  {output_file} > /dev/null"
    logger.log('INFO',f'Running dumpsterdriver with command {cmd}')
    invokeCommand(cmd)


def processDumpsterResult(json_file:str,processed_file:str):
    entropys = set()
    newdata = []

    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
        for entry in data:
            entry_entropy_value = entry['Details']['Entropy']
            # logger.log('INFO',f'{entry_entropy_value}')

            if entry_entropy_value not in entropys:
                newdata.append(entry)
                entropys.add(entry_entropy_value)

    for entry in newdata:
        file_location = entry['File']
        href = location2href(file_location)
        entry['href'] = href

    processed_json = json.dumps(newdata)
    with open(processed_file,'w') as f:
        f.write(processed_json)

def dumpsterDriverWrapper():

    os.chdir(config.runtime_jsfiles_dir)
    logger.log('INFO',f'Changing working dir to {config.runtime_jsfiles_dir}')
    cmd = f'fdupes . -r -f -1 -S -d -N  > /dev/null   '
    logger.log('INFO',f'Remove duplicate js files from waybackmachine with command {cmd}')
    invokeCommand(cmd)

    runDumpsterDriver(config.runtime_subdir/'entropy.json')

    processDumpsterResult(config.runtime_subdir/'entropy.json',config.result_subdir/'entropy.json')