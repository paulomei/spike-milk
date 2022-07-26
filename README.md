# Readme

Code challenge for Spike/AAG's selection process.

The objective is to take a [predictive model](https://github.com/SpikeLab-CL/ml-engineer-challenge/blob/main/data_scientist_past_challenge/data_scientist_challenge_answers.ipynb) into a production environment.

In this project are included: Python 3 virual environment, Dockerfile to build the image of a Flask app server and the codes.

In order to activate and deactivate the virtual enviroment (in case you need to edit) run the commands:
```
source activate

deactivate
```

To build, check and run the docker image run:
```
docker build -t spike-milk .

docker images

docker run -it -p 5000:5000 spike-milk
```

Once the image is running you can send REST requests using a script folowing the **client.py** template or a 3rd party REST client like [Postman](https://www.postman.com/product/rest-client)

For more details, please refer to the docs folder or the [shared version](https://few-tree-fdd.notion.site/spike-milk-User-and-developer-guide-d811d9e96bcb4c0695ebaae7231da891) in notion.so.
