# weekend-ui
Currently working on some cancer stuff

## Dev

Quickly get the project up and running with `poetry`:
```bash
poetry run streamlit run Main_Page.py
```

## Deployment

A Dockerfile is included if you want to deploy the website.

```bash
docker build . -t app
docker run -p 80:8501 app
```

Note that the website runs in debug mode by default.
Set `DEBUG=false` in your environment to disable debug logs.
This is already done in the Dockerfile.

