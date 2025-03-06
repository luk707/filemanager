# filemanager

## Setting up the local development stack

###

### Ubuntu/Linux Mint/WSL(Ubuntu)

#### MinIO
##### docker
Confirm docker is installed

```docker --version```

If not;

```sudo apt install docker.io```

##### docker-compose
Confirm docker-compose is installed;

```docker-compose --version```

If not;

```sudo apt install docker-compose```

<br />

**Ensure your user is in the docker group;**

```sudo usermod -dG docker $USER```

**Restart your shell to save change.**


When docker, and docker-compose, are installed

##### Start MinIO

```docker-compose up```

#### FastAPI

```fastapi dev main.py```


<br />

### MacOS

(According to Luke...) simply run `docker compose up` to run the required services locally

