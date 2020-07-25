import pafy
import json
import os
from typing import List
from youtube_search import YoutubeSearch

pafy.set_api_key(os.environ['GOOGLE_API_KEY'])


class Youtube:

    @staticmethod
    def search(query: str, results: int = 10) -> List[str]:
        def extract_url(result):
            return f"https://www.youtube.com{result['url_suffix']}"
        results = YoutubeSearch(query, max_results=results).to_json()
        return list(map(extract_url, json.loads(results)['videos']))

    @staticmethod
    def get_audio_url(url: str) -> str:
        video = pafy.new(url)
        return video.getbestaudio().url
