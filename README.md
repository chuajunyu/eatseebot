# EatseeBot

Eatsee is a social meetup telegram bot which matches users with other nearby users with similar food preferences, and
offers food recommendations to them.

This repository stores the front-end, the backend is stored in [this repo](https://github.com/chuajunyu/eatsee_db)

## Features / Tech Stack

- Telegram Bot built with Python-Telegram-Bot module which wraps the Telegram API
- Allows real time matching and chatting with other users
- Recommends food for users

## Set-up instructions

1. The frontend requires the [backend repo](https://github.com/chuajunyu/eatsee_db) to be set up to work

Follow the set up instructions in that repo before proceeding.

2. Set up your venv
```
python -m venv venv
venv\scripts\activate
pip install -r requirements.txt
```

3. Fill up the configuration values in `config.config`

```
API_ip = YOUR_BACKEND_API_IP
telegram_key = YOUR_TELEGRAM_BOT_KEY
```

4. run `py main.py`

