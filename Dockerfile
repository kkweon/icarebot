FROM python:3.7.1-stretch
WORKDIR /code
ADD ./requirements.txt /code/requirements.txt
RUN pip install -r requirements.txt
VOLUME ["/tmp", "/code"]
CMD python icarebot/main.py -v
