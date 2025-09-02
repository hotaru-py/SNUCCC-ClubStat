import json
import httpx
import re

client = httpx.Client(
    headers={
        "x-ig-app-id": "936619743392459",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.9,ru;q=0.8",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept": "*/*",
    }
)


def IGscore(username: str):
    result = client.get(
        f"https://i.instagram.com/api/v1/users/web_profile_info/?username={username}",
    )
    data = json.loads(result.content)
    data = str(data["data"]["user"])

    rx = r"'edge_liked_by': \{'count': \d+\}"
    likes = re.findall(rx, data)

    tot_likes = sum(int(i.lstrip("'edge_liked_by': {'count': ").rstrip("}")) for i in likes)
    n = 12 # Number of posts fixed coz Instagram API limits to 12
    score = tot_likes/n
    
    return score
