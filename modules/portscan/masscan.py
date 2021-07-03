import config
from log import logger
from utils import invokeCommand

def runMasscan(ipfile_input:str,file_output:str):
    cmd=f"{config.masscan_command}  -p1-65535 -iL {ipfile_input}  --source-port 61000 --rate 10000 -oL {file_output}"
    logger.log('debug', f'Running masscan with command {cmd}')
    invokeCommand(cmd)


def parseMasscanOutputList(masscan_out:str) -> dict:
    '''
#masscan
open tcp 443 8.8.8.8 1624852640
open tcp 53 8.8.8.8 1624852643
open tcp 853 8.8.8.8 1624852646
# end
    :param masscan_out:
    :return: ip_port  {str:set} dict
    '''
    ip_port = {}

    with open(masscan_out,'r') as f:
        next(f)
        for line in f:
            if line.startswith('#'):
                continue
            a = line.split(' ')
            ip = a[4]
            port = a[3]
            if ip in ip_port:
                ip_port[ip].add(port)
            else:
                ip_port[ip] = set()
                ip_port[ip].add(port)
    return ip_port


def masscanWrapper():
    logger.log('info',f"starting running masscan with input {config.noncdn_ips_file} ")
    runMasscan(config.noncdn_ips_file,config.masscan_ip_port_file)
    logger.log('info',f"masscan finished, result will be saved to  {config.masscan_ip_port_file} ")
