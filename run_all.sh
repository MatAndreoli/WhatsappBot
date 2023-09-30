#!/bin/bash

fuser -k 3000/tcp

pip install virtualenv
VIRTUAL_ENV=venv

virtualenv -p python3.11 ${VIRTUAL_ENV}
PATH="$VIRTUAL_ENV/bin:$PATH"

. venv/bin/activate
${VIRTUAL_ENV}/bin/pip install -r requirements.txt

cd WebScraper/
${VIRTUAL_ENV}/bin/python main.py &

cd ..
npm start
