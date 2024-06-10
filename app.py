from flask import Flask, request, jsonify
from flask_cors import CORS
from pytube import YouTube
import ssl

# Bypass SSL verification for pytube
ssl._create_default_https_context = ssl._create_unverified_context

app = Flask(__name__)
CORS(app)  # Enable CORS for all origins


@app.route("/videoId", methods=["GET"])
def videoId():
    try:
        url = request.args.get("url", "")
        if not url:
            return jsonify({"error": "No URL provided"}), 400

        # Extract the video ID from the URL
        video_id = url.split("v=")[1].split("&")[0]

        yt = YouTube(f"http://youtube.com/watch?v={video_id}")
        title = yt.title
        video_url = yt.streams.get_by_itag(18).url  # Get the URL for itag 18 (360p)

        # Return the video title and URL
        return video_url, 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/videoThumb", methods=["GET"])
def videoThumb():
    try:
        url = request.args.get("url", "")
        video_id = url.split("=")[1].split("&")[0]
        videoUrl = f"https://www.youtube.com/embed/{video_id}"
        return videoUrl, 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# if __name__ == "__main__":
#     app.run(debug=True)
