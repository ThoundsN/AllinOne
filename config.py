import pathlib
from dotenv import load_dotenv
import os

load_dotenv()


skip_wayback = False
skip_wayback_jsfiles = False
verbose_stdout = False
verbose_log = False

# 路径设置

root_data_dir = pathlib.Path(os.getenv('root_data_dir'))              #where to save your data
collaborator = os.getenv('collaborator')


allinone_dir = pathlib.Path(__file__).parent  # /allinone/




#command path
thirdparty_dir =  allinone_dir/'thirdparty'
binary_dir = thirdparty_dir/'binary'
python_dir = thirdparty_dir/'python'

oneforall_command = thirdparty_dir/"OneForAll"/"oneforall.py"
sqlite3_oneforall_path = thirdparty_dir/"OneForAll"/"results"/"result.sqlite3"
gau_command = binary_dir/"gau"
waybackmachine_downloader_command = "wayback_machine_downloader"
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
httprobe_command = binary_dir/"httprobe"


qsfuzz_command =binary_dir/"qsfuzz"
qsfuzz_sqli_template_path = thirdparty_dir/"QsfuzzTemplates"/"sqli.yaml"

gwen_xssjs_command =python_dir/"phantom-xss.js"             #must be under the same directory of gwen_xsspy

wordlist_path= allinone_dir/"other"/"wordlist.txt"

# nuclei_command = ""
# aquatone_command= binary_dir/"aquatone"
# chrome_command =""