
import os
import json
import requests

API_KEY = os.getenv("YOUTUBE_API_KEY")
BASE_URL = "https://www.googleapis.com/youtube/v3"
CHANNELS = {
    "@riki": "Riki",
    "@smeshariki": "TVSmeshariki"}

# отправка запросов к API. Принимает название ресурса API и список параметров, значения которых хотим получить
def api_get(endpoint, params):
    response = requests.get(
        f"{BASE_URL}/{endpoint}",
        params={**params, "key": API_KEY},
        timeout=30)
    response.raise_for_status()
    return response.json()


def get_channel(handle, expected_name):
    data = api_get(
        "channels",
        {"part": "snippet," #Название канала и другие основные сведения
                 "contentDetails", #Дополнительные сведения о контенте, в том числе id плейлиста загруженных видео
            "forHandle": handle})

    items = data.get("items", [])
    if not items:
        raise ValueError(f"Канал {handle} не найден")

    channel = items[0]
    return {
        "handle": handle,
        "expected_name": expected_name,
        "channel_id": channel["id"],
        "channel_title": channel["snippet"]["title"],
        "uploads_playlist": (
            channel["contentDetails"]
            ["relatedPlaylists"]["uploads"])
    }

if not API_KEY:
    raise ValueError("Не задана переменная YOUTUBE_API_KEY")

channels_data = {}

for handle, name in CHANNELS.items():
    channel = get_channel(handle, name)

    channels_data[handle] = channel

    print(f"{handle}: {channel['channel_title']}")
    print(f"Channel ID: {channel['channel_id']}")
    print(f"Uploads playlist: {channel['uploads_playlist']}\n")


with open("youtube_channels.json", "w", encoding="utf-8") as file:
    json.dump(
        channels_data,
        file,
        ensure_ascii=False,
        indent=4
    )

print("Данные сохранены в youtube_channels.json")
