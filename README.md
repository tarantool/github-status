# github-status

## Deployment
Build Docker image with:

`docker build -f ./Dockerfile -t githubstatus .`

Then run it like this:

`docker run --env BOT_TOKEN=<token> --env CHAT_ID=<chat_id> githubstatus`

## Run flake8
`flake8`

## Run tests:
`pip install -r test-requirements.txt`\
`python -m pytest -v test/`