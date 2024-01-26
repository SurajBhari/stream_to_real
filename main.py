from flask import Flask, render_template, request, redirect, url_for, session, flash
from urllib import parse
from chat_downloader.sites import YouTubeChatDownloader
from datetime import datetime


app = Flask(__name__)



@app.route('/')
def index():
    return render_template('index.html', output=[])


@app.route("/ytrt")
def ytrt():
    print("YTRT called")
    stream_url = request.args.get('Stream-url')
    if not stream_url:
        return render_template('index.html', output=[], is_output_link=False)
    output = []
    for stream in stream_url.split("\n"):
        x = parse.urlparse(stream)
        video_id = ""
        if x.path =="/watch":
            video_id = x.query.replace("v=","")
        if "/live/" in x.path:
            video_id = x.path.replace("/live/","")
        video_id = video_id.split("&")[0]   
        t = x.query.split("&")
        for i in t:
            if "t=" in i:
                t = i.split("t=")[1]
                break
        t = t.replace("s", "")
        print(video_id)
        vid = YouTubeChatDownloader().get_video_data(video_id=video_id)
        start_time = vid["start_time"] / 1000000 
        actual_time = start_time + int(t)
        actual_time = datetime.fromtimestamp(actual_time).strftime('%Y-%m-%d %H:%M:%S')
        output.append(f"{actual_time} https://youtu.be/{video_id}?t={t}s")
    return render_template('index.html', output=output, is_output_link=False)

@app.route("/rtyt")
def rtyt():
    print("rtyt called")
    stream_url = request.args.get('Stream-url')
    if not stream_url:
        return render_template('index.html', output=[], is_output_link=False)
    if not request.args.get('appt'):
        return render_template('index.html', output=["Enter Time"], is_output_link=False)
    output = []
    _time = request.args.get('appt')
    for stream in stream_url.split("\n"):
        x = parse.urlparse(stream)
        video_id = ""
        if x.path =="/watch":
            video_id = x.query.replace("v=","")
        if "/live/" in x.path:
            video_id = x.path.replace("/live/","")
        video_id = video_id.split("&")[0]   
        video_id.replace("/","")
        print(video_id)
        vid = YouTubeChatDownloader().get_video_data(video_id=video_id)
        print(vid)
        start_time = vid["start_time"] / 1000000  # let say stream started at 21-01-2024 10:00:00
        start_dt = datetime.fromtimestamp(start_time)
        time = datetime.strptime(_time, '%H:%M')
        dt = datetime(
            year=start_dt.year, 
            month=start_dt.month, 
            day=start_dt.day, 
            hour=time.hour,
            minute=time.minute, 
            second=time.second
        )
        gap = dt.timestamp() - start_time
        gap = int(gap)
        if gap < 0:
            output.append(f"Invalid time for {stream}, not started yet, {gap} seconds till stream starts\n")
            continue
        if gap > vid["duration"]:
            output.append(f"\nInvalid time for {stream}, stream ended, {gap} seconds after stream ended\n")
            continue
        link = f"https://youtu.be/watch?v={video_id}&t={gap}s"
        output.append(link)
    return render_template('index.html', output=output, is_output_link=True)
if __name__ == '__main__':
    app.run(port=5000, debug=True)
