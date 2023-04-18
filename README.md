# GetCourseAPI

Пытаюсь получить данные пользователей
Есть курс (подписка), 
нужно получать данные по всем пользователям
проверять по введенной почте их в базе данных
возвращать ответ

Вместо {account_name} вставил имя указанное как Account name на странице https://get.storytellers.online/saas/account/api
Вместо {secret_key} вставил сгенерированный ключ на той же странице https://get.storytellers.online/saas/account/api


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

Вот что печатается в консоли:
![image](https://user-images.githubusercontent.com/106590110/232912904-6b9997a8-fa50-4d08-a230-8eb40125f741.png)



