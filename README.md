# Telegram bot parses channel's name and tag

![Bot Preview](https://s12.gifyu.com/images/SW4V9.gif)

## How to Run

### Python

```
pip install -r requirements.txt
```

```
API_ID=00000000 \
API_HASH=aaaaaaaaaaaaaaaa0000000000000000 \
SOURCE_CHANNEL_ID=-1009999999999 \
DESTINATION_CHANNEL_ID=-1008888888888 \
python main.py
```

### Docker

```
docker build -t bot .
```

```
docker run -d -e \
                 API_ID=00000000 \
                 API_HASH=aaaaaaaaaaaaaaaa0000000000000000 \
                 SOURCE_CHANNEL_ID=-1009999999999 \
                 DESTINATION_CHANNEL_ID=-1008888888888 \
                 bot
```
