FROM python:3.10.7

WORKDIR /zohali

RUN chmod -R 755 /zohali

COPY requirements.txt ./

RUN apt-get -y update && apt-get install -y tesseract-ocr && apt install -y libtesseract-dev

RUN pip install -r requirements.txt

COPY . .

RUN chmod +x init.sh

ENTRYPOINT [ "sh", "init.sh"]
