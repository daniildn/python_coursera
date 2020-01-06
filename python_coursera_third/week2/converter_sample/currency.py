from bs4 import BeautifulSoup

from decimal import Decimal
"""
В функцию convert(amount, cur_from, cur_to, date, requests) будет передана сумма amount в валюте с кодом cur_from, и её требуется перевести в валюту cur_to через рубль (код: RUR). Для запроса к API нужно использовать переданный requests, точнее, его метод get().

Все суммы и курсы требуется хранить в Decimal, т.к. для финансовых данных вычисления с фиксированной точкой подходят больше.
Конечный результат нужно округлить до 4-х знаков, перед тем как вернуть его из функции. Посмотрите метод quantize().

Для некоторых валют курс возвращается из расчета не на одну денежную единицу указанной валюты, а на 10 или даже 100, 
поэтому у курса валюты в XML есть не только Value, но и Nominal, и справедлива формула: Nominal ед. валюты = Value рублей.
При проверке на сервере сеть недоступна. В функцию будет передан фейковый requests, его интерфейс и response аналогичны настоящему. 
Если его использовать в объеме, требуемом для задания, разницы не будет заметно.
"""


# http://www.cbr.ru/scripts/XML_daily.asp?date_req=02/03/2002

def convert(amount, cur_from, cur_to, date, requests):

    response = requests.get("http://www.cbr.ru/scripts/XML_daily.asp", params={"date_req": date})
    soup = BeautifulSoup(response.content, "xml")
    if cur_from == "RUR":
        valueFrom = Decimal(1.0)
        nominalFrom = Decimal(1.0)
    else:
        valueFrom = Decimal(str(soup.find("CharCode", text=cur_from).find_next_sibling('Value').string).replace(",", "."))
        nominalFrom = Decimal(str(soup.find("CharCode", text=cur_from).find_next_sibling('Nominal').string).replace(",", "."))

    if cur_to == "RUR":
        value_to = Decimal(1.0)
        nominalFrom = Decimal(1.0)
    else:
        value_to = Decimal(
            str(soup.find("CharCode", text=cur_to).find_next_sibling('Value').string).replace(",", "."))
        nominal_to = Decimal(
            str(soup.find("CharCode", text=cur_to).find_next_sibling('Nominal').string).replace(",", "."))

    total = ((amount * valueFrom) / nominalFrom) / value_to * nominal_to
    total = total.quantize(Decimal(".0001"))

    return total