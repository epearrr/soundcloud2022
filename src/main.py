import requests
import csv

url = "https://api-v2.soundcloud.com/users/234468714/followers"

payload = ""
headers = {
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "Accept-Language": "en-US,en;q=0.9",
    "Authorization": "OAuth 2-293430-234468714-lzXrYdwUACsnYD",
    "Connection": "keep-alive",
    "Origin": "https://soundcloud.com",
    "Referer": "https://soundcloud.com/",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-site",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36",
    "sec-ch-ua": "^\^.Not/A",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "^\^Windows^^"
}

# gets next 200 followers (200 is seemingly the highest allowed by soundcloud's api)
def get_followers_chunk(offset=0):
    querystring = {"offset":offset,"limit":"200","client_id":"RfoqFLXghO6UuFNArI1Ksd17qWClDBFt","app_version":"1660231961","app_locale":"en"}
    response = requests.request("GET", url, data=payload, headers=headers, params=querystring)
    
    return response.json() # returns a dictionary with keys 'collection' (list of followers) and 'next_href' (next batch of followers)
    
# writes csv file with all followers' info
def write_csv(all_followers):
    follower_info = ['avatar_url', 'city', 'comments_count', 'country_code', 'created_at', 'creator_subscriptions',
                     'creator_subscription', 'description', 'followers_count', 'followings_count', 'first_name',
                     'full_name', 'groups_count', 'id', 'kind', 'last_modified', 'last_name', 'likes_count',
                     'playlist_likes_count', 'permalink', 'permalink_url', 'playlist_count', 'reposts_count',
                     'track_count', 'uri', 'urn', 'username', 'verified', 'visuals', 'badges', 'station_urn',
                     'station_permalink']
    
    with open('followers.csv', 'w', encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames = follower_info)
        writer.writeheader()
        writer.writerows(all_followers)
    

def main():
    all_followers = []
    offset = 0
        
    while True:
        print('offset: ' + str(offset))
        followers_chunk = get_followers_chunk(offset)
        all_followers += followers_chunk['collection']
        try:
            offset = followers_chunk['next_href'].split('?')[1].split('=')[1].split('&')[0]
        except AttributeError: # an AttributeError here would imply that no offset was found, meaning we've found every follower
            break
    
    write_csv(all_followers)
    

if __name__ == '__main__':
    main()
    