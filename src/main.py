import requests
import csv
from bs4 import BeautifulSoup

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
def get_followers_chunk(offset, url):
    querystring = {"offset":offset,"limit":"200","client_id":"RfoqFLXghO6UuFNArI1Ksd17qWClDBFt","app_version":"1660231961","app_locale":"en"}
    response = requests.request("GET", url, data=payload, headers=headers, params=querystring)
    
    return response.json() # returns a dictionary with keys 'collection' (list of followers) and 'next_href' (next batch of followers)
    
# writes csv file with all followers' info
def write_csv(all_followers):
    follower_info = ['followers_count', 'id', 'permalink_url', 'username']
    
    with open('followers.csv', 'w', encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames = follower_info)
        writer.writeheader()
        writer.writerows(all_followers)
    
# gets rid of unnecessary info in the dictionaries
def consolidate_dicts(all_followers):
    for i in range(len(all_followers)):
        all_followers[i].pop('created_at')
        all_followers[i].pop('city')
        all_followers[i].pop('last_name')
        all_followers[i].pop('avatar_url')
        all_followers[i].pop('comments_count')
        all_followers[i].pop('country_code')
        all_followers[i].pop('creator_subscriptions')
        all_followers[i].pop('creator_subscription')
        all_followers[i].pop('description')
        all_followers[i].pop('followings_count')
        all_followers[i].pop('first_name')
        all_followers[i].pop('full_name')
        all_followers[i].pop('groups_count')
        all_followers[i].pop('kind')
        all_followers[i].pop('last_modified')
        all_followers[i].pop('likes_count')
        all_followers[i].pop('playlist_likes_count')
        all_followers[i].pop('permalink')
        all_followers[i].pop('playlist_count')
        all_followers[i].pop('reposts_count')
        all_followers[i].pop('track_count')
        all_followers[i].pop('uri')
        all_followers[i].pop('urn')
        all_followers[i].pop('verified')
        all_followers[i].pop('visuals')
        all_followers[i].pop('badges')
        all_followers[i].pop('station_urn')
        all_followers[i].pop('station_permalink')


def get_api_url(account_url):
    page_source = requests.get(account_url, 'html.parser').text
    soup = BeautifulSoup(page_source)
    
    user_id = soup.find('meta', {'property':'twitter:app:url:googleplay'})['content'].split(':')[2] #.find('a', {'class':'sc-button-startstation sc-button-secondary sc-button sc-button-medium sc-button-responsive'})['href']
    
    return f"https://api-v2.soundcloud.com/users/{user_id}/followers"


def main():
    all_followers = []
    offset = 0
        
    account_url = input('Give a SoundCloud account URL: ')
    api_url = get_api_url(account_url)
    
    while True:
        print('offset: ' + str(offset))
        followers_chunk = get_followers_chunk(offset, api_url)
        all_followers += followers_chunk['collection']
        try:
            offset = followers_chunk['next_href'].split('?')[1].split('=')[1].split('&')[0]
        except AttributeError: # an AttributeError here would imply that no offset was found, meaning we've found every follower
            break
    
    
    consolidate_dicts(all_followers)
    print(all_followers[0])
    write_csv(all_followers)
    

if __name__ == '__main__':
    main()
    