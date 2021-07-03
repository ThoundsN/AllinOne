import config
from log import logger
from utils import invokeCommand
from masscan import parseMasscanOutputList
import asyncio


async def runNmap(ip:str,ports:set) -> str:
    cmd=f"{config.nmap_command} --script vulners.nse --script-args mincvss=5.0 -sV  -p{','.join(ports)} --version-intensity 9  {ip}  "
    logger.log('debug', f'Running nmap with command {cmd}')
    nmap_result = invokeCommand(cmd,return_stdout=True)
    return nmap_result

async def nmapTasks(ip_port:dict):
    tasks = [asyncio.create_task(runNmap(ip,ports_set)) for ip,ports_set in ip_port.items()]
    nmap_results =  await asyncio.gather(*tasks,return_exceptions=True)
    return nmap_results


def nmapWrapper():
    logger.log('info', f'starting running nmap for port scanning, input: {config.masscan_ip_port_file}..........')
    ip_port = parseMasscanOutputList(config.masscan_ip_port_file)
    nmap_results = asyncio.run(nmapTasks(ip_port))
    with open(config.nmap_result_file, 'w') as f:
        for nmap_result in nmap_results:
            f.write(nmap_result)
            f.write('\n')
    logger.log('info', f'nmap finished, results {config.nmap_result_file}..........')
