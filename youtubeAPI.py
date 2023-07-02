import googleapiclient.discovery
import googleapiclient.errors
import requests
import isodate
import mongoDB

from config import API_KEY

def fetchYtDetails(custURL):

    api_service_name = "youtube"
    api_version = "v3"

    # Use your API_KEY here
    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, developerKey=API_KEY)

    # Used HTTP request method to find channel id, since right now we can't find channel Id by youtube api functions.
    try:
        parsingYtDetails(custURL, youtube)
    except Exception as error:
        return f'Error : {error}'

    youtube.close()


def parsingYtDetails(custURL, youtube):
    channel_Id = requests.get(
        f'https://www.googleapis.com/youtube/v3/search?part=id&q={custURL}&type=channel&key={API_KEY}').json()['items'][0]['id']['channelId']

    # Channel Details
    channelResp = youtube.channels().list(
        id=channel_Id, part='snippet, statistics').execute()

    # * Added channel details
    finalResp = {
        'Channel_Name': {
            'Channel_Id': channelResp['items'][0]['id'],
            'Custom_URL': custURL,
            'Channel_Name': channelResp['items'][0]['snippet']['title'],
            'Video_Count' : int(channelResp['items'][0]['statistics']['videoCount']),
            'Subscription_Count': int(channelResp['items'][0]['statistics']['subscriberCount']),
            'Channel_Views': int(channelResp['items'][0]['statistics']['viewCount']),
            'Channel_Description': channelResp['items'][0]['snippet']['description'],
            'Thumbnail': channelResp['items'][0]['snippet']['thumbnails']['default']['url'],
            'Playlists': {},
        }
    }

    # Playlist Details
    playlistResp = youtube.playlists().list(
        part='snippet',
        channelId=channel_Id,
        maxResults=2
    ).execute()

    for playlistRespIndex, playlistRespItems in enumerate(playlistResp['items']):
        playlist_Id = playlistRespItems['id']

        # * Added playlist details
        finalResp['Channel_Name']['Playlists'] |= {
            f'Playlist_Id_{playlistRespIndex}': {
                'Playlist_Id': playlist_Id,
                'Playlist_Title': playlistRespItems['snippet']['title'],
                'Videos': {}
            }
        }

        # Getting Video Id's
        playlistItemsResp = youtube.playlistItems().list(
            part='snippet',
            playlistId=playlist_Id,
            maxResults=2
        ).execute()

        # Video Id's in list
        videoIdList = [
            playlistItemsRespItems['snippet']['resourceId']['videoId']
            for playlistItemsRespItems in playlistItemsResp['items']
        ]
        for videoIdItems in videoIdList:

            # Video details
            videoResp = youtube.videos().list(
                part="snippet, contentDetails, statistics",
                id=videoIdItems
            ).execute()

            # * Added Video details
            for videoRespIndex, videoRespItems in enumerate(videoResp['items']):
                video_Id = videoRespItems['id']
                finalResp['Channel_Name']['Playlists'][f'Playlist_Id_{playlistRespIndex}']['Videos'] |= {
                    f'Video_Id_{videoRespIndex}': {
                        'Video_Id': video_Id,
                        'Video_Name': videoRespItems['snippet']['title'],
                        'Video_Description': videoRespItems['snippet']['description'],
                        'PublishedAt': str(isodate.parse_date(videoRespItems['snippet']['publishedAt'])),
                        'View_Count': int(videoRespItems['statistics']['viewCount']),
                        'Like_Count': int(videoRespItems['statistics']['likeCount']),
                        'Favorite_Count': int(videoRespItems['statistics']['favoriteCount']),
                        'Comment_Count': int(videoRespItems['statistics']['commentCount']),
                        'Duration': str(isodate.parse_duration(videoRespItems['contentDetails']['duration'])),
                        'Thumbnail': videoRespItems['snippet']['thumbnails']['default']['url'],
                        'Comments': {}
                    }
                }

                # Comment details
                commentsResp = youtube.commentThreads().list(
                    part='snippet',
                    videoId=videoIdItems,
                    maxResults=2
                ).execute()

                # * Added comment details
                for commentRespIndex, commentRespItems in enumerate(commentsResp['items']):
                    comment_Id = commentRespItems['id']
                    finalResp['Channel_Name']['Playlists'][f'Playlist_Id_{playlistRespIndex}']['Videos'][f'Video_Id_{videoRespIndex}']['Comments'] |= {
                        f'Comment_Id_{commentRespIndex}': {
                            'Comment_Id': comment_Id,
                            'Comment_Text': commentRespItems['snippet']['topLevelComment']['snippet']['textDisplay'],
                            'Comment_Author': commentRespItems['snippet']['topLevelComment']['snippet']['authorDisplayName'],
                            'Comment_PublishedAt': str(isodate.parse_date(commentRespItems['snippet']['topLevelComment']['snippet']['publishedAt']))
                        }
                    }

    mongoDB.mongoAdd(jsonResponse=finalResp)
