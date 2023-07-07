import os
# from google_auth_oauthlib.flow import InstalledAppFlow
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors

from googleapiclient.http import MediaFileUpload

scopes = ["https://www.googleapis.com/auth/youtube.upload"]

class YoutubeController:

    def __init__(self, client_secrets_file: str = "client_secret.json", api_service_name: str = "youtube", api_version: str = "v3" ) -> None:
        self.api_service_name = api_service_name
        self.api_version = api_version
        self.client_secrets_file = client_secrets_file

    def upload_video(self, video_path: str, title: str = "Default title", description: str = "Default description", tags: list[str] = []):

        os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

        # Get credentials and create an API client

        flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
            self.client_secrets_file, scopes)
        
        credentials = flow.run_local_server()

        youtube = googleapiclient.discovery.build(
            self.api_service_name, self.api_version, credentials=credentials)

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
        print("Upload succesfull!")

if __name__ == "__main__":
    youtube = YoutubeController()
    youtube.upload_video("./results/result1.mp4")