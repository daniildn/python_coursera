import requests

# t = 'text'
# print('текст %s текст' % t)
# print('текст {} текст'.format(t))
ACCESS_TOKEN = '17da724517da724517da72458517b8abce117da17da72454d235c274f1a2be5f45ee711'
API_URL = 'https://api.vk.com/method'
V = '5.71'


def get_user_id(uid):
    userid = ''
    res = requests.get(API_URL + "/users.get", params={
        'access_token': ACCESS_TOKEN,
        'user_ids': uid,
        "v": V
    })
    try:
        res = res.json()["response"][0]
        userid = res["id"]
        # print(userid)
        return userid
    except:
        pass


def get_friends(user_id):
    res = requests.get(API_URL + "/friends.get", params={
        'access_token': ACCESS_TOKEN,
        'user_id': user_id,
        'fields': "bdate",
        "v": V
    })

    try:
        res = res.json()["response"]["items"]
        return res
    except:
        pass
    print(res.json())


def calc_age(uid):
    user_id = get_user_id(uid)
    if user_id is None:
        return
    friends = get_friends(user_id)
    if friends is None:
        return

    years = {}
    for friend in friends:
        bdate = friend.get("bdate")
        if not bdate:
            continue

        bdate = bdate.split(".")
        if len(bdate) != 3:
            continue
        year = int(bdate[2])
        diff = 2019 - year
        years.setdefault(diff, 0)
        years[diff] += 1

    return sorted(years.items(), key=lambda v: (v[1], -v[0]), reverse=True)


if __name__ == '__main__':
    res = calc_age('reigning')
    print(res)

# В итоге запросы будут иметь вид:

# – Для получения id пользователя по username или user_id:
#
# https://api.vk.com/method/users.get?v=5.71&access_token=[token]&user_ids=[user_id]
#
# – Для получения списка друзей:
#
# https://api.vk.com/method/friends.get?v=5.71&access_token=[token]&user_id=[user_id]&fields=bdate
#
