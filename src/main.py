import shutil
from utils import *

isAdmin : bool = is_admin()
isWindows : bool = is_windows()

try:
    winDir : str = os.environ["WINDIR"]
except:
    winDir : str = ""

hosts_file_path = winDir+"\\System32\\drivers\\etc\\hosts"

AI_urls : list = get_ai_list()
file_dir : str = os.path.dirname(__file__)

if not isWindows:
    print("Support on linux is experimental, be warned!")
    hosts_file_path = "/etc/hosts"

if not isAdmin:
    print("Not running as admin!")
    input()
    exit(1)

CheckPatchElseContinue(hosts_file_path)
RemovePatch(hosts_file_path)

print("Backing up file")
shutil.copy(hosts_file_path, file_dir)

# write to the hosts file
hosts = open(hosts_file_path, "a")
hosts.write(f"#patch{version}\n")

for i in AI_urls:
    hosts.write(f"127.0.0.1 {i}\n")

hosts.write("#endofpatch\n")
hosts.close()

ApplyChanges() # aka flush the dns
print("Finished! Restart your browsers to apply changes!")

