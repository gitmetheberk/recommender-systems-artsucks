#!/bin/bash

cd frontend

lcp --proxyUrl http://104.236.113.146:8000 > lcp.log&

echo LCP started
