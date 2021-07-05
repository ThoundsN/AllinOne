import config
import utils
from log import logger
from modules.sqli import timeSqli


def runqsfuzzSqli(urls_file:str,template_file:str):
    cmd = f" cat {urls_file} |    {config.qsfuzz_command}  -c {template_file} -w 80 "
    logger.log('info',f'Running qsfuzz with command {cmd}')
    qsfuzz_result = utils.invokeCommand(cmd,return_stdout=True)
    logger.log('info',f'qsfuzz finished')
    return set(qsfuzz_result.split('\n'))


def sqliWrapper():
    results = runqsfuzzSqli(config.waybackurls_withquery_live_file,config.qsfuzz_sqli_template_path)
    utils.writeFile(results,config.qsfuzz_sqli_result_file)
    urls = utils.readFile(config.waybackurls_withquery_live_file)

    logger.log('info',f'Starting to test blind time based sqli')
    timeSqli_results = timeSqli.main(urls)
    if timeSqli_results:
        utils.writeFile(timeSqli_results,config.time_sqli_result_file)
