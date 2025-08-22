# DockerVerse
Telegram bot to manage docker containers.


## Features
- START, STOP or RESTART containers through bot.
- Get real-time updates when a container starts, stops, restarts, or gets destroyed.
- Retrive logs by time and number of lines.
- Allow multiple users to manage.
- Can be executed locally or on a server with same minimal config.
- Keeps track of Docker events and user actions in `event.log` file.


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


## Setup
1. Clone this repository and navigate to the project directory.
```bash
git clone https://github.com/manu-ox/DockerVerse.git && cd DockerVerse
```
2. Copy file `.env-sample` to `.env`
```bash
cp .env-sample .env
```
3. Edit the `.env` file, fill the environment variables and save the file.
```bash
nano .env
```
4. Try running the application using `docker-compose`.
```bash
docker-compose up --build
```
5. Run the application in detached mode.
```bash
docker-compose up -d
```


## Credits
- [docker-py](https://github.com/docker/docker-py)
- [pyrogram](https://github.com/TelegramPlayground/pyrogram)

<br>

[![](https://xstats.xoid.me/stats/manu-ox/DockerVerse)](https://stats.xoid.me/stats/manu-ox/DockerVerse)
