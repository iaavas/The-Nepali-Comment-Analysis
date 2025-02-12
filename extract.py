from googleapiclient.discovery import build
from datetime import datetime
import pandas as pd
import os


def get_channel_videos(api_key, channel_id):
    """
    Fetch video information from a YouTube channel

    Parameters:
    api_key (str): Your YouTube Data API key
    channel_id (str): The channel ID to scrape

    Returns:
    pandas.DataFrame: DataFrame containing video information
    """
    # Create YouTube API client
    youtube = build('youtube', 'v3', developerKey=api_key)

    videos = []
    next_page_token = None

    while True:
        # Get channel's uploads
        request = youtube.search().list(
            part='snippet',
            channelId=channel_id,
            maxResults=50,
            order='date',
            pageToken=next_page_token,
            type='video'
        )
        response = request.execute()

        # Get video IDs
        video_ids = [item['id']['videoId'] for item in response['items']]

        # Get detailed video information
        video_request = youtube.videos().list(
            part='snippet,statistics',
            id=','.join(video_ids)
        )
        video_response = video_request.execute()

        # Extract relevant information
        for video in video_response['items']:
            video_data = {
                'Title': video['snippet']['title'],
                'Views': int(video['statistics'].get('viewCount', 0)),
                'Upload_Date': datetime.strptime(
                    video['snippet']['publishedAt'],
                    '%Y-%m-%dT%H:%M:%SZ'
                ).strftime('%Y-%m-%d'),
                'Likes': int(video['statistics'].get('likeCount', 0)),
                'Comments': int(video['statistics'].get('commentCount', 0)),
                'Description': video['snippet']['description']
            }
            videos.append(video_data)

        # Check if there are more pages
        next_page_token = response.get('nextPageToken')
        if not next_page_token:
            break

    # Convert to DataFrame
    df = pd.DataFrame(videos)
    return df


def main():
    # Replace with your API key and channel ID
    API_KEY = 'YOUR_API_KEY'
    CHANNEL_ID = 'CHANNEL_ID'

    # Get video data
    df = get_channel_videos(API_KEY, CHANNEL_ID)

    # Save to CSV
    df.to_csv('youtube_channel_data.csv', index=False)
    print(f"Data saved to youtube_channel_data.csv")

    # Display first few rows
    print("\nFirst few rows of the data:")
    print(df.head())


if __name__ == "__main__":
    main()
