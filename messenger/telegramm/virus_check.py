import requests
import time

def virus_check(user_id):
    if user_id == 5131136267:
        return "admin"
    else:
        file_path = f"D:\\windos_custom\\messenger\\storage\\user_files\\{user_id}.zip"
        api_key = "your_api_token"

        url_scan = "https://www.virustotal.com/api/v3/files"
        headers = {
            "x-apikey": api_key
        }

        # Отправка файла на сканирование
        with open(file_path, "rb") as file:
            files = {"file": (file_path, file)}
            response = requests.post(url_scan, headers=headers, files=files)
            response_data = response.json()
            analysis_id = response_data["data"]["id"]

        # Ожидание завершения анализа
        url_report = f"https://www.virustotal.com/api/v3/analyses/{analysis_id}"
        while True:
            response = requests.get(url_report, headers=headers)
            report = response.json()
            status = report["data"]["attributes"]["status"]
            if status == "completed":
                break
            time.sleep(10)  # Ожидание 10 секунд перед повторной проверкой

        results = report['data']['attributes']['results']
        detections = 0
        for scanner, result in results.items():
            if result['category'] == 'malicious':
                detections += 1
                print(f"{scanner}: {result['category']} - {result['result']}")

        if detections > 0:
            return [False,f"Обнаружено {detections} антивирусных движков, пометивших файл как вредоносный."]
        else:
            return True