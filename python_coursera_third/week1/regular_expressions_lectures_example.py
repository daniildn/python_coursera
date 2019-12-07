import re
nicknames = ["scvbfgefgdfgdfg", "alёna", "ivan ivanovich"]
reg = re.compile(r"^\w+$", re.ASCII)
for nick in nicknames:
    print("{} nickname: '{}'".format(
        "valid" if reg.match(nick) else "invalid", nick
    ))

text = "Анна и Лена загорали на берегу рекикогда к ним подошнл Яна и Ильнар"

print(re.findall(r"\b[А-Я]\w*(?:на|НА)\b", text))


text="как защитить металл от коррозии "

print(type(re.findall(r"(\w){2,}", text)))


print(re.sub(r"[а|A]","s", text))


