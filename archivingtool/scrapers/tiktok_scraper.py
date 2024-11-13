# https://github.com/davidteather/tiktok-api
from TikTokApi import TikTokApi
import asyncio
import os

import json
from datetime import datetime

ms_token = os.environ.get(
    "ms_token", None
)  # set your own ms_token, think it might need to have visited a profile


async def scrape(video_url):
    async with TikTokApi() as api:
        await api.create_sessions(ms_tokens=[ms_token], num_sessions=1, sleep_after=3)
        video = api.video(url=video_url)

        video_info = await video.info()  # is HTML request, so avoid using this too much

        verified = "Unverified"
        if video_info.get('author').get('verified'):
            verified = "Verified"

        return {
            "Link to Disinformative Content" : video_url,
            'Date of Submission' : datetime.now().strftime('%d %b %Y'),
            "Summary" : video_info.get("desc"),
            "Date Posted" : datetime.fromtimestamp(int(video_info.get("createTime"))).strftime('%d %b %Y'),
            "Likes" : video_info.get("stats").get("diggCount"),
            "Views" : video_info.get('stats').get('playCount'),
            "Comments" : video_info.get("stats").get("commentCount"), # not included
            "Shares" : video_info.get("stats").get("shareCount"), # not included
            "Account Name" : video_info.get('author').get('nickname'),
            "Account URL" :  "https://www.tiktok.com/@grprm._" + video_info.get('author').get('uniqueId'), # not included
            "Status of the Post" : video_info.get("available"),
            "Account Verification" : verified,
            "Platform" : "TikTok",
            "Format" : "Video",
            "Primary Country" : video_info.get('locationCreated'),
        }
        
        # print(video_info.get('author').get('uniqueId'))
        # print(video_info.get('author').get('verified')) 
        # print(video_info.get('desc'))
        # print(video_info.get('music').get('title'))
        # print(video_info.get('stats').get('shareCount')) 
        # print(video_info.get('stats').get('playCount'))  
        # print(video_info.get('locationCreated')) 
        # print(video_info.keys())



if __name__ == "__main__":
    print(asyncio.run(scrape('https://www.tiktok.com/@grprm._/video/7277556717066456321')))
