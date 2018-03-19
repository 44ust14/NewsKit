FROM python:3
RUN mkdir /newskit
WORKDIR /newskit

RUN pip install flask
RUN pip install bs4
RUN pip install requests
RUN pip install lxml
RUN pip install scrapy
