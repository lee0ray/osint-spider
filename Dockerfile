FROM selenium/standalone-chrome
MAINTAINER zhangym2527@chinaunicom.cn

USER root

ADD osint/requirements.txt /root/
RUN sed s'/archive.ubuntu.com/mirrors.aliyun.com/g' /etc/apt/sources.list  -i  && \
    apt update -y && apt upgrade -y && apt install -y python3 python3-pip && \ 
    pip install install -r /root/requirements.txt -i https://mirrors.aliyun.com/pypi/simple/ --no-cache-dir && \
    cp /usr/share/zoneinfo/Asia/Shanghai /etc/localtime

ADD entrypoint.sh /root/

EXPOSE 8000

ENTRYPOINT ["/bin/bash", "/root/entrypoint.sh"]
