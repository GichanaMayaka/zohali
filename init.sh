#!/bin/sh

export ENV=development && export TESSDATA_PREFIX=/usr/share/tesseract-ocr/4.00/tessdata && export POSTGRES_HOSTNAME=zohali-db && python3 serve.py