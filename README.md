A telegram bot to collect information about web3 companies and investors, the goal is that users can 
 access the bot and send data about companies or investors to be collected in a google spreadsheet.

# Setup

1. Clone this repository and move to project base directory.
2. Run poetry install. (NOTE: Poetry is required to install package)
3. Add `credential.json` file in base directory from google API console. (Please activate google sheet and google drive services first).

__NOTE :__ Add `http://localhost:8000` as redirect url.

__Demo credential.json file__

```json
{
    "installed": {
        "client_id": "xyz.apps.googleusercontent.com",
        "project_id": "xyz",
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://oauth2.googleapis.com/token",
        "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
        "client_secret": "xyz",
        "redirect_uris": ["http://localhost"]
    }
}
```

4. Add `TELEGRAM_TOKEN` in `.env` obtained from `bot father`. Search `bot father` in telegram and send `/start` create app and get token for it.

5. To start app run

```bash
poetry shell # to activate environment
python main.py
```

6. Now search your telegram bot in telegram and send `/start` to start conversations.

# Demo link

__https://youtu.be/wDBV2j5ujpY__

# Features

- Can add data for `companies` and `investors` on seperate worksheet in same google spread sheet.
- Can handle mutiple user at same time without any race condition.
- Data is fetched on application startup to reduce latency.

## What other feature can be implemented?

- Data can be stored in redis to support mutiple process at same time to handle millions of request at same time.
- Data can be pushed in chunks and made lazy to give realtime experience to user.
