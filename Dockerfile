FROM python:3.12

WORKDIR /root/dockerVerse

COPY requirements.txt requirements.txt

RUN pip install -U pip
RUN pip install --no-cache-dir -r requirements.txt

ENV IS_DOCKER_ENV=1

COPY . .

CMD ["python", "-m", "dockerVerse"]
