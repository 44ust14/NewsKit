# newschatbot
1) Install doker --> https://docs.docker.com/install/#supported-platforms
2) Install doker-compose --> https://docs.docker.com/compose/install/
3) Git clone repo from Git Hub
4) cd newskit

-- Launch via docker-compose --

5) sudo docker-compose up


-- Launch via Dockerfile напряму (not recommended) --

5) docker build -t python ./
6) sudo docker run -p 8000:8000 -v `pwd`:/newskit --rm -it python python app.py



To pull docker repository(image) from Docker Hub --> docker pull dmytrolopushanskyy/newskit::firstpush
