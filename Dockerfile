FROM python:3.10.7

WORKDIR /zohali

COPY requirements.txt ./

RUN apt-get -y update && apt-get install -y tesseract-ocr && apt install -y libtesseract-dev

ENV TESSDATA_PREFIX=/usr/share/tesseract-ocr/4.00/tessdata

RUN pip install -r requirements.txt

COPY . .

CMD ["python", "./app/parser.py"]
