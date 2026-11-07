import os
import json
import requests
import xml.etree.ElementTree as ET

API_KEY = os.environ.get("YOUTUBE_API_KEY")
CHANNEL_ID = "UCV4UK9LNNLViFP4qZA_Wmfw"
UPLOADS_PLAYLIST_ID = "UUV4UK9LNNLViFP4qZA_Wmfw"

def fetch_youtube_posts():
    posts = []

    # Attempt 1: YouTube API
    if API_KEY:
        try:
            url = f"https://www.googleapis.com/youtube/v3/playlistItems?key={API_KEY}&playlistId={UPLOADS_PLAYLIST_ID}&part=snippet&maxResults=25"
            res = requests.get(url, timeout=10)
            if res.status_code == 200:
                data = res.json()
                for item in data.get("items", []):
                    snippet = item.get("snippet", {})
                    video_id = snippet.get("resourceId", {}).get("videoId")
                    if video_id:
                        posts.append({
                            "platform": "YouTube",
                            "title": snippet.get("title", "Untitled Upload"),
                            "url": f"https://www.youtube.com/watch?v={video_id}",
                            "published_at": snippet.get("publishedAt", ""),
                            "thumbnail": snippet.get("thumbnails", {}).get("high", {}).get("url", "")
                        })
                if posts:
                    return posts
        except Exception as e:
            print(f"API fetch failed: {e}")

    # Fallback: Official Channel RSS Feed
    try:
        print("Using RSS fallback for YouTube...")
        rss_url = f"https://www.youtube.com/feeds/videos.xml?channel_id={CHANNEL_ID}"
        res = requests.get(rss_url, timeout=10)
        if res.status_code == 200:
            root = ET.fromstring(res.text)
            ns = {'atom': 'http://www.w3.org/2005/Atom', 'yt': 'http://www.youtube.com/xml/schemas/2015'}
            for entry in root.findall('atom:entry', ns):
                title = entry.find('atom:title', ns).text if entry.find('atom:title', ns) is not None else 'Untitled'
                link_elem = entry.find('atom:link', ns)
                link = link_elem.attrib['href'] if link_elem is not None else ''
                published = entry.find('atom:published', ns).text if entry.find('atom:published', ns) is not None else ''
                posts.append({
                    "platform": "YouTube",
                    "title": title,
                    "url": link,
                    "published_at": published,
                    "thumbnail": ""
                })
    except Exception as e:
        print(f"RSS fetch failed: {e}")

    return posts

def save_social_data(data):
    os.makedirs("data", exist_ok=True)
    with open("data/social_posts.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)
    print(f"Saved {len(data)} social posts")

if __name__ == "__main__":
    save_social_data(fetch_youtube_posts())
