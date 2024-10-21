# YouTube gif maker

Easily make and share GIFs of your favorite YouTube moments.

- [Using the app](#using-the-app)
- [Install and run the app using Python](#install-and-run-the-app-using-python)
- [Install and run the app using Docker](#install-and-run-the-app-using-docker)
- [How it works](#how-it-works)

## Using the app

To use the app

1.  Find a youtube / shorts url containing a short phrase you want to gif-a-fy
2.  Enter text describing the moment you want to gif-a-fy
3.  Click the 'create gif' button to create your gif, download, and share!

After creation you can manually adjust, trim, or extend the length of your gif.

Here's a brief gif showing how easy it is to create gifs using the app.

<div align="center">
<img align="center" src="https://github.com/jermwatt/readme_gifs/blob/main/yt_gif_maker.gif" height="325">
</div>

And here are a few gifs made using the app

<div align="center">
<img src="https://github.com/jermwatt/readme_gifs/blob/main/yt-gify-example-0.gif" height="325">
<img src="https://github.com/jermwatt/readme_gifs/blob/main/yt-gify-example-1.gif" height="325">
<img src="https://github.com/jermwatt/readme_gifs/blob/main/yt-gify-example-2.gif" height="325">
</div>

## Install and run the app using Python

To run the app install the associated `requirements.txt` and run

```python
python -m streamlit run yt_gif_maker/app.py
```

## Install and run the app using Docker

Or run via Docker

```sh
docker compose up
```

You do _not_ need a GPU to run this locally.

## How it works

The app pulls your desired YouTube video and - if available - YouTube's automated transcript. Because these transcripts tend to be low quality, you can also produce your own using any of Whisper's core models (including the newly released turbo).

A vector embedding of the transcription is then created for semantic matching of your input phrase.

Once the best match is found the corresponding timestamps are used to create an initial clip + gif of your input phrase. You can then manually adjust the start/stop time of your gif, download, and share!
