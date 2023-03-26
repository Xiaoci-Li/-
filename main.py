import requests, re
from bs4 import BeautifulSoup


def get_html(url, method='get', data=None):
    headers = {
        'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36",
    }
    if method == 'get':
        res = requests.get(url, headers=headers)
    else:
        res = requests.post(url, headers=headers, data=data)

    return res.text


def chapter_content(chapter_info):
    url = "https://www.biquzge.com/api/reader_js.php"
    page = 1
    while page < 5:
        data = {
            'articleid': '48047',
            'chapterid': chapter_info[0],
            'pid': page,
        }
        html = get_html(url, method='post', data=data)
        soup = BeautifulSoup(html, "html.parser")

        with open("%s.txt" % chapter_info[1], "a", encoding="utf-8") as f:
            for i in soup:
                f.write(i.text)
        page = page + 1

    print("%s\t---------OK---------" % chapter_info[1])


def chapters_list():
    '''
    https://www.biquzge.com/info/48047.html
    https://www.biquzge.com/info/48047/70040569.html
    '''
    host = "https://www.biquzge.com"
    url = host + '/info/48047.html'
    html = get_html(url, 'get')
    soup = BeautifulSoup(html, 'html.parser')
    tag = soup.find_all('div', class_='info-chapters flex flex-wrap')
    tag_a = tag[0].find_all('a')  # 0：新章节 1：所有章节
    chapters_list = []
    for each in tag_a:
        chapter_id = re.findall(r"/info/.*?/(.*?).html", each['href'])[0]
        chapter_name = each.text
        chapters_list.append((chapter_id, chapter_name))

    return chapters_list


if __name__ == '__main__':
    new_list = chapters_list()
    for i in new_list[1:]:
        chapter_content(i)
