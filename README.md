# Toast Backend
## Set up
- `git clone` this repo 
- [Install docker](https://docs.docker.com/docker-for-mac/install/)
- Check the version by `docker --version`
- Make sure Docker desktop is running 
- `cd` into `/backend`
- Build the docker image by `docker-compose up --build`
- The Django app will be hosted on `http://0.0.0.0:8000/`
- Append `api/clients/` to the url to hit the sample endpoint
