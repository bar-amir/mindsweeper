<p align="center">
  <img alt="Mindsweeper" title="Mindsweeper" src="https://user-images.githubusercontent.com/28039736/82994340-a5ccc900-a00a-11ea-8f43-99d5f91ac532.jpg" />
</p>
<h3 align="center">
  Mindsweeper
</h3>
<p align="center">
  <a target="_blank" title="Build Status" href="https://travis-ci.com/bar-amir/mindsweeper"><img src="https://travis-ci.com/bar-amir/mindsweeper.svg?branch=master"></a>
  <a target="_blank" title="Codecov" href="https://codecov.io/gh/bar-amir/mindsweeper"><img src="https://codecov.io/gh/bar-amir/mindsweeper/branch/master/graph/badge.svg"></a>
  <a target="_blank" title="Documentation Status" href="https://mindsweeper.readthedocs.io/en/latest/?badge=latest"><img src="https://readthedocs.org/projects/mindsweeper/badge/?version=latest"></a>
</p>

## About
## Prerequisites
```
Docker v19.03.6
docker-compose v1.25.5
Node v12.16.3
npm v16.14.5
Python v3.8
```

## Installation

Clone the repository and enter the project's root folder:
```bash
$ git clone https://github.com/bar-amir/mindsweeper.git
...
$ cd mindsweeper
```

Grant execution permissions to all scripts:
```bash
$ chmod a=rx -R scripts 
```

Run install.sh:
```bash
$ scripts/install.sh
```
This script will:
* Create a virtual enviroment
* Update pip and install dependencies
* Update npm and install dependencies
* Compile .proto files

Activate virtual enviroment:
```bash
$ source .env/bin/activate
```

## Running locally

### With Docker
Run run-pipeline.sh
```bash
$ scripts/run-pipeline.sh
```
This script will:
* Configure the GUI for running in a container
* Build and run all the services with Docker Compose

### Locally


Now you can start any of the services using Python API or the CLI and upload a raw file to the server.

## Sample File
Download sample.mind.gz from here. [reupload to GCP]
from mindsweeper root folder, run
upload-sample path_to_sample/sample.mind.gz
