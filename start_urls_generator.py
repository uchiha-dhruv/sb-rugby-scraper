
class UrlGenSpider:
    name = 'test2'
    start_urls = [
        'https://rugby.statbunker.com/competitions/LastMatches?comp_id=646&limit=10&offs=UTC&offset='
    ]
    generated_urls = [start_urls[0]]
    for x in range(10, 50, 10):
        page_link = start_urls[0] + str(x)
        generated_urls.append(page_link)

    print(generated_urls)
