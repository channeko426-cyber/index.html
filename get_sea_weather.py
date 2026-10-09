import json
import urllib.request
import sys
from datetime import datetime, timedelta

def fetch_json(url):
    print(f"🚀 [FETCHING URL]: {url}")
    req = urllib.request.Request(
        url, 
        headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
    )
    with urllib.request.urlopen(req, timeout=15) as response:
        return json.loads(response.read().decode())

try:
    # パラメータが完全に固定された安全なURL
    marine_url = "https://open-meteo.com"
    weather_url = "https://open-meteo.com"

    m_data = fetch_json(marine_url)
    print("✅ Marine data fetched successfully.")
    
    w_data = fetch_json(weather_url)
    print("✅ Weather data fetched successfully.")

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
    print("🎉 SUCCESS: data.json has been created completely!")

except Exception as e:
    print(f"🚨 ERROR OCCURRED: {e}", file=sys.stderr)
    sys.exit(1)
