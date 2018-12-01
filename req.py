import json
import os
import socket
import sys
import time

import requests
import urllib3

from secret import KEY


API_VERSION = '1.27.0.0'
ENGINE_VERSION = '201811_02a'
GCS_TOKYO = 'tokyo'


URL = 'http://api.ekispert.jp/v1/json/{}'

with open('codes.txt', 'r') as fp:
    CODES = [int(code_str) for code_str in fp.read().split()]


def _get_base(path, **kwargs):
    payload = {'key': KEY}
    for key, val in kwargs.items():
        payload[key] = val
    r = requests.get(URL.format(path), params=payload)
    if r.status_code != 200:
        sys.stderr.write(f'Error:{r.status_code} @{repr(kwargs)}\n')
        sys.stderr.flush()
        return None
    return r.json()

def _dump_base(json_obj, filename, dirname):
    with open(os.path.join(dirname, filename), 'w') as fp:
        json.dump(json_obj, fp)
    return

def _load_base(filename, dirname):
    with open(os.path.join(dirname, filename), 'r') as fp:
        json_obj = json.load(fp)
    return json_obj

def get_station(**kwargs):
    return _get_base('station', **kwargs)

def dump_station(code):
    json_obj = get_station(code=code)
    if json_obj is None:
        return
    return _dump_base(json_obj, f'st{code}.json', 'data/station/')

def load_station(code):
    json_obj = _load_base(f'st{code}.json', 'data/station/')
    return json_obj

def get_station_info(**kwargs):
    return _get_base('station/info', **kwargs)

def dump_station_info(code):
    json_obj = get_station_info(code=code, type='rail')
    if json_obj is None:
        return
    return _dump_base(json_obj, f'st_info{code}.json', 'data/station_info/')

def load_station_info(code):
    json_obj = _load_base(f'st_info{code}.json', 'data/station_info/')
    return json_obj

def main():
    for i, code in enumerate(CODES, 1):
        while True:
            try:
                dump_station(code)
            except (socket.gaierror,
                    urllib3.exceptions.PoolError,
                    urllib3.exceptions.MaxRetryError,
                    urllib3.exceptions.ConnectionError):
                time.sleep(60)
            else:
                time.sleep(1)
                break
        while True:
            try:
                dump_station_info(code)
            except (socket.gaierror,
                    urllib3.exceptions.PoolError,
                    urllib3.exceptions.MaxRetryError,
                    urllib3.exceptions.ConnectionError):
                time.sleep(60)
            else:
                time.sleep(1)
                break
        sys.stdout.write(str(code))
        if i % 10:
            sys.stdout.write('.')
        else:
            sys.stdout.write('\n')
        sys.stdout.flush()


if __name__ == '__main__':
    main()

