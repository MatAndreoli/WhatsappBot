#!/bin/bash

fuser -k 3000/tcp
. venv/bin/activate

cd WebScraper/
python3 main.py &
cd ..
npm start
