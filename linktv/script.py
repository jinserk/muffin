program_list = [
    {"title": "JTBC 뉴스룸", "keyword": "jtbc 뉴스룸", "filename": "jtbc_news_room.json"},
    {"title": "JTBC 이규연의 스포트라이트", "keyword": "이규연의 스포트라이트", "filename": "jtbc_spotlight.json"},
    {"title": "JTBC 썰전", "keyword": "썰전", "filename": "jtbc_ssuljeon.json"},
    {"title": "SBS 그것이 알고싶다", "keyword": "그것이 알고 싶다 -", "filename": "sbs_want_to_know.json"},
]

def crawl_links(request):
    print(request.host)
    scrapy_proj = "linktv"
    os.chdir(scrapy_proj)
    for item in program_list:
        keyword = item["keyword"]
        filename = item["filename"] sp.Popen(["scrapy", "crawl", scrapy_proj, "-o", filename, "-t", "json",
                  "-a", "keyword={}".format(keyword)])
    os.chdir("..")
    return muffin.HTTPFound('/linktv')


