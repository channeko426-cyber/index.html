import json
import urllib.request
from datetime import datetime, timedelta

LAT, LON = 37.11, 138.00

def fetch_json(url):
    with urllib.request.urlopen(url) as response:
        return json.loads(response.read().decode())

try:
    # 3日分のデータを取得
    marine_url = f"https://open-meteo.com{LAT}&longitude={LON}&hourly=wave_height,wave_period,wave_direction&timezone=Asia%2FTokyo&forecast_days=3"
    weather_url = f"https://open-meteo.com{LAT}&longitude={LON}&hourly=wind_speed_10m,wind_direction_10m,weather_code,temperature_2m&timezone=Asia%2FTokyo&forecast_days=3"

    m_data = fetch_json(marine_url)
    w_data = fetch_json(weather_url)

    times = m_data["hourly"]["time"]
    hourly_list = []

    for i in range(len(times)):
        hourly_list.append({
            "time": times[i],
            "wave_height": m_data["hourly"]["wave_height"][i],
            "wave_period": m_data["hourly"]["wave_period"][i],
            "wave_direction": m_data["hourly"]["wave_direction"][i],
            "wind_speed": w_data["hourly"]["wind_speed_10m"][i],
            "wind_direction": w_data["hourly"]["wind_direction_10m"][i],
            "weather_code": w_data["hourly"]["weather_code"][i],
            "temperature": w_data["hourly"]["temperature_2m"][i]
        })

    # 日本の現在時刻を記録
    jst_now = (datetime.utcnow() + timedelta(hours=9)).strftime("%Y/%m/%d %H:%M")

    output = {
        "updated_at": jst_now,
        "hourly_data": hourly_list
    }

    with open("data.json", "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
    print("Data file generated successfully!")

except Exception as e:
    print(f"Error occurred: {e}")
