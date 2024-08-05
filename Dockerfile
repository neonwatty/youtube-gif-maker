FROM python:3.10-slim

RUN apt-get update && apt-get install -y \
    build-essential \
    software-properties-common \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /home

ENV PYTHONPATH=.

COPY requirements.txt /home/requirements.txt
COPY yt_gif_maker /home/yt_gif_maker
COPY .streamlit /home/.streamlit
RUN pip3 install -r /home/requirements.txt

# moviepy / decorator needs to be reinstalled to avoid error --> https://github.com/Zulko/moviepy/issues/1321
RUN pip3 uninstall moviepy decorator -y
RUN pip3 install moviepy

EXPOSE 8502

HEALTHCHECK CMD curl --fail http://localhost:8502/_stcore/health || exit 1

ENTRYPOINT ["streamlit", "run", "/home/yt_gif_maker/app.py", "--server.port=8502", "--server.address=0.0.0.0"]