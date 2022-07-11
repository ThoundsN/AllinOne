#!/usr/bin/env python3

import pathlib
import fire
from modules.brute import ffuf
from modules.crlf import crlf
from modules.js import jsentropy,jsfirebase
from modules.lfi import lfi
from modules.onefall import onefall
from modules.portscan import masscan,nmap
from modules.sqli import sqli
from modules.ssrf import ssrf
from modules.waybackmachine import gau,waybackdownloader
from modules.xss import xss
from modules.other import screenshot
from modules.crawler import crawler
import utils
import config
from datetime import datetime
import log 




yellow = '\033[01;33m'
white = '\033[01;37m'
green = '\033[01;32m'
blue = '\033[01;34m'
red = '\033[1;31m'
end = '\033[0m'

class AllInOne(object):
    """
    AllInOne usage summary

    Examples:

        python3 AllInOne.py run example.com 

    """
    def __init__(self,domain=None):
        self.domain = domain




    @staticmethod
    def mkDataDir():
        varialbes = vars(config)
        for key in varialbes:
            if key.endswith("dir"):
                utils.makeDir(varialbes[key])


# todo adding  a option using previous unifinished  folder instead of creating a new one by checking files.
    @staticmethod
    def configDataDir(domain_name):
        config.domain_name = domain_name
        config.start_time = datetime.today().strftime('%m_%d_%H_%M')
        # config.start_time = '10_18_16_11'

        

        config.current_data_dir =  config.root_data_dir/config.domain_name/config.start_time
        config.log_path = config.current_data_dir/f'AllInOne.txt'  # AllInOne日志保存路径
        config.exception_path = "/root/docker-nginx-php-mysql/web/public/data/exceptions.txt"




        config.wayback_subdir = config.current_data_dir/'wayback'

        config.waybackurls_file = config.wayback_subdir / 'waybackurls.txt'
        config.waybackjsurls_file = config.wayback_subdir / 'waybackJsurls.txt'
        config.waybackurls_unique_file = config.wayback_subdir / 'waybackurls_unique.txt'
        config.waybackurls_withquery_file = config.wayback_subdir / 'withqurey_waybackurls.txt'
        config.waybackurls_withquery_live_file = config.wayback_subdir / 'live_withqurey_waybackurls.txt'

        config.runtime_subdir = config.current_data_dir/'runtime'
        config.runtime_jsfiles_dir = config.runtime_subdir /'jsfiles'
        config.ffuf_runtime_raw_dir = config.runtime_subdir / 'ffuf_runtime/raw'
        config.ffuf_runtime_processed_dir = config.runtime_subdir / 'ffuf_runtime/processed'
        config.ffuf_runtime_process403_dir = config.runtime_subdir / 'ffuf_runtime/process_403'

        config.ffuf_runtime_fuzzingpath_urls_file = config.ffuf_runtime_process403_dir / 'fuzzingpath_urls.txt'
        config.ffuf_runtime_fuzzingpath_raw_csv = config.ffuf_runtime_process403_dir / 'fuzzingpath_raw.csv'
        config.ffuf_runtime_fuzzingpath_processed_csv = config.ffuf_runtime_process403_dir / 'fuzzingpath_processed.csv'
        config.crawler_output = config.runtime_subdir / 'crawlerurls.txt'
        config.raw_merged_withqueryurl_file = config.runtime_subdir / 'raw_merged_withqueryurls.txt'
        config.merged_withqueryurl_file = config.runtime_subdir / 'merged_withqueryurls.txt'
        config.subdomains_file = config.runtime_subdir / 'subdomains.txt'
        config.alive_urls_file = config.runtime_subdir / 'alive_urls.txt'
        config.alive_noncdn_urls_file = config.runtime_subdir / 'alive_noncdn_urls.txt'
        config.all_urls_file = config.runtime_subdir / 'all_urls.txt'
        config.noncdn_ips_file = config.runtime_subdir / 'noncdn_ips.txt'
        config.masscan_ip_port_file = config.runtime_subdir / 'masscan_ip_port.txt'
        config.ssrf_urls_file = config.runtime_subdir / 'ssrfurls.txt'


        config.result_subdir = config.current_data_dir/'results'
        config.result_screenshots_dir = config.result_subdir /'screenshots'

        config.jsfirebase_html = config.result_subdir / 'jsfirebase.html'
        config.nmap_result_file = config.result_subdir / 'nmap_result.txt'
        config.ffuf_result_html = config.result_subdir / 'ffuf.html'
        config.ffuf_403_result_html = config.result_subdir / 'ffuf403.html'
        config.xsspy_result_file = config.result_subdir / 'xsspy_result.txt'
        config.kxss_result_file = config.result_subdir / 'kxss_result.txt'
        config.lfipy_result_file = config.result_subdir / 'lfipy_result.txt'
        config.crlfpy_result_file = config.result_subdir / 'crlfpy_result.txt'
        config.qsfuzz_sqli_result_file = config.result_subdir / 'sqli_result.txt'
        config.time_sqli_result_file = config.result_subdir / 'time_sqli_result.txt'

    def configLog(self):
        log.logger.add(config.log_path, level='DEBUG', format=log.logfile_fmt, enqueue=True, encoding='utf-8',backtrace=True, diagnose=True)
        log.logger.add(config.exception_path, level='ERROR', format=log.logfile_fmt, enqueue=True, encoding='utf-8',backtrace=True, diagnose=True)
        log.logger.log('INFO',f'Starting running allinone with {self.domain}')

    @log.logger.catch
    def run(self):
        config.domain_name = self.domain


        self.configDataDir(self.domain)
        self.mkDataDir()
        self.configLog()

        onefall.oneforallWrapper()

        # screenshot.webscreenshotWrapper()
        # masscan.masscanWrapper()
        # nmap.nmapWrapper()
        # ffuf.ffufWrapper()
        
        crawler.crawlerWrapper()

        gau.gauWrapper()

        if not config.skip_wayback:
            try:
                crawler_urls = utils.readFile(config.crawler_output)
                wayback_query_live_urls = utils.readFile(config.waybackurls_withquery_live_file)
                merged_urls = set(crawler_urls+wayback_query_live_urls)
                utils.writeFile(merged_urls,config.merged_withqueryurl_file)
                utils.dedupeUrlsWithqeury(config.raw_merged_withqueryurl_file,config.merged_withqueryurl_file)
            except:
                log.logger.exception("merge query urls file goes wrong ")
        else:
            crawler_urls = utils.readFile(config.crawler_output)
            utils.writeFile(crawler_urls,config.merged_withqueryurl_file)


        if not config.skip_wayback_jsfiles and not config.skip_wayback:
            jsentropy.dumpsterDriverWrapper()

            jsfirebase.jsfirebaseWrapper()



        if isUrlqueryFileUseful(config.merged_withqueryurl_file):
            xss.xssWrapper()

            lfi.lfiWrapper()


            crlf.crlfWrapper()

            ssrf.ssrfWrapper()

            sqli.sqliWrapper()


    @staticmethod
    def mass(file):
        with open(file) as f:
            lines =  filter(None, f.readlines())
        
        for line in lines:
            try:
                line = line.strip()
                a = AllInOne(domain=line)
                a.run()
            except Exception as e:
                continue

    @staticmethod
    def check():   #checkDependencies
        varialbes = vars(config)
        for key in varialbes:
            if key.endswith("command"):
                utils.checkOneDependency(varialbes[key])
        exit(0)


if __name__ == '__main__':
    fire.Fire(AllInOne)