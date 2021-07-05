import config
import utils
from log import logger
from utils import invokeCommand
from modules.brute import ffuf2html
import csv
import os
from modules.brute import ffuf403

def runffuf(domain_url:str) :
    #https://github.com/ffuf/ffuf
    cmd=f"{config.ffuf_command}  -w {config.wordlist_path} -u {domain_url}/FUZZ -sa -r -H \"X-Real-IP: 127.0.0.1 \"-recursion -sf -ac -fs  0 -fw 1 -t 100 -s -o {config.ffuf_runtime_raw_dir}/{utils.dot2Underscore(domain_url)}.csv -of csv "
    logger.log('debug', f'Running ffuf with command {cmd}')
    invokeCommand(cmd)


def processFfufCsv(csvfile_input:str,csvfile_output:str):  #legacy code
    word_set = set()
    writer = csv.writer(open(csvfile_output, 'w'))

    with open(csvfile_input, 'r') as csvfile:
        csvreader = csv.reader(csvfile)
        writer.writerow(next(csvreader))
        for row in csvreader:
            if row[4] == '401':
                writer.writerow(row)
                continue
            if row[6] not in word_set:
                word_set.add(row[6])
                writer.writerow(row)


def ffufWrapper():
    with open(config.alive_noncdn_urls_file,'r') as f:
        for url in f:
            runffuf(url)

    csvfiles = utils.getFilesInDir(config.ffuf_runtime_raw_dir,".csv")
    for csvfile in csvfiles:
        newcsvfile =  config.ffuf_runtime_processed_dir + os.path.basename(csvfile)
        processFfufCsv(csvfile,newcsvfile)

    ffuf2html.main(config.ffuf_runtime_processed_dir,config.ffuf_result_file)


    ffuf403.fuzzPaths(csvfiles,config.ffuf_runtime_403_fuzzingpath_urls_result_csv,config.ffuf_runtime_403_fuzzingpath_result_csv)   
    processFfufCsv(config.ffuf_runtime_403_fuzzingpath_result_csv,config.ffuf_runtime_403_fuzzingpath_processed_csv)
    ffuf2html.csvfile2html(config.ffuf_runtime_403_fuzzingpath_processed_csv,config.ffuf_403_result_html)