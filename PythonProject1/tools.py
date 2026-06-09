import requests
from datetime import datetime


# Tool 1：查询天气
def get_weather(city):
    """
    查询城市天气
    """
    try:
        url = f"https://wttr.in/{city}?format=j1"

        response = requests.get(url, timeout=10)

        data = response.json()

        current = data["current_condition"][0]

        result = {
            "city": city,
            "temperature": current["temp_C"],
            "humidity": current["humidity"],
            "weather": current["weatherDesc"][0]["value"]
        }

        return str(result)

    except Exception as e:
        return f"天气查询失败: {str(e)}"


# Tool 2：查询时间
def get_current_time():
    """
    获取当前时间
    """
    now = datetime.now()

    return now.strftime("%Y-%m-%d %H:%M:%S")