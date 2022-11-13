#!/usr/bin/env python3
# -*- mode: python; coding: utf-8; fill-column: 80; -*-
#
# Ref: https://curl.se/libcurl/c/curl_easy_getinfo.html
# Ref: https://blog.cloudflare.com/a-question-of-timing/
#
"""Parse output of `curl` to retrieve various measurements.
"""

import io
import sys


DATA_RES  = 'RES'
DATA_SIZE = 'SIZE'
DATA_TIME = 'TIME'

OUT_COLS = ('url', 'srvip',
            'dns', 'tcp', 'ssl', 'pre', 'beg', 'total',
            'rtt', 'ttfb', 'taround',
            'req', 'header', 'download')
OUT_DELIM = ','


def parse_tags(line, data, tag, tag_type=float):
    """parse output and gather measurements of given type."""
    if not line or not line.startswith(tag):
        return line
    dtype, meas, val = line.split()
    if dtype != tag:
        raise ValueError(f"Malformed input: `{line}`")
    data[meas] = tag_type(val)
    return None


def proc_meas(meas):
    """Process measurements."""
    meas['rtt'] = meas['tcp'] - meas['dns']
    meas['ttfb'] = meas['beg'] - meas['ssl']
    meas['taround'] = meas['ttfb'] - meas['rtt']


def fmt_value(val):
    """Format value into a readable string."""
    if type(val) is float:
        return f"{val:8.6f}"
    else:
        return str(val)

def emit_meas(stream, meas):
    """Emit measurements."""
    line = OUT_DELIM.join(fmt_value(meas[f]) for f in OUT_COLS)
    stream.write(f"{line}\n")


def main(input, output):
    lines = (line.strip() for line in input)

    meas = {}
    # Extract different types of measurements.
    timings = lambda line: parse_tags(line, meas, DATA_TIME)
    sizes   = lambda line: parse_tags(line, meas, DATA_SIZE, int)
    req     = lambda line: parse_tags(line, meas, DATA_RES, str)

    # Header.
    out_cols = ','.join(OUT_COLS)
    output.write(f"# {out_cols}\n")

    for line in lines:
        req(sizes(timings(line)))

    proc_meas(meas)
    emit_meas(output, meas)


def _wrap(s):
    return io.TextIOWrapper(s, encoding='utf-8')


if __name__ == '__main__':
    main(_wrap(sys.stdin.buffer), _wrap(sys.stdout.buffer))
