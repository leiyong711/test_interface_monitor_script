FROM python:3.9

WORKDIR /code
ADD ./requirements.txt /code

RUN pip3 install -r /code/requirements.txt --no-cache-dir -i https://pypi.tuna.tsinghua.edu.cn/simple
ADD . /code

CMD ["python"  "/code/main.py","-a 10.0.0.2 -p 65000 -n US-East -c 5"]
