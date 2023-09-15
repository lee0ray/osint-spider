#!/bin/bash


mkdir -p /root/spiders/logs

scrapyd 2>&1 1>/root/spiders/logs/scrapyd.log &

gerapy init /root/spiders/gerapy
cd /root/spiders/gerapy
gerapy migrate
gerapy runserver 0.0.0.0:8000 2>&1 1>/root/spiders/logs/gerapy.log
