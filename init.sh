#!/bin/sh

set -eu

echo "[Checking database connection]"

i=0
until [ $i -ge 30 ]; do
    nc -z zohali-db 5432 && break

    i=$((i + 1))

    echo "$i: Waiting for database to start after $i second(s)..."
    sleep $i
done

if [ $i -eq 30 ]; then
    echo "Database connection refused, terminating ..."
    exit 1
fi

echo "Database is up ..."

export ENV=development && export TESSDATA_PREFIX=/usr/share/tesseract-ocr/4.00/tessdata && python3 serve.py
