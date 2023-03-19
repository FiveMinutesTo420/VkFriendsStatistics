import os
import requests
from statistics import mean
import datetime
import sys
from dotenv import load_dotenv

load_dotenv()
API_TOKEN = os.getenv("API_TOKEN")
cur_year = datetime.datetime.now().year
line = "-----------"

user_id = input("Enter ID vk: ")
print(" ")
# request to get a user's friends
req = f"https://api.vk.com/method/friends.get?user_id={user_id}&order=name&fields=bdate,sex&access_token={API_TOKEN}&v=5.131"
# request to get a user
user_query = f"https://api.vk.com/method/users.get?user_ids={user_id}&name_case=gen&access_token={API_TOKEN}&v=5.131"

r_user = requests.get(user_query)
user_data = r_user.json()

if ("error" in user_data):
    sys.exit(user_data['error']['error_msg'])
# writing user's data in variable
user = user_data['response'][0]

r = requests.get(req)
data = r.json()
if ("error" in data):
    sys.exit(data['error']['error_msg'])

# writing all user's friends in variable
friends = data['response']['items']
# total count of user's friend
count = data['response']['count']

no_bdate = 0
ages = []
middle_age = 0

females_count = 0
males_count = 0
no_gender = 0

names = []
surnames = []

c_most_common_name = 0
most_common_name = None
c_most_common_surname = 0
most_common_surname = None

for friend in friends:
    # counts amount of friends who's not not specified their birthday
    if "bdate" not in friend:
        no_bdate += 1
    else:
        # counts amount of friends who's specified only day and month of their birthday
        if (len(friend['bdate'].split('.')) == 2):
            no_bdate += 1
        else:
            # records all birthdays that is fewer than 1950
            if (int(friend['bdate'].split('.')[-1]) >= 1950):
                ages.append(int(friend['bdate'].split('.')[-1]))
    # counts amount of females and males
    if friend['sex'] == 1:
        females_count += 1
    elif friend['sex'] == 2:
        males_count += 1
    else:
        no_gender += 1
    # records all friends names and last names
    names.append(friend['first_name'])
    surnames.append(friend['last_name'])

# counts and writing most common name
for name in names:
    n = names.count(name)
    if n > c_most_common_name:
        c_most_common_name = n
        most_common_name = name
# counts and writing most common surname

for surname in surnames:
    s = surnames.count(surname)
    if s > c_most_common_surname:
        c_most_common_surname = s
        most_common_surname = surname
# counts percentage of males and females
percent_males = round((males_count / count) * 100, 1)
percent_females = round((females_count / count) * 100, 1)

# gets average age of friends
middle_age = int(mean(ages))

# output data
print(f"{line}Информация{line}")
print(f"Всего друзей у {user['first_name']} {user['last_name']} - {count}")
print(" ")
print("Из них: ")
print(f"------- {males_count} мужского пола ({percent_males}%)")
print(f"------- {females_count} женского пола ({percent_females}%)")
print(f"------- {no_bdate} не указали год рождения")
print(" ")
print(
    f"Средний год рождения(на основе тех, кто указал год рождения не менее 1950 года): {middle_age}")
print(f"Средний возраст: {cur_year - middle_age} ")
if (c_most_common_name != 1):
    print(
        f"Самое частое имя - {most_common_name}, встречается аж целых {c_most_common_name} раза ")
else:
    print("Нет повторяющихся имен")
if (c_most_common_surname != 1):
    print(
        f"Самая частая фамилия - {most_common_surname}, встречается аж целых {c_most_common_surname} раза")
else:
    print("Нет повторяющихся фамилий")
print(" ")
