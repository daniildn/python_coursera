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
        if tree[file] is False:
            del files[file]
    acting_link, bridge = end, [end]
    while acting_link is not start:
        bridge.append(files[acting_link])
        acting_link = files[acting_link]
    return bridge


def parse(start, end, path):
    """
    Если не получается найти список страниц bridge, через ссылки на которых можно добраться от start до end, то,
    по крайней мере, известны сами start и end, и можно распарсить хотя бы их: bridge = [end, start]. Оценка за тест,
    в этом случае, будет сильно снижена, но на минимальный проходной балл наберется, и тест будет пройден.
    Чтобы получить максимальный балл, придется искать все страницы. Удачи!
    Длину максимальной последовательности ссылок, между которыми нет других тегов, открывающихся или закрывающихся.
     Например: <p><span><a></a></span>, <a></a>, <a></a></p> - тут 2 ссылки подряд,
     т.к. закрывающийся span прерывает последовательность. <p><a><span></span></a>, <a></a>, <a></a></p> - а тут 3 ссылки подяд, т.к. span находится внутри ссылки, а не между ссылками.
    """

    bridge = build_bridge(start, end, path)  # Искать список страниц можно как угодно, даже так: bridge = [end, start]

    # Когда есть список страниц, из них нужно вытащить данные и вернуть их
    out = {}
    for file in bridge:
        with open("{}{}".format(path, file)) as data:
            soup = BeautifulSoup(data, "lxml")

        body = soup.find(id="bodyContent")

        imgs = len(body.find_all("img", width=lambda x: int(x or 0) > 199))
        headers = len(
            [tag for tag in body.find_all(["h1", "h2", "h3", "h4", "h5", "h6"]) if tag.get_text()[0] in "ETC"])
        lists = len([tag for tag in body.find_all(["ol", "ul"]) if not tag.find_parents(["ol", "ul"])])
        # TODO посчитать реальные значения
        tag = body.find_next("a")
        linkslen = -1
        while tag:
            len_for_iter = 1
            for tag in tag.find_next_siblings():
                if tag.name != 'a':
                    break
                len_for_iter += 1
            if len_for_iter > linkslen:
                linkslen = len_for_iter
            tag = tag.find_next("a")
        # print(linkslen)

        out[file] = [imgs, headers, linkslen, lists]

    return out