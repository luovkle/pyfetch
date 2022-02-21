#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import socket
import os
import platform


class Color:
    END = "\33[0m"
    BOLD = "\033[1m"
    YELLOW = "\33[33m"
    RED = '\033[91m'
    BLUE = "\033[94m"


ascii_art = (
    f"{Color.BOLD}{Color.BLUE}     .,:::;'.     {Color.END}",
    f"{Color.BOLD}{Color.BLUE}     :.;:::::     {Color.END}",
    f"{Color.BOLD}{Color.BLUE}  ...,,'':::: ::' {Color.END}",
    f"{Color.BOLD}{Color.BLUE}':::::::::;;, {Color.YELLOW}KKKx{Color.END}",
    f"{Color.BOLD}{Color.BLUE};::: '{Color.YELLOW}ccccccckKKKK{Color.END}",
    f"{Color.BOLD}{Color.BLUE} :::.{Color.YELLOW}KKKKKKKKKKK0 {Color.END}",
    f"{Color.BOLD}{Color.YELLOW}     KKKKdddd.    {Color.END}",
    f"{Color.BOLD}{Color.YELLOW}     .KKKKO'k     {Color.END}",
)


def get_title() -> str:
    name = os.getlogin()
    hostname = socket.gethostname()
    return f"{name}@{hostname}"


def get_os() -> str:
    with open("/etc/os-release", "r") as f:
        content = f.readlines()
        name = content[0].rstrip()
        o_system = name.removeprefix('NAME="').removesuffix('"')
        return o_system


def get_host() -> str:
    with open("/sys/devices/virtual/dmi/id/product_name", "r") as f:
        host = f.read().rstrip()
        return host


def get_kernel() -> str:
    return platform.release()


def get_uptime() -> str:
    with open("/proc/uptime", "r") as f:
        fields = f.read().split()
        hours = float(fields[0]) / 60 / 60
        minutes = (hours % 1) * 60
        return f"{int(hours)}h {int(minutes)}m"


def get_private_ip() -> str:
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.connect(("1.1.1.1", 80))
        ip = s.getsockname()[0]
        return ip


def get_memory() -> str:
    mems = {}
    with open("/proc/meminfo", "r") as f:
        for line in f:
            fields = line.split()
            key = fields[0].removesuffix(":")
            value = int(fields[1])
            mems.update({key: value})
    total = mems["MemTotal"]
    free = mems["MemFree"]
    buffers = mems["Buffers"]
    cache = mems["Cached"] + mems["SReclaimable"]
    buff_cache = buffers + cache
    used = total - free - buff_cache
    return f"{int(used / 1024)}M / {int(total / 1024)}M"


def main() -> None:
    data = {
        "title": f"{Color.YELLOW}{Color.BOLD}{get_title()}{Color.END}",
        "os": f"{Color.BOLD}os{Color.END}\t{get_os()}",
        "host": f"{Color.BOLD}host{Color.END}\t{get_host()}",
        "kernel": f"{Color.BOLD}kernel{Color.END}\t{get_kernel()}",
        "uptime": f"{Color.BOLD}uptime{Color.END}\t{get_uptime()}",
        "ip": f"{Color.BOLD}ip{Color.END}\t{get_private_ip()}",
        "memory": f"{Color.BOLD}memory{Color.END}\t{get_memory()}",
    }
    keys = ()
    for key in data:
        keys += (key,)
    iterations = len(ascii_art) if len(ascii_art) > len(keys) else len(keys)
    for idx in range(iterations):
        ascii_art_line = ascii_art[idx] if idx < len(ascii_art) else ""
        data_line = data[keys[idx]] if idx < len(keys) else ""
        print(f"{ascii_art_line}\t{data_line}")


if __name__ == "__main__":
    if platform.system() == "Linux":
        main()
    else:
        print(f"{Color.RED}Operating system not supported.{Color.END}")
