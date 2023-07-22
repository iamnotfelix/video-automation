import os
from google_auth_oauthlib.flow import InstalledAppFlow
import googleapiclient.discovery
import googleapiclient.errors

from googleapiclient.http import MediaFileUpload

from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request

class YoutubeController:
    """ YoutubeController class provides communication with the YouTubeApi. """

    def __init__(self, client_secrets_file: str = "client_secret.json", api_service_name: str = "youtube", api_version: str = "v3" ) -> None:
        self.api_service_name = api_service_name
        self.api_version = api_version
        self.client_secrets_file = client_secrets_file
        self.scopes = ["https://www.googleapis.com/auth/youtube.upload", 
                       "https://www.googleapis.com/auth/youtube.readonly"]

    def get_credentials(self):
        credentials = None
        # The file token.json stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists("token.json"):
            credentials = Credentials.from_authorized_user_file("token.json", self.scopes)
        # If there are no (valid) credentials available, let the user log in.
        if not credentials or not credentials.valid:
            if credentials and credentials.expired and credentials.refresh_token:
                credentials.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(self.client_secrets_file, self.scopes)
                credentials = flow.run_local_server()
            # Save the credentials for the next run
            with open("token.json", 'w') as token:
                token.write(credentials.to_json())
        
        return credentials

    def upload_video(self, video_path: str, thumbnail_path: str, title: str = "Default title", description: str = "Default description", tags: list[str] = []) -> str:

        os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
        
        credentials = self.get_credentials()

        youtube = googleapiclient.discovery.build(self.api_service_name, self.api_version, credentials=credentials)

        # Uploading video
        request = youtube.videos().insert(
            part="snippet,status",
            body={
                "snippet": {
                    "categoryId": "23",
                    "title": title,
                    "description": description,
                    "tags": tags
                },
                "status": {
                    "privacyStatus": "public",
                    'selfDeclaredMadeForKids': False
                }
            },
            media_body=MediaFileUpload(video_path)
        )
        response = request.execute()

        print(response)

        video_id = response['id']
        self.set_thumbnail(video_id, thumbnail_path)        

        print("Uploaded succesfully!")

        return video_id

    def get_video_ids(self, channel_id: str) -> list[str]:
        os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
        
        credentials = self.get_credentials()

        youtube = googleapiclient.discovery.build(self.api_service_name, self.api_version, credentials=credentials)

        # Get info about channel
        request = youtube.channels().list(
            part = "contentDetails",
            id = channel_id
        )
        
        response = request.execute()
        
        # Get the id of the uploads playlist
        uploads_id = response['items'][0]['contentDetails']['relatedPlaylists']['uploads']

        # Get the first page of videos
        request = youtube.playlistItems().list(
            part = "snippet",
            playlistId = uploads_id,
            maxResults = 50
        )
        response = request.execute()

        # Store video ids from the first call
        video_ids = [item['snippet']['resourceId']['videoId'] for item in response['items']]
        
        # Repeat process for next pages
        while "nextPageToken" in response:
            nextPageToken = response["nextPageToken"]
            request = youtube.playlistItems().list(
                part = "snippet",
                pageToken = nextPageToken,
                playlistId = uploads_id,
                maxResults = 50
            )

            response = request.execute()
            video_ids.extend([item['snippet']['resourceId']['videoId'] for item in response['items']])

        return video_ids
    
    def get_video_titles(self, channel_id: str) -> list[str]:
        os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
        
        credentials = self.get_credentials()

        youtube = googleapiclient.discovery.build(self.api_service_name, self.api_version, credentials=credentials)

        # Get info about channel
        request = youtube.channels().list(
            part = "contentDetails",
            id = channel_id
        )
        
        response = request.execute()
        
        # Get the id of the uploads playlist
        uploads_id = response['items'][0]['contentDetails']['relatedPlaylists']['uploads']

        # Get the first page of videos
        request = youtube.playlistItems().list(
            part = "snippet",
            playlistId = uploads_id,
            maxResults = 50
        )
        response = request.execute()

        # Store titles from the first call
        titles = [item['snippet']['title'] for item in response['items']]
        
        # Repeat process for next pages
        while "nextPageToken" in response:
            nextPageToken = response["nextPageToken"]
            request = youtube.playlistItems().list(
                part = "snippet",
                pageToken = nextPageToken,
                playlistId = uploads_id,
                maxResults = 50
            )

            response = request.execute()
            titles.extend([item['snippet']['title'] for item in response['items']])

        return titles
    
    def set_thumbnail(self, video_id: str, file_path: str) -> None:
        os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
        
        credentials = self.get_credentials()

        youtube = googleapiclient.discovery.build(self.api_service_name, self.api_version, credentials=credentials)

        # Setting the thumbnail
        request = youtube.thumbnails().set(
            videoId = video_id,
            media_body = MediaFileUpload(file_path)
        )
        response = request.execute()

        print(response)



if __name__ == "__main__":
    youtube = YoutubeController()
    # youtube.upload_video("./results/result1.mp4")
    # print(youtube.get_video_titles("UCJlxrVg_KbrVJIR3zoUlWxQ"))
    # youtube.set_thumbnail("iWqBq-ED62Y", "./thumbnails/fd8b41e8-f473-47bf-b41f-e52ce2fd21ae.jpeg")