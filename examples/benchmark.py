"""
pyubx2 Performance benchmarking utility

Usage (kwargs optional): python3 benchmark.py cycles=10000

Created on 5 Nov 2021

:author: semuadmin
:copyright: SEMU Consulting © 2021
:license: BSD 3-Clause
"""
# pylint: disable=line-too-long

from sys import argv
from datetime import datetime
from platform import version as osver, python_version
from pyubx2.ubxreader import UBXReader
from pyubx2._version import __version__ as ubxver

UBXMESSAGES = [
    b"\xb5b\x10\x02\x18\x00\x72\xd8\x07\x00\x18\x18\x00\x00\x4b\xfd\xff\x10\x40\x02\x00\x11\x23\x28\x00\x12\x72\xd8\x07\x00\x03\x9c",
    b"\xb5b\x10\x02\x1c\x00\x6d\xd8\x07\x00\x18\x20\x00\x00\xcd\x06\x00\x0e\xe4\xfe\xff\x0d\x03\xfa\xff\x05\x09\x0b\x00\x0c\x6d\xd8\x07\x00\xee\x51",
    b"\xb5b\x10\x02\x18\x00\xd5\xd8\x07\x00\x18\x18\x00\x00\x4d\xfd\xff\x10\x45\x02\x00\x11\x1f\x28\x00\x12\xd5\xd8\x07\x00\xcc\xac",
    b"\xb5b\x10\x02\x1c\x00\xd0\xd8\x07\x00\x18\x20\x00\x00\x7c\x06\x00\x0e\xcb\xfe\xff\x0d\xac\xf9\xff\x05\x09\x0b\x00\x0c\xd0\xd8\x07\x00\xf2\xae",
    b"\xb5b\x10\x02\x18\x00\x38\xd9\x07\x00\x18\x18\x00\x00\x4a\xfd\xff\x10\x41\x02\x00\x11\x27\x28\x00\x12\x38\xd9\x07\x00\x95\x7a",
    b"\xb5b\x10\x02\x1c\x00\x33\xd9\x07\x00\x18\x20\x00\x00\x0f\x06\x00\x0e\x16\xfe\xff\x0d\x5b\xfa\xff\x05\x0a\x0b\x00\x0c\x33\xd9\x07\x00\x49\x9f",
    b"\xb5b\x10\x02\x18\x00\x9c\xd9\x07\x00\x18\x18\x00\x00\x4e\xfd\xff\x10\x4e\x02\x00\x11\x20\x28\x00\x12\x9c\xd9\x07\x00\x67\x0e",
    b"\xb5b\x10\x02\x1c\x00\x97\xd9\x07\x00\x18\x20\x00\x00\x85\x06\x00\x0e\x77\xfe\xff\x0d\xe1\xf9\xff\x05\x0a\x0b\x00\x0c\x97\xd9\x07\x00\x6d\xa4",
    b"\xb5b\x10\x02\x18\x00\xff\xd9\x07\x00\x18\x18\x00\x00\x4c\xfd\xff\x10\x3e\x02\x00\x11\x24\x28\x00\x12\xff\xd9\x07\x00\x1f\x22",
    b"\xb5b\x10\x02\x1c\x00\xfa\xd9\x07\x00\x18\x20\x00\x00\x92\x06\x00\x0e\x61\xfe\xff\x0d\x9f\xf9\xff\x05\x0a\x0b\x00\x0c\xfa\xd9\x07\x00\xe8\x90",
    b"\xb5b\x10\x02\x18\x00\x63\xda\x07\x00\x18\x18\x00\x00\x47\xfd\xff\x10\x44\x02\x00\x11\x1c\x28\x00\x12\x63\xda\x07\x00\xe2\xe4",
    b"\xb5b\x10\x02\x1c\x00\x5e\xda\x07\x00\x18\x20\x00\x00\xef\x06\x00\x0e\xb8\xfe\xff\x0d\xc8\xf9\xff\x05\x0a\x0b\x00\x0c\x5e\xda\x07\x00\x8f\xce",
    b"\xb5b\x10\x02\x18\x00\xc6\xda\x07\x00\x18\x18\x00\x00\x4a\xfd\xff\x10\x4e\x02\x00\x11\x21\x28\x00\x12\xc6\xda\x07\x00\xba\x88",
    b"\xb5b\x10\x02\x1c\x00\xc1\xda\x07\x00\x18\x20\x00\x00\x82\x06\x00\x0e\x5b\xfe\xff\x0d\xc8\xf9\xff\x05\x09\x0b\x00\x0c\xc1\xda\x07\x00\x8a\xd2",
    b"\xb5b\x10\x02\x18\x00\x2a\xdb\x07\x00\x18\x18\x00\x00\x48\xfd\xff\x10\x47\x02\x00\x11\x27\x28\x00\x12\x2a\xdb\x07\x00\x81\x4e",
    b"\xb5b\x10\x02\x1c\x00\x25\xdb\x07\x00\x18\x20\x00\x00\x1b\x07\x00\x0e\xed\xfe\xff\x0d\xfa\xf9\xff\x05\x09\x0b\x00\x0c\x25\xdb\x07\x00\xb2\xef",
    b"\xb5b\x10\x02\x1c\x00\xdb\x25\x01\x00\x18\x20\x00\x00\x76\x02\x00\x0e\x06\xf8\xff\x0d\xde\xf7\xff\x05\x54\x0a\x00\x0c\xdb\x25\x01\x00\x3b\x91",
    b"\xb5b\x10\x02\x18\x00\xee\x23\x01\x00\x18\x18\x00\x00\xe8\x11\x00\x10\xfa\x07\x00\x11\xa1\x22\x00\x12\xee\x23\x01\x00\x6e\xf9",
    b"\xb5b\x10\x02\x1c\x00\x94\x21\x01\x00\x18\x20\x00\x00\xff\x05\x00\x0e\xf3\xfe\xff\x0d\x4d\x0b\x00\x05\x51\x0a\x00\x0c\x94\x21\x01\x00\xa5\x52",
    b"\xb5b\x05\x01\x02\x00\x06\x01\x0f\x38",
    b"\xb5b\x06\x01\x08\x00\xf0\x01\x00\x01\x01\x01\x00\x00\x036",
    b"\xb5b\x06\x00\x00\x00\x06\x18",
    b"\xb5b\x01\x12$\x000D\n\x18\xfd\xff\xff\xff\xf1\xff\xff\xff\xfc\xff\xff\xff\x10\x00\x00\x00\x0f\x00\x00\x00\x83\xf5\x01\x00A\x00\x00\x00\xf0\xdfz\x00\xd0\xa6",
    b"\xb5b\x06\x17\x04\x00\x00\x00\x00\x00\x21\xe9",
    b"\xb5b\x06\x17\x0c\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x29\x61",
    b"\xb5b\x13\x80\x0e\x00\x01\x02\x03\x04\x05\x06\x07\x08\x09\x0a\x0b\x0c\x01\x02\xf2\xc2",
    b"\xb5b\x13\x21\x06\x00\x03\x01\x02\x00\x00\x04\x44\x3a",
    b"\xb5b\x06\x8b\x0c\x00\x00\x00\x00\x00\x01\x00\x52\x40\x80\x25\x00\x00\xd5\xd0",
    b"\xb5b\x06\x8b\x09\x00\x00\x00\x00\x00\x01\x00\x51\x20\x55\x61\xc2",
    b"\xb5b\x06\x8b\x16\x00\x00\x00\x00\x00\x01\x00\x51\x20\x55\x01\x00\x52\x40\x80\x25\x00\x00\x02\x00\x21\x30\x23\x1c\x92",
    b"\xb5b\x06\x8b\x0c\x00\x00\x00\x00\x00\x68\x00\x11\x40\xb6\xf3\x9d\x3f\xdb\x3d",
    b"\xb5b\x10\x02\x1c\x00\x6d\xd8\x07\x00\x18\x20\x00\x00\xcd\x06\x00\x0e\xe4\xfe\xff\x0d\x03\xfa\xff\x05\x09\x0b\x00\x0c\x6d\xd8\x07\x00\xee\x51",
    b"\xb5b\x10\x02\x18\x00\x72\xd8\x07\x00\x18\x18\x00\x00\x4b\xfd\xff\x10\x40\x02\x00\x11\x23\x28\x00\x12\x72\xd8\x07\x00\x03\x9c",
    b"\xb5b\n1\x14\x01\x00\x01\x00\x00-+-,+-.,-.+,+.-..-,..//./00203017?9398:L]<@C;H<>=A@BDCGJNQRVY[_cgpqyz\x7f\x84\x8c\x90\x99\xa0\xa7\xae\xb0\xae\xaa\xa7\xa2\x9b\x97\x96\x94\x91\x90\x8e\x8c\x8c\x8c\x8b\x8b\x89\x88\x89\x89\x89\x8b\x88\x89\x8a\x89\x8a\x8a\x89\x8a\x8b\x8a\x8a\x8b\x8b\x8c\x8a\x8a\x8a\x8b\x88\x88\x87\x87\x86\x85\x85\x85\x84\x89\x84\x85\x83\x84\x84\x84\x85\x88\x87\x87\x88\x8a\x8a\x8a\x8a\x8b\x8e\x8c\x8d\x8d\x8f\x8e\x8d\x8f\x8e\x8f\x8f\x8e\x8f\x8f\x90\x91\x92\x93\x93\x93\x95\x94\x94\x94\x94\x95\x94\x95\x93\x93\x91\x92\x93\x92\x94\x95\x94\x95\x97\x97\x98\x97\x94\x90\x8d\x86\x82\x7fyupmg`]VRLEB?=;99665422202101///-//.-0-.-/..--,.-+-,--+.,,--,,-*\x00 \xa1\x07 \xa1\x07\x00@\xc4`^\x0c\x00\x00\x00\x15j",
    b"\xb5b\r\x01\x10\x00\x88gh\x16\x00\x00\x00\x00\x00\x00\x00\x00\x85\x08\x1b\x0fB\xff",
    b"\xb5b\x05\x01\x02\x00\x06\x01\x0f\x38",
    b"\xb5b\x06\x01\x08\x00\xf0\x01\x00\x01\x01\x01\x00\x00\x036",
    b"\xb5b\x06\x00\x00\x00\x06\x18",
    b"\xb5b\x01\x12$\x000D\n\x18\xfd\xff\xff\xff\xf1\xff\xff\xff\xfc\xff\xff\xff\x10\x00\x00\x00\x0f\x00\x00\x00\x83\xf5\x01\x00A\x00\x00\x00\xf0\xdfz\x00\xd0\xa6",
    b"\xb5b\x06\x17\x04\x00\x00\x00\x00\x00\x21\xe9",
    b"\xb5b\x06\x17\x0c\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x29\x61",
    b"\xb5b\x13\x80\x0e\x00\x01\x02\x03\x04\x05\x06\x07\x08\x09\x0a\x0b\x0c\x01\x02\xf2\xc2",
    b"\xb5b\x13\x21\x06\x00\x03\x01\x02\x00\x00\x04\x44\x3a",
    b"\xb5b\x06\x8b\x0c\x00\x00\x00\x00\x00\x01\x00\x52\x40\x80\x25\x00\x00\xd5\xd0",
    b"\xb5b\x06\x8b\x09\x00\x00\x00\x00\x00\x01\x00\x51\x20\x55\x61\xc2",
    b"\xb5b\x06\x8b\x16\x00\x00\x00\x00\x00\x01\x00\x51\x20\x55\x01\x00\x52\x40\x80\x25\x00\x00\x02\x00\x21\x30\x23\x1c\x92",
    b"\xb5b\x06\x8b\x0c\x00\x00\x00\x00\x00\x68\x00\x11\x40\xb6\xf3\x9d\x3f\xdb\x3d",
    b"\xb5b\x10\x02\x1c\x00\x6d\xd8\x07\x00\x18\x20\x00\x00\xcd\x06\x00\x0e\xe4\xfe\xff\x0d\x03\xfa\xff\x05\x09\x0b\x00\x0c\x6d\xd8\x07\x00\xee\x51",
    b"\xb5b\x10\x02\x18\x00\x72\xd8\x07\x00\x18\x18\x00\x00\x4b\xfd\xff\x10\x40\x02\x00\x11\x23\x28\x00\x12\x72\xd8\x07\x00\x03\x9c",
    b"\xb5b\n1\x14\x01\x00\x01\x00\x00-+-,+-.,-.+,+.-..-,..//./00203017?9398:L]<@C;H<>=A@BDCGJNQRVY[_cgpqyz\x7f\x84\x8c\x90\x99\xa0\xa7\xae\xb0\xae\xaa\xa7\xa2\x9b\x97\x96\x94\x91\x90\x8e\x8c\x8c\x8c\x8b\x8b\x89\x88\x89\x89\x89\x8b\x88\x89\x8a\x89\x8a\x8a\x89\x8a\x8b\x8a\x8a\x8b\x8b\x8c\x8a\x8a\x8a\x8b\x88\x88\x87\x87\x86\x85\x85\x85\x84\x89\x84\x85\x83\x84\x84\x84\x85\x88\x87\x87\x88\x8a\x8a\x8a\x8a\x8b\x8e\x8c\x8d\x8d\x8f\x8e\x8d\x8f\x8e\x8f\x8f\x8e\x8f\x8f\x90\x91\x92\x93\x93\x93\x95\x94\x94\x94\x94\x95\x94\x95\x93\x93\x91\x92\x93\x92\x94\x95\x94\x95\x97\x97\x98\x97\x94\x90\x8d\x86\x82\x7fyupmg`]VRLEB?=;99665422202101///-//.-0-.-/..--,.-+-,--+.,,--,,-*\x00 \xa1\x07 \xa1\x07\x00@\xc4`^\x0c\x00\x00\x00\x15j",
]


