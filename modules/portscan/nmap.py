import config
from log import logger
from utils import invokeCommand
from modules.portscan.masscan import parseMasscanOutputList
import asyncio


async def runNmap(ip:str,ports:set) -> str:
    cmd=f"{config.nmap_command} --script vulners.nse --script-args mincvss=5.0 -sV  -p{','.join(ports)} --version-intensity 9  {ip}  "
    logger.log('INFO', f'Running nmap with command {cmd}')
    proc  = await asyncio.create_subprocess_shell(cmd,stdout=asyncio.subprocess.PIPE,stderr=asyncio.subprocess.PIPE)
    stdout, stderr = await proc.communicate()
    # nmap_result = invokeCommand(cmd,return_stdout=True)
    return stdout.decode()

async def nmapTasks(ip_port:dict):
    '''
    # some machine have more than 10000+ ports opend
    '''
    try:
        tasks = [asyncio.create_task(runNmap(ip,ports_set)) for ip,ports_set in ip_port.items() if len(ip_port[ip]) < 50]
        nmap_results =  await asyncio.gather(*tasks)
        logger.log('INFO', f'Debug:  nmap_results: {nmap_results}')
    except:
        logger.exception("A exception happened")
    return nmap_results


def nmapWrapper():
    logger.log('INFO', f'starting running nmap for port scanning, input: {config.masscan_ip_port_file}..........')
    logger.log('INFO', f'Results will be saved to  {config.nmap_result_file}')

    ip_port = parseMasscanOutputList(config.masscan_ip_port_file)
    nmap_results = asyncio.run(nmapTasks(ip_port))
    with open(config.nmap_result_file, 'w') as f:
        for nmap_result in nmap_results:
            f.write(nmap_result)
            f.write('\n')
    logger.log('INFO', f'nmap finished')
