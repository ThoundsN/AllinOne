#!/usr/bin/env python3

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
import utils
import config


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

        python3 AllInOne.py --domain example.com run

    """
    def __init__(self,domain=None):
        self.domain = domain
        # self.domains = domains
        # self.skipdns = skipdns
        config.domain_name = domain


    def configParam(self):
        pass


    @staticmethod
    def mkDataDir():
        varialbes = vars(config)
        for key in varialbes:
            if key.endswith("dir"):
                utils.makeDir(varialbes[key])

    def configThirdPartyPath(self):
        pass

    def run(self,domain):
        self.mkDataDir()
        onefall.oneforallWrapper(domain)
        gau.gauWrapper(domain)
        waybackdownloader.waybackDownloaderWrapper()
        jsentropy.dumpsterDriverWrapper()
        jsfirebase.jsfirebaseWrapper()
        screenshot.webscreenshotWrapper()
        masscan.masscanWrapper()
        nmap.nmapWrapper()
        ffuf.ffufWrapper()
        xss.xssWrapper()
        sqli.sqliWrapper()
        crlf.crlfWrapper()
        lfi.lfiWrapper()
        ssrf.ssrfWrapper()

    @staticmethod
    def check(self):   #checkDependencies
        varialbes = vars(config)
        for key in varialbes:
            if key.endswith("command"):
                utils.checkOneDependency(varialbes[key])
        exit(0)


if __name__ == '__main__':
    fire.Fire(AllInOne)