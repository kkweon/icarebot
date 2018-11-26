# icarebot
[![Build Status](https://travis-ci.com/kkweon/icarebot.svg?branch=master)](https://travis-ci.com/kkweon/icarebot)

Reddit icarebot

## Requirements

- python 3.6

## Run

- Copy [praw.ini.template](./praw.ini.template) and rename to praw.ini
- Fill out the following section
    ```
    client_id = yourclientbotid
    client_secret = yourclientbotsecret
    username = username
    password = password
    ```
- Run
    ```
    python3 icarebot/main.py
    ```

    or

    ```
    docker build -t icarebot .
    docker-compose up -d
    ```
