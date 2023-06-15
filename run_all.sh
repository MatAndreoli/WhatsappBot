#!/bin/bash

. venv/bin/activate

cd WebScraper/
python3 main.py &
cd ..
npm start
