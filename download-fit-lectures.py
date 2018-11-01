#!/usr/bin/python3
from argparse import RawTextHelpFormatter
from time import gmtime, strftime
from bs4 import BeautifulSoup
from platform import system
import requests
import argparse
import urllib3
import sys
import os
import re
 
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
 
class MyParser(argparse.ArgumentParser):
    def error(self, message):
        self.print_help()
        sys.exit(1)
 
parser = argparse.ArgumentParser(usage='Příklad použití:\n%(prog)s -l xlogin00 -heslo heslo12345 -a https://video1.fit.vutbr.cz/av/records-categ.php?id=1234 [-c C:\\adresář\\přednášky] [-v] [-u] [-p INT]')
parser = MyParser(formatter_class=RawTextHelpFormatter)
group = parser.add_mutually_exclusive_group()
group.add_argument("-u", "--uspat", help="Uspí pc po dostahování přednášek\nWindows vyžaduje spustit cmd jako správce a poté zadat \"powercfg -h off\"", action="store_true", dest="uspat")
group.add_argument("-v", "--vypnout", help="Vypne pc po dostahování přednášek", action="store_true", dest="vypnout")
parser.add_argument("-p", "--pocet", help="Počet přednášek, které se stáhnou", type=int, dest="pocet")
parser.add_argument("-c", "--cesta", help="Zadej cestu, kde chces uložit přednášky", type=str, dest="cesta")
parser.add_argument("-l", "--login", help="Zadej svůj login pro přihlášení", type=str, required=True, dest="login")
parser.add_argument("-H", "--heslo", help="Zadej svoje heslo pro přihlášení", type=str, required=True, dest="heslo")
parser.add_argument("-a", "--adresa", help="URL adresa daného předmětu z video-serveru", type=str, required=True, dest="adresa")
args = parser.parse_args()
 
if args.cesta:
    if not os.path.exists(args.cesta):
        os.makedirs(args.cesta)
    output_dir = os.path.abspath(args.cesta)
else:
    output_dir = os.path.abspath("")
 
session = requests.session()
 
def login(username, password):
    session.get("https://cas.fit.vutbr.cz/", verify=False)
    session.post("https://cas.fit.vutbr.cz/cosign.cgi", verify=False,
        data={
            "login": username,
            "password": password,
            "useKX509": "0",
            "doLogin": "Log In"
        })
 
def get_recording_urls(recordings_url):
    response = session.get(recordings_url, verify=False)
    soup = BeautifulSoup(response.text, features="html.parser")
    entries = soup.find_all("li", style="vertical-align: middle; list-style-image: url(/img/odrazka-film.gif)")
    url_base = response.url.rsplit("/", 1)[0]
    urls = []
    for entry in entries:
        recording_url = url_base + "/" + entry.find("a").get("href")
        urls.append(recording_url)
    return urls
 
def download_file(url, filename):
    response = session.get(url, verify=False, stream=True)
    # filename = response.headers["Content-Disposition"].split('filename="', 1)[1].split('"', 1)[0]
    total_size = None
    if "Content-Length" in response.headers:
        total_size = int(response.headers["Content-Length"])
    bytes_written = 0
    with open(filename, "wb") as file:
        for chunk in response.iter_content(4096):
            file.write(chunk)
            bytes_written += len(chunk)
            if total_size is not None:
                print(f"\r{bytes_written/1024/1024:.2f} MiB / {total_size/1024/1024:.2f} MiB - {bytes_written/total_size*100:.2f}%", end="")
            else:
                print(f"\r{bytes_written/1024/1024:.2f} MiB", end="")
 
def get_valid_name(name):
    return re.sub(r'[\/:*?"<>|]', "", name)
 
def download_recording(recording_url, output_dir):
    response = session.get(recording_url, verify=False)
    soup = BeautifulSoup(response.text, features="html.parser")
    download_link = soup.find("a", title="Stažení záznamu").get("href")
    title_el = soup.find("h3", class_="nadpis")
    title = title_el.text
    sub_title = title_el.next_sibling.strip()
    recording_name = get_valid_name(title + " " + sub_title) + ".mp4"
    filename = os.path.join(output_dir, recording_name)
    if os.path.exists(filename):
        print(f"Soubor {filename} uz existuje, preskakuju...")
    else:
        print(f"Stahuju {title} {sub_title} do {filename}")
        download_file(download_link, filename)
 
login(args.login, args.heslo)
recording_urls = get_recording_urls(args.adresa)
for recording in recording_urls:
    try:
        download_recording(recording, output_dir)
        if args.pocet is not None:
            args.pocet -= 1
            if args.pocet <= 0:
                print("Stazen pozadovany pocet prednasek")
                break
    except Exception as e:
        print("Stazeni prednasky selhalo, nejspis byl vycerpan denni limit")
        print(repr(e))
 
 
if system() == "Windows":
    if args.uspat:
        os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0 ")
    elif args.vypnout:
        os.system("shutdown -s")
elif system() == "Linux":
    if args.uspat:
        os.system("systemctl hibernate")
    elif args.vypnout:
        os.system("systemctl suspend")
else:
    print("Prosím kontaktuj tvůrce skriptu")