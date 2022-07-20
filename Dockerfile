from ubuntu:latest

RUN apt-get update
RUN apt-get install --assume-yes --no-install-recommends --quiet python3 python3-pip
RUN apt-get clean all
RUN pip install --no-cache --upgrade pip setuptools

WORKDIR /app
COPY . /app
RUN pip --no-cache-dir install -r requirements.txt
EXPOSE 5000

ENTRYPOINT ["python3"]
CMD ["server.py"]
