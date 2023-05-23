# github-status

## Deployment
Build Docker image with:

`docker build -f ./Dockerfile -t githubstatus .`

Then run it like this:

`docker run --env BOT_TOKEN=<token> --env CHAT_ID=<chat_id> githubstatus`
