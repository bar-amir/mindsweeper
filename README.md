<p align="center">
  <img alt="Mindsweeper" title="Mindsweeper" src="https://user-images.githubusercontent.com/28039736/82994340-a5ccc900-a00a-11ea-8f43-99d5f91ac532.jpg" />
</p>
<h3 align="center">
  Mindsweeper
</h3>
<p align="center">
  <a title="Build Status" href="https://travis-ci.com/bar-amir/mindsweeper"><img src="https://travis-ci.com/bar-amir/mindsweeper.svg?branch=master"></a>
  <a title="Codecov" href="https://codecov.io/gh/bar-amir/mindsweeper"><img src="https://codecov.io/gh/bar-amir/mindsweeper/branch/master/graph/badge.svg"></a>
  <a title="Documentation Status" href="https://mindsweeper.readthedocs.io/en/latest/?badge=latest"><img src="https://readthedocs.org/projects/mindsweeper/badge/?version=latest"></a>
</p>

![mindsweeper](https://user-images.githubusercontent.com/28039736/90511423-19dbc080-e165-11ea-9a5a-ff0267b9de35.gif)

## About
Final project submission for the course "Advanced Systems Design". (Tel Aviv University, 2020)

The project experiments with several technologies and concepts:
1. Client-server: Uploading large files, handling multiple connections parallely (Flask, Protocol Buffers)
2. Microservices architecture: Parsing messages containing different types of data and saving them to a database (RabbitMQ, MongoDB) 
3. RESTful API: Exposing the saved data, and consuming it by a CLI and a GUI (Click, React)
4. Built a framework for adding support for new file formats and parsers.
5. Easy deployment, CI/CD, testing and documentation (Docker, TravisCI, Codecov, pytest, Sphinx, Read the Docs)

Documentation is available [here](https://mindsweeper.readthedocs.io/).

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

Grant execution permission to all scripts under the `scripts` folder:
```bash
$ chmod a=rwx -R scripts 
```

Run `install.sh`:
```bash
$ scripts/install.sh
```
This script will:
* Create a virtual enviroment
* Update pip and install dependencies
* Update npm and install dependencies
* Compile `.proto` files to modules

Activate the virtual enviroment:
```bash
$ source .env/bin/activate
```

## Running with Docker
Run `run-pipeline.sh`
```bash
$ scripts/run-pipeline.sh
```
This script will:
* Configure the GUI for running in a container
* Build and run all the services with Docker Compose

When all services are running, you can upload messages to Mindsweeper via http://localhost:8000, access the web interface via http://localhost:8080, and consume the API via http://localhost:5000.

## Basic usage
Upload a `.mind` or a `.mind.gz` file containing snapshots to Mindsweeper using the client's CLI:
```bash
$ python -m mindsweeper.client upload-sample /path/to/file
```
Mindsweeper would then parse the files and upload the snapshots to its database. You could then view them at http://localhost:8080.
