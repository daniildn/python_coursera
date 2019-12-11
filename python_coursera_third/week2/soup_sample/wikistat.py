import os
import re

from bs4 import BeautifulSoup


# Вспомогательная функция, её наличие не обязательно и не будет проверяться
def build_tree(start, end, path):
    link_re = re.compile(r"(?<=/wiki/)[\w()]+")  # Искать ссылки можно как угодно, не обязательно через re
    files = dict.fromkeys(os.listdir(path), False)  # Словарь вида {"filename1": None, "filename2": None, ...}
    queue_of_links = [start]
    while queue_of_links:
        link_for_next_layer = []
        for p in queue_of_links:
            with open("{}{}".format(path, p)) as file:
                links = re.findall(link_re, file.read())
                #
                for link in links:
                    if files.get(link) is False:
                        files[link] = p
                        if link == end:
                            return files

                        link_for_next_layer.append(link)
            queue_of_links = link_for_next_layer

def build_bridge(start, end, path):
    tree = build_tree(start, end, path)
    files = tree.copy()
    for file in tree.keys():
        if tree[file] is False :
            del files[file]
    acting_link, bridge = end, [end]
    while acting_link is not start:
        bridge.append(files[acting_link])
        acting_link = files[acting_link]
    return  bridge
def parse(start, end, path):
    """
    Если не получается найти список страниц bridge, через ссылки на которых можно добраться от start до end, то,
    по крайней мере, известны сами start и end, и можно распарсить хотя бы их: bridge = [end, start]. Оценка за тест,
    в этом случае, будет сильно снижена, но на минимальный проходной балл наберется, и тест будет пройден.
    Чтобы получить максимальный балл, придется искать все страницы. Удачи!
    """

    bridge = build_bridge(start, end, path)  # Искать список страниц можно как угодно, даже так: bridge = [end, start]

    # Когда есть список страниц, из них нужно вытащить данные и вернуть их
    out = {}
    for file in bridge:
        with open("{}{}".format(path, file)) as data:
            soup = BeautifulSoup(data, "lxml")

        body = soup.find(id="bodyContent")

        # TODO посчитать реальные значения
        imgs = 5  # Количество картинок (img) с шириной (width) не меньше 200
        headers = 10  # Количество заголовков, первая буква текста внутри которого: E, T или C
        linkslen = 15  # Длина максимальной последовательности ссылок, между которыми нет других тегов
        lists = 20  # Количество списков, не вложенных в другие списки

        out[file] = [imgs, headers, linkslen, lists]

    return out

# def parse(start, end, path):
#     bridge = build_bridge(start, end, path)
#
#     out = {}
#     for file in bridge:
#         with open("{}{}".format(path, file)) as data:
#             soup = BeautifulSoup(data, "lxml")
#             body = soup.find(id="bodyContent")
#
#             imgs = len(body.find_all('img', width=lambda x: int(x or 0) > 199))
#             headers = sum(
#                 1 for tag in body.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6']) if tag.get_text()[0] in "ETC"
#             )
#             lists = sum(1 for tag in body.find_all(['ol', 'ul']) if not tag.find_parent(['ol', 'ul']))
#
#             tag = body.find_next("a")
#             linkslen = -1
#             while (tag):
#                 curlen = 1
#                 for tag in tag.find_next_siblings():
#                     if tag.name != 'a':
#                         break
#                     curlen += 1
#                 if curlen > linkslen:
#                     linkslen = curlen
#                 tag = tag.find_next("a")
#
#             out[file] = [imgs, headers, linkslen, lists]
#
#     return out
