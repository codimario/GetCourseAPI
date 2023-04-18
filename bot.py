# https://{account_name}.getcourse.ru/pl/api/account
# https://{account_name}.getcourse.ru/pl/api/account/users?key={secret_key}&status=active
# https://storytellers.online.getcourse.ru/pl/api/account/users?key={secret_key}&tags=курс:Подписка
# https://storytellers.online.getcourse.ru/pl/api/account/exports/1234?key={secret_key}

import requests
import time

# params = {'status': 'active'} params=params
account_name = "storytellersonline"
secret_key = "HWVx4LHIRMXTAEPcWV0FzOQrWA8Ya5T7xJrv6F5WrjDFqVsNVRmfxU7sa5dvIeLBQ3Ll6WwiHKjobP7EhP3rMUJpxXfmK5ICwvHLkk0VWtGdvndpDR35lY2rnkaPJWH4"

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
                # ВОТ ТУТ ОШИБКА 404 ЗАПРОС НА exports ↑
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




















