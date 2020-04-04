# Toast Backend
## Set up
- `git clone` this repo 
- [Install docker](https://docs.docker.com/docker-for-mac/install/)
- Check the version by `docker --version`
- Make sure Docker desktop is running 
- `cd` into `/backend`
- Create an `.env.dev` file to store the environment variables which can be copied over from the codeshare url (Check Slack) 
- Build the docker image by `docker-compose up --build`
- The Django app will be hosted on `http://0.0.0.0:8000/`
