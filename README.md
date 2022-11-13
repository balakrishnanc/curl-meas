# About

This repository consists of a configuration file for `curl` to gather various measurements when fetching a URL as well as a python script to parse that output and retrieve the web-performance measurements.

# Running

```
» curl --disable -K ./.curlrc <...url...> | ./parse-curl.py
```

Use `--disable` to ensure that `curl` ignores any other configuration files (in the paths that it searches by default).

# Example

```
» curl --disable -K ./.curlrc -I https://github.com | ./parse-curl.py
# url,srvip,dns,tcp,ssl,pre,beg,total,rtt,ttfb,taround,req,header,download
https://github.com/,140.82.121.4,0.061550,0.090141,0.127763,0.127880,0.156613,0.156687,0.028591,0.028850,0.000259,73,3180,0
```
