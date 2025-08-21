# DockerVerse
Telegram bot to manage docker containers.


## Features
- START, STOP or RESTART containers through bot.
- Get real-time updates when a container starts, stops, restarts, or gets destroyed.
- Retrive logs by time and number of lines.
- Allow multiple users to manage.
- Can be executed locally or on a server with same minimal config.


## Pre-requisites
- Docker
- Telegram account


## Environment Variables

**Required:**
- `TELEGRAM_API_ID`: The api_id obtained after creating application at [my.telegram.org](https://my.telegram.org/apps).
- `TELEGRAM_API_HASH`: The api_hash obtained after creating application at [my.telegram.org](https://my.telegram.org/apps).
- `TELEGRAM_BOT_TOKEN`: The bot api token. Send message `/newbot` to [@BotFather](https://t.me/BotFather) in telegram to create a bot.
- `AUTHORIZED_USER_IDS`: Telegram account ids of authorized users. Send a message to [@userinfobot](https://t.me/userinfobot) to get id.

**Optional:**
- `PROTECTED_CONTAINER_IDS`: Ids of containers to protect.
- `ALLOWED_CONTAINER_IDS`: Ids of containers allowed to access.
- `CONTAINER_IDS_TO_IGNORE`: Ids of containers to ignore. Have no effect if `ALLOWED_CONTAINER_IDS` is specified.
