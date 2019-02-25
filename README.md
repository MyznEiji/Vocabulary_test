# Vocabulary_test
for English Life


## Installation

$ git clone git@github.com:MyznEiji/Vocabulary_test.git


## Set enviroment
$ docker run -it --name vocabulary_test -v /Users/miyazonoeiji/projects/python/vocabulary_test/:/root/vocabulary_test frolvlad/alpine-python3

## How to run
$ docker container start vocabulary_test && docker exec -it vocabulary_test python3 /root/vocabulary_test/main.py && docker container stop vocabulary_test
