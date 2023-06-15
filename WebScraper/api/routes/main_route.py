from api import app, request
import subprocess

from flask import make_response


@app.route('/events')
def events():
    output = 'No error'
    try:
        subprocess.check_output(['scrapy', 'crawl', 'unisal-events'])
    except subprocess.CalledProcessError as e:
        output = e.output
    print(output)
    return make_response("<h1>Success</h1>", 200)

@app.route('/fiis')
def fiis():
    output = 'No error'
    try:
        fiis = request.args.get('fiis')
        subprocess.check_output(['scrapy', 'crawl', 'fiis-scraper', '-a', f'fiis={fiis}'])
        pass
    except subprocess.CalledProcessError as e:
        output = e.output
    print(output)
    return make_response("<h1>Success</h1>", 200)
