#!/usr/local/bin/python3.6


from nyawc.Options import Options
from nyawc.QueueItem import QueueItem
from nyawc.Crawler import Crawler
from nyawc.CrawlerActions import CrawlerActions
from nyawc.http.Request import Request
import click
import re


boring_extension_regex = list((
"png\?",
"jpg\?",
"jpeg\?",
"gif\?",
"svg\?",
"bmp\?",
"ttf\?",
"avif\?",
"wav\?",
"mp4\?",
"aac\?",
"ajax\?",
"css\?",
"all\?",
"woff\?",
"js\?",
"woff2\?",
"map\?",
"pdf\?",
"xml\?",
"png$",
"jpg$",
"jpeg$",
"gif$",
"svg$",
"bmp$",
"ttf$",
"avif$",
"wav$",
"mp4$",
"aac$",
"ajax$",
"css$",
"all$",
"woff$",
"js$",
"woff2$",
"map$",
"pdf$",
"xml$"
))


class Driver:
    def __init__(self,options,outfile,url):
        self.__options = options
        self.__outfile = outfile
        self.__url = url

        self.__options.callbacks.crawler_before_start = self.cb_crawler_before_start
        self.__options.callbacks.crawler_after_finish = self.cb_crawler_after_finish
        self.__options.callbacks.request_before_start = self.cb_request_before_start
        self.__options.callbacks.request_after_finish = self.cb_request_after_finish





    def cb_crawler_before_start(self):
        print("Crawler started.")

    def cb_crawler_after_finish(self,queue):
        # Print the amount of request/response pairs that were found.
        print("Crawler finished, found " + str(queue.count_total) + " requests.")

        # Iterate over all request/response pairs that were found.
        for queue_item in queue.get_all("finished"):
            pass
            # print(queue_item)
            # print("Request method {}".format(queue_item.request.method))
            # print("Request URL {}".format(queue_item.request.url))
            # print("Request POST data {}".format(queue_item.request.data))

    def cb_request_before_start(self,queue, queue_item):
        url = queue_item.request.url
        for regex in boring_extension_regex:
            if re.search(regex,url):
                return CrawlerActions.DO_SKIP_TO_NEXT
        # print("Starting: {}".format(queue_item.request.url))

        return CrawlerActions.DO_CONTINUE_CRAWLING

    def cb_request_after_finish(self,queue, queue_item, new_queue_items):
        # print(queue_item.response.text)
        if queue_item.response.status_code not in  [401,403,404,405,502,501,406]:
            self.__outfile.write(queue_item.request.url)
            self.__outfile.write("\n")
        print("Found url: {}".format(queue_item.request.url))
        return CrawlerActions.DO_CONTINUE_CRAWLING

    def start(self):
        startpoint = Request(self.__url)
        crawler = Crawler(self.__options)
        # signal.signal(signal.SIGINT, self.__signal_handler)

        crawler.start_with(startpoint)


@click.command()
@click.option('-o', "--outfile",required=True, type=click.File('a'))
@click.option('-u', "--url",required=True, type=str)
def run(outfile, url):
    options = Options()
    
    options.performance.max_threads = 333
    options.performance.request_timeout = 15

    options.identity.headers.update({
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36"})
    options.scope.subdomain_must_match = False




    if "http"  not in url:
        url = "http://" + url

    driver = Driver(options,outfile,url)

    driver.start()

if __name__ == '__main__':
    run()

