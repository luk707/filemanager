# filemanager

## Contributors ✨

Thanks go to these wonderful people

<a href = "https://github.com/luk707/filemanager/graphs/contributors">
  <img src = "https://contrib.rocks/image?repo=luk707/filemanager"/>
</a>

Made with [contributors-img](https://contrib.rocks).

## Development

### Prerequisites

This application depends on a minio instance. A docker compose manifest is provided to simplify your local configuration for development.

Ensure you have [docker installed](#installing-docker-and-docker-compose), and run the following:

`docker-compose up`

### Backend

`fastapi dev main.py`

### Frontend

The frontend can be run simply by running `npm run dev` in the `client` directory of the repo.

Dependencies can be installed using `npm install` to fetch new dependencies and `npm install <NAME_OF_DEP>` to add a new dependency.

Unit tests can be run using `npm test`.

## Tips

### Installing node and npm

### Installing docker and docker compose

#### macOS

Take a look at [Orb Stack](https://orbstack.dev/), it provides docker & docker compose out of the box.

#### Ubuntu/Linux Mint/WSL(Ubuntu)

Confirm docker is installed

`docker --version`

If not;

`sudo apt install docker.io`

Confirm docker-compose is installed;

`docker-compose --version`

If not;

`sudo apt install docker-compose`

<br />

**Ensure your user is in the docker group;**

`sudo usermod -dG docker $USER`

**Restart your shell to save change.**
