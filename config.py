import utils
import pathlib





# 路径设置
allinone_dir = pathlib.Path(__file__).parent  # /allinone/
collaborator = 'https://ssrf.ragnarokv.site/'
start_time = utils.getCurrentTime()
domain_name = ""


root_data_dir = pathlib.Path("/root/docker-nginx-php-mysql/web/public/data")              #where to save your data
current_data_dir =  utils.makeDir(root_data_dir/domain_name/start_time)
log_path = current_data_dir/f'AllInOne_{start_time}.log'  # AllInOne日志保存路径


wayback_subdir = current_data_dir/'wayback'

waybackurls_file = wayback_subdir / 'waybackurls.txt'
waybackjsurls_file = wayback_subdir / 'waybackJsurls.txt'
waybackurls_withquery_file = wayback_subdir / 'withqurey_waybackurls.txt'
waybackurls_withquery_live_file = wayback_subdir / 'live_withqurey_waybackurls.txt'


runtime_subdir = current_data_dir/'runtime'
runtime_jsfiles_dir = runtime_subdir /'jsfiles'
ffuf_runtime_raw_dir = runtime_subdir / 'ffuf_runtime/raw'
ffuf_runtime_processed_dir = runtime_subdir / 'ffuf_runtime/processed'
ffuf_runtime_process403_dir = runtime_subdir / 'ffuf_runtime/process_403'

ffuf_runtime_403_fuzzingpath_urls_result_csv = ffuf_runtime_process403_dir / 'fuzzingpath_urls.txt'
ffuf_runtime_403_fuzzingpath_result_csv = ffuf_runtime_process403_dir / 'fuzzingpath_result.csv'
ffuf_runtime_403_fuzzingpath_processed_csv = ffuf_runtime_process403_dir / 'fuzzingpath_processed.csv'
subdomains_file = runtime_subdir / 'subdomains.txt'
alive_urls_file = runtime_subdir / 'alive_urls.txt'
alive_noncdn_urls_file = runtime_subdir / 'alive_noncdn_urls.txt'
all_urls_file = runtime_subdir / 'all_urls.txt'
noncdn_ips_file = runtime_subdir / 'noncdn_ips.txt'
masscan_ip_port_file = runtime_subdir / 'masscan_ip_port.txt'
ssrf_urls_file = runtime_subdir / 'ssrfurls.txt'


result_subdir = current_data_dir/'results'
result_screenshots_dir = result_subdir /'screenshots'

jsfirebase_html = result_subdir / 'jsfirebase.html'
nmap_result_file = result_subdir / 'nmap_result.txt'
ffuf_result_file = result_subdir / 'ffuf.html'
ffuf_403_result_html = result_subdir / 'ffuf403.html'
xsspy_result_file = result_subdir / 'xsspy_result.txt'
kxss_result_file = result_subdir / 'kxss_result.txt'
lfipy_result_file = result_subdir / 'lfipy_result.txt'
crlfpy_result_file = result_subdir / 'crlfpy_result.txt'
qsfuzz_sqli_result_file = result_subdir / 'sqli_result.txt'
time_sqli_result_file = result_subdir / 'time_sqli_result.txt'



#command path
thirdparty_dir =  allinone_dir/'thirdparty'
binary_dir = thirdparty_dir/'binary'
python_dir = thirdparty_dir/'python'

oneforall_command = thirdparty_dir/"oneforall"/"oneforall.py"
sqlite3_oneforall_path = thirdparty_dir/"AllInOne"/"results"/"result.sqlite3"
gau_command = binary_dir/"gau"
waybackmachine_downloader_command = binary_dir/"wayback_machine_downloader"
urldedupe_command = binary_dir/"urldedupe"
aria2c_command = "aria2c"
dumpsterdriver_command = thirdparty_dir/"DumpsterDiver"/"DumpsterDiver.py"
httpx_command = binary_dir/"httpx"
masscan_command= binary_dir/"masscan"
nmap_command="nmap"
ffuf_command=binary_dir/"ffuf"
gwen_xsspy_command = python_dir/"gwen001_xss.py"
phantomjs_command = "phantomjs"
kxss_command = binary_dir/"kxss"
gwen_lfipy_command = python_dir/"gwen001_lfi.py"
gwen_crlfpy_command = python_dir/"gwen001_crlf.py "
webscreenshot_command = thirdparty_dir/"webscreenshot"/"webscreenshot.py"


qsfuzz_command =binary_dir/"qsfuzz"
qsfuzz_sqli_template_path = thirdparty_dir/"QsfuzzTemplates"/"sqli.yaml"

gwen_xssjs_command =python_dir/"phantom-xss.js"             #must be under the same directory of gwen_xsspy

wordlist_path= allinone_dir/"other"/"wordlist.txt"

# nuclei_command = ""
# aquatone_command= binary_dir/"aquatone"
# chrome_command =""