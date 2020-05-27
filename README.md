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

## About

## Installation

Clone the repository and enter the project's root folder:
```
git clone https://github.com/bar-amir/mindsweeper.git
cd mindsweeper
```

Grant execution permissions to all scripts:
```
chmod a=rx -R scripts 
```

Run install.sh
```
https://github.com/bar-amir/mindsweeper/blob/master/README.md
scripts/install.sh
```
The script will:
* Create a virtual enviroment
* Install dependencies, both for Python and Node
* Compile .proto files

## Running locally

### Running with Docker
Simply use Docker Compose:
```
docker-compose up
```

### Running locally

Activate virtual enviroment:
```
source .env/bin/activate
```
Now you can start any service using Python API or the CLI (Read more here).

## Sample File
Download sample.mind.gz from here. [reupload to GCP]
from mindsweeper root folder, run
upload-sample path_to_sample/sample.mind.gz
