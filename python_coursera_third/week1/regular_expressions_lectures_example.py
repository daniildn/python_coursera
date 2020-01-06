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

text = 'a123b45с6d'

def find_all_digits(text):
    exp = r'\D*?(\d+)\D*?'  #Тут напишите своё регулярное выражение
    return re.findall(exp, text)

print(find_all_digits(text))

