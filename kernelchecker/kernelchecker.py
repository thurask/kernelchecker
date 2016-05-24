#!/usr/bin/env python3
import argparse
import collections
import datetime
import string
import sys
import requests
from bs4 import BeautifulSoup

__title__ = "kernelchecker"
__author__ = "Thurask"
__license__ = "WTFPL v2"
__copyright__ = "Copyright 2016 Thurask"
__version__ = "1.0.0"


class Kernel(object):
    def __init__(self, release, version, date, new=False):
        self.release = release
        self.version = version
        self.date = date
        self.new = new


def dateparse(datestring):
    stamp = datetime.datetime.strptime(datestring, "%Y-%m-%d")
    return stamp.strftime("%Y %m %d")


def make_key(key):
    return key if "next" in key else ".".join(key.split(".")[0:2])


def scrape_kernels():
    url = "https://www.kernel.org/"
    req = requests.get(url)
    soup = BeautifulSoup(req.text, "html.parser")
    table = soup.find("table", {"id": "releases"})
    kernels = collections.OrderedDict()
    for tr in table.findAll("tr"):
        tds = tr.findAll("td")
        release = tds[0].text.replace(":", "")
        date = dateparse(tds[2].text)
        kern = Kernel(release, tds[1].text, date)
        key = make_key(kern.version)
        kernels[key] = kern
    return kernels


def result_printer(release, version, date):
    print("{0}: {1} ({2})".format(release, version, date))


def main():
    print("~~~~KERNELCHECKER {0}~~~~\n".format(__version__))
    print("GETTING VERSIONS...\n")
    results = scrape_kernels()
    for key in results:
        kernel = results[key]
        result_printer(kernel.release, kernel.version, kernel.date)


def parse_args():
    parser = argparse.ArgumentParser(
        prog="kernelchecker",
        description="Linux kernel version scanner",
        epilog="https://github.com/thurask/kernelchecker")
    parser.add_argument(
        "-v",
        "--version",
        action="version",
        version="{0} {1}".format(parser.prog, __version__))
    parser.parse_known_args(sys.argv[1:])
    main()


if __name__ == "__main__":
    main()
