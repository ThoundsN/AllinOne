import config
import utils
from log import logger
from modules.sqli import timeSqli


def runqsfuzzSqli(urls_file:str,template_file:str,file_out):
    cmd = f" cat {urls_file} |    {config.qsfuzz_command}  -c {template_file} -w 60  > {file_out}"
    logger.log('INFO',f'Running qsfuzz with command {cmd}')
    qsfuzz_result = utils.invokeCommand(cmd,return_stdout=True)
    logger.log('INFO',f'qsfuzz finished')
    return set(qsfuzz_result.split('\n'))


def runtimeSqli():
    urls = utils.readFile(config.waybackurls_withquery_live_file)
    logger.log('INFO',f'Starting to test blind time based sqli')
    timeSqli_results = timeSqli.main(urls)
    if timeSqli_results:
        logger.log('INFO',f'Found potential vulnerble sqli url , saved to {config.time_sqli_result_file}')
        utils.writeFile(timeSqli_results,config.time_sqli_result_file)


def sqliWrapper():
    # runqsfuzzSqli(config.waybackurls_withquery_live_file,config.qsfuzz_sqli_template_path,config.qsfuzz_sqli_result_file)
    runtimeSqli()


