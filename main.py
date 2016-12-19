import muffin
import json
import os
import subprocess as sp
import aiohttp as ah
from pathlib import Path
from hubstorage import HubstorageClient

app = muffin.Application('devsrv')

@app.register('/')
def root(request):
    return 'server is running!'

#@app.register('/linktv')
#def linktv(request):
#    html = '<p><a href="linktv/reload">reload</a></p>\n'
#    for item in program_list:
#        html += "<p>\n"
#        title = item["title"]
#        keyword = item["keyword"]
#        filename = item["filename"]
#        html += load_links(title, filename)
#        html += "</p>\n"
#    return html

#def load_links(title, filename):
#    html = "<B>{}</B>\n".format(title)
#    scrapy_proj = "linktv"
#    path = Path(scrapy_proj + "/" + filename)
#    if not path.is_file():
#        return html
#
#    os.chdir(scrapy_proj)
#
#    with open(filename) as f:
#        j = json.load(f)
#
#    html += "<ul>\n"
#    titles = sorted(j, key=lambda k: k['date'], reverse=True)
#    for title in titles:
#        date = title['date']
#        links = title['link']
#        html += "<li>{}: ".format(date)
#        for i in range(len(links)):
#            html += "<a href=\"" + links[i] + "\">link#{}".format(i+1) + "</a> "
#        html += "\n"
#    html += "</ul>\n"
#
#    os.chdir("..")
#    return html

#@app.register('/linktv/reload')
#def crawl_links(request):
#    scrapy_proj = "linktv"
#    os.chdir(scrapy_proj)
#    for item in program_list:
#        keyword = item["keyword"]
#        filename = item["filename"]
#        sp.Popen(["scrapy", "crawl", scrapy_proj, "-o", filename, "-t", "json",
#                  "-a", "keyword={}".format(keyword)])
#    os.chdir("..")
#    return muffin.HTTPFound('/linktv')

@app.register('/linktv')
def linktv(request):
    data = fetch_from_hc()
    html = ""
    for name, v in data.items():
        html += "<p>\n"
        html += "<B>{}</B>\n".format(name)
        html += "<ul>\n"
        for date in sorted(v.keys(), reverse=True):
            links = v[date]
            html += "<li>{}: ".format(date)
            for i in range(len(links)):
                html += "<a href=\"" + links[i] + "\">link#{}".format(i+1) + "</a> "
            html += "\n"
        html += "</ul>\n"
        html += "</p>\n"
    return html

def fetch_from_hc():
    APIKEY = 'fa73d9f566ea472b93fdcfabfd602fdd'
    PROJECT = '134699'
    hc = HubstorageClient(auth=APIKEY)
    project = hc.get_project(PROJECT)
    j_meta = project.jobq.list()
    j_finished = [j for j in j_meta if j['state'] == 'finished']
    j_sorted = sorted(j_finished, key=lambda k: k['finished_time'], reverse=True)
    j_key = j_sorted[0]['key']
    items = hc.get_job(j_key).items.list()
    data = {}
    for i in items:
        name = i['name']
        date = i['date'][0]
        link = i['link']
        if not name in data:
            data[name] = {}
        data[name][date] = link
    return data

if __name__ == '__main__':
    app.manage()

