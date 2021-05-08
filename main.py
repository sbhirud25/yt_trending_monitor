import requests
import datetime
import isodate
import math
import csv
date_today = datetime.datetime.today().strftime("%d-%m-%Y")
listdict = {'1': 'Film & Animation', '2': 'Autos & Vehicles', '10': 'Music', '15': 'Pets & Animals', '17': 'Sports', '18': 'Short Movies', '19': 'Travel & Events', '20': 'Gaming', '21': 'Videoblogging', '22': 'People & Blogs', '23': 'Comedy', '24': 'Entertainment', '25': 'News & Politics', '26': 'Howto & Style', '27': 'Education', '28': 'Science & Technology', '30': 'Movies', '31': 'Anime/Animation', '32': 'Action/Adventure', '33': 'Classics', '34': 'Comedy', '35': 'Documentary', '36': 'Drama', '37': 'Family', '38': 'Foreign', '39': 'Horror', '40': 'Sci-Fi/Fantasy', '41': 'Thriller', '42': 'Shorts', '43': 'Shows', '44': 'Trailers'}

payload={}
headers = {
      'authority': 'content-youtube.googleapis.com',
      'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="90", "Google Chrome";v="90"',
      'x-goog-encode-response-if-executable': 'base64',
      'x-origin': 'https://explorer.apis.google.com',
      'sec-ch-ua-mobile': '?0',
      'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36',
      'x-requested-with': 'XMLHttpRequest',
      'x-javascript-user-agent': 'apix/3.0.0 google-api-javascript-client/1.1.0',
      'x-referer': 'https://explorer.apis.google.com',
      'accept': '*/*',
      'sec-fetch-site': 'same-origin',
      'sec-fetch-mode': 'cors',
      'sec-fetch-dest': 'empty'
    }
country_codes = ['EG','SA','AE']
nextPageToken = ''
for countrycode in country_codes:
    url = "https://content-youtube.googleapis.com/youtube/v3/videos?part=contentDetails&part=snippet&part=statistics&part=topicDetails&part=id&part=player&chart=mostPopular&regionCode=" + countrycode + "&pageToken=" + nextPageToken + "&maxResults=50&key=AIzaSyAa8yy0GdcGPHdtD083HiGGx_S0vMPScDM"
    #url = "https://content-youtube.googleapis.com/youtube/v3/videos?part=contentDetails&part=snippet&part=statistics&part=topicDetails&part=id&part=player&chart=mostPopular&regionCode="+countrycode+"&maxResults=50&key=AIzaSyAa8yy0GdcGPHdtD083HiGGx_S0vMPScDM"
    response = requests.get(url, headers=headers, data=payload)
    data = response.json()
    totalResults = data['pageInfo']['totalResults']
    nextPageToken = data['nextPageToken']
    pages = math.ceil(totalResults/50)-1
    for page in range(pages):
        for i in range(len(data['items'])):
            publishedAt = datetime.datetime.strptime(data['items'][i]['snippet']['publishedAt'],"%Y-%m-%dT%H:%M:%S%z").timestamp()
            id = data['items'][i]['id']
            YT_id = data['items'][i]['snippet']['channelId']
            title = data['items'][i]['snippet']['title']
            channelTitle = data['items'][i]['snippet']['channelTitle']
            categoryId = listdict[data['items'][i]['snippet']['categoryId']]
            video_duration = isodate.parse_duration(data['items'][i]['contentDetails']['duration']).total_seconds()
            licensedContent = data['items'][i]['contentDetails']['licensedContent']
            viewCount = data['items'][i]['statistics']['viewCount']
            likeCount = data['items'][i]['statistics']['likeCount']
            dislikeCount = data['items'][i]['statistics']['dislikeCount']
            favoriteCount = data['items'][i]['statistics']['favoriteCount']
            commentCount = data['items'][i]['statistics']['commentCount']
            category_details = []
            try: #category_details
                for a in range(len(data['items'][i]['topicDetails']['topicCategories'])):
                    category = data['items'][i]['topicDetails']['topicCategories'][a].replace('https://en.wikipedia.org/wiki/','')
                    category_details.append(category)
            except KeyError:
                category_details = []
            row = countrycode,id,title,channelTitle,YT_id,categoryId,category_details,publishedAt,viewCount,likeCount,dislikeCount,favoriteCount,commentCount,video_duration,licensedContent
            with open(r'yt_trending_vids.csv', 'a', newline='',
                      encoding="utf-8") as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(row)
