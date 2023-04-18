# ЭКСПОРТ ПОЛЬЗОВАТЕЛЕЙ
# 1. Отправить действие users, секретный ключ и хотя бы один фильтр объектов для экспорта:
# «https://{account_name}.getcourse.ru/pl/api/account/users?key={secret_key}&....»
# 2. Отправить действие exports, ключ экспорта и секретный ключ:
# «https://{account_name}.getcourse.ru/pl/api/account/exports/{export_id}?key={secret_key}»

import requests
import time

account_name = "testAccount"
secret_key = "12345"

# Шаг 1: 
url = f'https://{account_name}.getcourse.ru/pl/api/account/users?key={secret_key}&created_at[from]=2022-01-01'
try:
    response = requests.get(url, verify=True)
    if response.ok:
        response_json = response.json() 
        print(response_json)
        if "export_id" in response_json["info"]:
            export_id = response_json["info"]["export_id"]
            
            # Шаг 2: проверяем статус готовности экспорта
            url = f'https://{account_name}.getcourse.ru/pl/api/account/exports/{export_id}/status?key={secret_key}'
            while True:
                # ВОТ ТУТ ОШИБКА 404 ЗАПРОС НА exports ↓
                response = requests.get(url, verify=True)
                print(response.status_code)
                
                if response.ok:
                    response_json = response.json()
                    # выводим ответ для дальнейшего анализа
                    print(response_json)
                    # проверяем статус экспорта
                    status = response_json["status"]
                    if status == "ready":
                        # Шаг 3: скачиваем файл экспорта
                        url = f'https://{account_name}.getcourse.ru/pl/api/account/exports/{export_id}/download?key={secret_key}'
                        response = requests.get(url, verify=True)
                        if response.ok:
                            with open('export.csv', 'wb') as f:
                                f.write(response.content)
                            print("Экспорт пользователей успешно сохранен в файле export.csv")
                            break
                    elif status == "in progress":
                        print(f'Текущий статус экспорта: {status}')
                        # ждем 10 секунд перед повторной проверкой статуса экспорта
                        time.sleep(10)
                    elif status == "failed":
                        print(f'Экспорт завершился с ошибкой. Статус экспорта: {status}')
                        break
        else:
            print("Не удалось создать экспорт")
except requests.exceptions.RequestException as e:
    print(e)
