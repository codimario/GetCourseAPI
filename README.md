# GetCourseAPI

Пытаюсь провести экспорт пользователей как указано в документации https://getcourse.ru/help/api#users.

* Вместо {account_name} вставил значение Account name со страницы https://get.storytellers.online/saas/account/api
* Вместо {secret_key} вставил сгенерированный ключ с той же страницы https://get.storytellers.online/saas/account/api


### Первый запрос выполняется корректно и возвращает export_id ✅
```python
url = f'https://{account_name}.getcourse.ru/pl/api/account/users?key={secret_key}&created_at[from]=2022-01-01'
try:
    response = requests.get(url, verify=True)
    if response.ok:
        response_json = response.json() 
        print(response_json)
        if "export_id" in response_json["info"]:
            export_id = response_json["info"]["export_id"]
```

### Второй запрос выполняется с ошибкой и возвращает 404 ❌
Передаем export_id, полученное в пункте 1:
```python
            # Шаг 2: проверяем статус готовности экспорта
            url = f'https://{account_name}.getcourse.ru/pl/api/account/exports/{export_id}/status?key={secret_key}'
            while True:
                # ВОТ ТУТ ОШИБКА 404 В ЗАПРОСЕ exports ↓
                response = requests.get(url, verify=True)
                print(response.status_code)
                if response.ok:
                    response_json = response.json()
```

### Вот что печатается в консоли:
![image](https://user-images.githubusercontent.com/106590110/232912904-6b9997a8-fa50-4d08-a230-8eb40125f741.png)

### Предполагаемые ошибки:
1. В правильности {account_name} и {secret_key} не сомневаюсь, т.к. запрос на получение export_id проходит успешно.
2. Сомневаюсь в правильности написания фильтров, пробовал разные варианты, но ни один не сработал.

