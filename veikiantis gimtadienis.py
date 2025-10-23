import datetime
import requests
import json

# Power Automate webhook URL
webhook_url = "https://defaultd8967df182fd49ae8495bfd989f50b.97.environment.api.powerplatform.com:443/powerautomate/automations/direct/workflows/02481b4ac87045109b5ed1244346f810/triggers/manual/paths/invoke?api-version=1&sp=/triggers/manual/run&sv=1.0&sig=17WbP6Cevdyr-ZuY7rb_GiVKcacSyZ43JQAXAkPthYc"

# Path to the birthday list file
FILE_PATH = "gimtadieniai.rtf"

def read_birthdays(file_path):
    birthdays = []
    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            parts = line.strip().split(";")
            if len(parts) >= 2:
                name = parts[0].strip()
                date_str = parts[1].strip()
                birthdays.append((name, date_str))
    return birthdays

def check_today_birthdays(birthdays):
    today = datetime.datetime.now().strftime("%m-%d")
    return [name for name, date in birthdays if date == today]

def send_text(message: str) -> None:
    payload = {"message": message}  # ← tik tekstas
    r = requests.post(
        webhook_url,
        json=payload,                       # siųsk kaip JSON
        headers={"Content-Type": "application/json"},
        timeout=15,
    )
    if r.status_code // 100 != 2:
        raise SystemExit(f"HTTP {r.status_code}: {r.text}")
    print("OK")

def main():
    birthdays = read_birthdays(FILE_PATH)
    today_birthdays = check_today_birthdays(birthdays)

    if today_birthdays:
        names = ", ".join(today_birthdays)
        message = f"🎉 Šiandien gimtadienį švenčia: {names}!"
        print(f"Siunčiama žinutė: {message}")
        send_text(message)
    else:
        print("📅 Šiandien nėra gimtadienių.")

if __name__ == "__main__":
    main()
