## NER
Internally `ner_server.sh` will listen on `127.0.0.1:8011`.
The stanford NER change will try to connect to `127.0.0.1:80/word_embeddings/ws/wordvectors_get.php?w1=`.
This in turn will try to connect to `127.0.0.1:8001/wordvectors_get?` => this is a fasttext-mod server.

## IATE-EUROVOC
IATE-EUROVOC will listen on `9001`.
A nice guide for apache+php on Ubuntu base image: [https://writing.pupius.co.uk/apache-and-php-on-docker-44faef716150](https://writing.pupius.co.uk/apache-and-php-on-docker-44faef716150).

## NLPipe
NLPipe is running at `http://127.0.0.1:5000`. It starts with `/root/nlpipe/start-ws.sh` and stops with `/root/nlpipe/stop-ws.sh`.
Log of the web service can be found in the `/root/nlpipe/ws.log` file.
To check the NLPipe installation, after building and starting the Docker image, run `run_nlpipe_tests.sh` script.

## Docker
In order to build a fresh image, do the following steps:
1. `stop.sh`
2. `build.sh` -- check for building errors during the build
3. `start.sh` -- wait approx. 1 minute for the container to start

If you need to do multiple builds, it may be necessary to free up space by running `docker system prune` as `root`.
If you need a `/bin/bash` shell into the newly built and started container, run `run_shell.sh`.
