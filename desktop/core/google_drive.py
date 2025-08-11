from __future__ import print_function
import os
import pickle
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# =========================
# CONFIGURATION
# =========================
SCOPES = ['https://www.googleapis.com/auth/drive.file']
CREDENTIALS_FILE = 'client_secret_500301562304-vlqnr6eqvel0mqudieadrb3rs9mv709n.apps.googleusercontent.com.json'  # OAuth credentials you downloaded
FOLDER_ID = '1XDJeaTDhmbxejG6AC71ddKYEuTizRSag'  # Target folder ID
LOCAL_FOLDER = r'C:\Users\athar\OneDrive\Desktop\Atharva\Lata-Mangeshkar\fingerprint\desktop\data'  # Local folder to upload
# =========================

def get_service():
    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_FILE, SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
    return build('drive', 'v3', credentials=creds)

def upload_to_drive(file_path, service):
    file_name = os.path.basename(file_path)
    file_metadata = {'name': file_name, 'parents': [FOLDER_ID]}
    media = MediaFileUpload(file_path, resumable=True)
    uploaded = service.files().create(
        body=file_metadata, media_body=media, fields='id'
    ).execute()
    file_id = uploaded.get('id')

    # Make file public
    service.permissions().create(
        fileId=file_id,
        body={"role": "reader", "type": "anyone"}
    ).execute()

    print(f"✅ Uploaded: {file_name}")
    print(f"   Public link: https://drive.google.com/file/d/{file_id}/view")

def upload_folder(local_folder, service):
    for fname in os.listdir(local_folder):
        fpath = os.path.join(local_folder, fname)
        if os.path.isfile(fpath):
            upload_to_drive(fpath, service)

if __name__ == '__main__':
    service = get_service()
    upload_folder(LOCAL_FOLDER, service)
