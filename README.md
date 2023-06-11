# Watch Next

[Documentation](https://drive.google.com/file/d/1eiwaazx7lD3NpryT07yIzt_COT05oJBj/view?usp=sharing)

## Prerequisites
- Docker
- Docker Compose

## Usage

### Starting the containers
To (re)build images and start the containers, run the following in the project root directory:
```bash
$ docker compose up --build -d
```
The web UI will be available at http://0.0.0.0:3000 (e.g. http://localhost:3000).

### Stopping the containers
To stop the containers, run the following in the project root directory:
```bash
$ docker compose down
```
