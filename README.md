# [NewsKit](t.me/newskit_bot)

Bot for getting the most relevant news content

t.me/newskit_bot

## Getting Started

To launch this application with Docker:

1) Install doker --> https://docs.docker.com/install/#supported-platforms
2) Install doker-compose --> https://docs.docker.com/compose/install/

### Prerequisites

3) Clone this repository and go to root folder

```
git clone https://github.com/emloft/NewsKit.git
cd newskit
```

## Launch via docker-compose

```
sudo docker-compose up
```

## Direct launch via Dockerfile (not recommended)

```
docker build -t python ./
```
And then run:
```
sudo docker run -p 8000:8000 -v `pwd`:/newskit --rm -it python python app.py
```

## Authors

We are open to new opportunities so feel free to get in touch with us!

* [Dmytro Lopushanskyy](https://www.facebook.com/profile.php?id=100007359646680) - Front-End & Back-End Developer
* [Mark Lastovski](https://www.facebook.com/mlastovski) - Game-Dev & Back-End Developer





