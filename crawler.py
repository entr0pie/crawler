#!/bin/python3

import requests
from bs4 import BeautifulSoup
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--target", type=str, required=True, help="Website to start the crawling")
parser.add_argument("--output", type=str, required=False, help="Output into file.")
args = parser.parse_args()

known = set()


to_crawl = [args.target]
lastlink = args.target

while len(to_crawl) > 0:
    response = requests.get(to_crawl[0])

    if response.status_code != 200:
        continue

    soup = BeautifulSoup(response.text, 'html.parser')

    links = soup.find_all('a')

    for ln in links:
        
        ln = ln.get('href')

        if str(type(ln)) == "<class 'NoneType'>":
            continue

        if ln == '':
            continue

        if ln[0:5] != 'https':
            ln = lastlink + ln
        
        if ln not in known:
            print(ln)
            
            if args.output:
                file = open(args.output, 'a')
                file.write(ln + '\n')
            
            known.add(ln)
            to_crawl.append(ln)
            to_crawl.pop(0)
