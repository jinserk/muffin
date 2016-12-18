import muffin
import json
import os
import subprocess as sp
import aiohttp as ah
from pathlib import Path

app = muffin.Application('devsrv')

program_list = [
    {"title": "JTBC 뉴스룸", "keyword": "jtbc 뉴스룸", "filename": "jtbc_news_room.json"},
    {"title": "JTBC 이규연의 스포트라이트", "keyword": "이규연의 스포트라이트", "filename": "jtbc_spotlight.json"},
    {"title": "JTBC 썰전", "keyword": "썰전", "filename": "jtbc_ssuljeon.json"},
    {"title": "SBS 그것이 알고싶다", "keyword": "그것이 알고 싶다 -", "filename": "sbs_want_to_know.json"},
]

@app.register('/')
def root(request):
    return 'server is running!'

@app.register('/linktv')
def linktv(request):
    html = '<p><a href="linktv/reload">reload</a></p>\n'
    for item in program_list:
        html += "<p>\n"
        title = item["title"]
        keyword = item["keyword"]
        filename = item["filename"]
        html += load_links(title, filename)
        html += "</p>\n"
    return html

def load_links(title, filename):
    html = "<B>{}</B>\n".format(title)
    scrapy_proj = "linktv"
    path = Path(scrapy_proj + "/" + filename)
    if not path.is_file():
        return html

    os.chdir(scrapy_proj)

    with open(filename) as f:
        j = json.load(f)

    html += "<ul>\n"
    titles = sorted(j, key=lambda k: k['date'], reverse=True)
    for title in titles:
        date = title['date']
        links = title['link']
        html += "<li>{}: ".format(date)
        for i in range(len(links)):
            html += "<a href=\"" + links[i] + "\">link#{}".format(i+1) + "</a> "
        html += "\n"
    html += "</ul>\n"

    os.chdir("..")
    return html

@app.register('/linktv/reload')
def crawl_links(request):
    scrapy_proj = "linktv"
    os.chdir(scrapy_proj)
    for item in program_list:
        keyword = item["keyword"]
        filename = item["filename"]
        sp.Popen(["scrapy", "crawl", scrapy_proj, "-o", filename, "-t", "json",
                  "-a", "keyword={}".format(keyword)])
    os.chdir("..")
    return muffin.HTTPFound('/linktv')


if __name__ == '__main__':
    app.manage()

