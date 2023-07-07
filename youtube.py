import os
from google_auth_oauthlib.flow import InstalledAppFlow
import googleapiclient.discovery
import googleapiclient.errors

from googleapiclient.http import MediaFileUpload

from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request

class YoutubeController:

    def __init__(self, client_secrets_file: str = "client_secret.json", api_service_name: str = "youtube", api_version: str = "v3" ) -> None:
        self.api_service_name = api_service_name
        self.api_version = api_version
        self.client_secrets_file = client_secrets_file
        self.scopes = ["https://www.googleapis.com/auth/youtube.upload"]

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


    def upload_video(self, video_path: str, title: str = "Default title", description: str = "Default description", tags: list[str] = []) -> None:

        os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
        
        credentials = self.get_credentials()

        youtube = googleapiclient.discovery.build(self.api_service_name, self.api_version, credentials=credentials)

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
        print("Uploaded succesfully!")

if __name__ == "__main__":
    youtube = YoutubeController()
    youtube.upload_video("./results/result1.mp4")