def progbar(i: int, lim: int, inc: int = 20):
    """
    Display progress bar on console.

    :param int i: iteration
    :param int lim: max iterations
    :param int inc: bar increments (20)
    """

    i = min(i, lim)
    pct = int(i * inc / lim)
    if not i % int(lim / inc):
        print("\u2593" * pct + "\u2591" * (inc - pct), end="\r")


def benchmark(**kwargs) -> float:
    """
    pyubx2 Performance benchmark test.

    :param int cycles: (kwarg) number of test cycles (10,000)
    :returns: benchmark as transactions/second
    :rtype: float
    :raises: UBXStreamError
    """

    cyc = int(kwargs.get("cycles", 10000))
    txnc = len(UBXMESSAGES)
    txnt = txnc * cyc

    print(
        f"\nOperating system: {osver()}",
        f"\nPython version: {python_version()}",
        f"\npyubx2 version: {ubxver}",
        f"\nTest cycles: {cyc:,}",
        f"\nTxn per cycle: {txnc:,}",
    )

    start = datetime.now()
    print(f"\nBenchmark test started at {start}")
    for i in range(cyc):
        progbar(i, cyc)
        for msg in UBXMESSAGES:
            _ = UBXReader.parse(msg)
    end = datetime.now()
    print(f"Benchmark test ended at {end}.")
    duration = (end - start).total_seconds()
    rate = round(txnt / duration, 2)

    print(
        f"\n{txnt:,} messages processed in {duration:,.3f} seconds = {rate:,.2f} txns/second.\n"
    )

    return rate


def main():
    """
    CLI Entry point.

    args as benchmark() method
    """

    benchmark(**dict(arg.split("=") for arg in argv[1:]))


if __name__ == "__main__":

    main()
