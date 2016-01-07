FROM daocloud.io/python:2.7
ADD requirements.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt
RUN mkdir /code
COPY . /code
WORKDIR /code
EXPOSE 5000
