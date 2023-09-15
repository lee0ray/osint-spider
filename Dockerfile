FROM selenium/standalone-chrome


ADD osint/requirements.txt /root/
RUN apt update && apt upgrade && apt install python3 python3-pip && pip install install -r /root/requirements.txt -i http://mirrors.cloud.aliyuncs.com/pypi/simple/ --no-cache-dir
