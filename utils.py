from ctypes import windll
from sys import exit
import platform
import os
from time import sleep

version = 1

def is_admin() -> bool:
    is_admin = windll.shell32.IsUserAnAdmin() != 0

    return is_admin

def CheckPatchElseContinue(file : str) -> None:
    hosts_read = open(file, "r")
    lines = hosts_read.readlines()
    hosts_read.close()

    ispatchapplied = False

    for i in lines:
        if "patch" in i:
            ispatchapplied = True

    versionnum = GetPatchVersion(file)

    if ispatchapplied and versionnum == version:
        print("Patch already applied!")
        print("Do you want to erase it?")
        print("1. Yes")
        print("2. No")
        choice = 0
        while (choice !=1 and choice != 2):
            choice = int(input())

        if (choice == 1):
            RemovePatch(file)
   
        exit(1)


def RemovePatch(file : str) -> None:
    hosts_read = open(file, "r")
    lines = hosts_read.readlines()
    hosts_read.close()
    begin = -1
    end = -1

    # find the beginning
    for i in range(len(lines)):
        line = lines[i]
        if "patch" in line:
            begin = i
            break

    # find the end
    for i in range(len(lines)):
        line = lines[i]
        if "endofpatch" in line:
            end = i
            break

    # begin and end are 0 indexed btw

    if begin != -1 and end != -1:
        for i in range(len(lines)):
            if (i >= begin and i <= end):
                lines[i] = ""

        hosts = open(file, "w")
        hosts.writelines(lines)
        hosts.close()

def is_windows() -> bool:
    return (platform.system() == "Windows")

def GetPatchVersion(file : str) -> int:
    hosts_read = open(file, "r")
    lines = hosts_read.readlines()
    hosts_read.close()
    v = -1

    # remove all new lines and carriage returns
    for i in range(len(lines)):
        lines[i] = lines[i].replace("\n", "").replace("\r", "")

    for i in lines:
        if "patch" in i:
            i = i.replace("#patch", "")
            v = int(i)
            
            print(f"Version: {v}")
            break

    return int(v)


def ApplyChanges() -> None:
    isWin = is_windows()

    if isWin:
        sleep(0.5)
        os.system("ipconfig /flushdns")
        sleep(0.5)
        os.system("nbtstat -R")
        sleep(0.5)
        os.system('start PowerShell.exe -WindowStyle Hidden -NoProfile -NoLogo -Command "try { $ServicePID = (get-wmiobject win32_service | where { $_.name -eq \'Dnscache\'}).processID; Stop-Process $ServicePID -Force } catch {}"')
    else:
        os.system("/etc/init.d/nscd restart")
        sleep(0.5)

def get_ai_list() -> list:
    AIs : list = [
                  #OpenAI
                  "chatgpt.com", 
                  "openai.com",
                  "chat.openai.com",
                  "sora.com",
                  
                  # uhhhh
                  "lindy.ai",
                  "perplexity.ai",
                  "jasper.ai",
                  "copy.ai",
                  
                  # coding & IDE
                  "claude.ai",
                  "cursor.com",
                  "api.individual.githubcopilot.com", # an api for copilot
                  "gemini.google.com",

                  #POS
                  "midjourney.com",

                  # random ones that i found 
                  "synthesia.io",
                  "play.ht", 
                  "descript.com",
                  "vapi.ai",
                  "app.obviously.ai",
                  "make.com",
                  "intercom.com",
                  "zapier.com",
                  "elevenlabs.com",
                  "copilot.microsoft.com"
                ]

    return AIs
