from flask import Flask, render_template, request, jsonify
from flask_cors import CORS, cross_origin
from urllib.request import urlopen
import logging
import pymongo
logging.basicConfig(filename="scrapper.log" , level=logging.INFO)
import concurrent
from functions_copy import max_scrolls,videos_links, url_client, process_video

app = Flask(__name__)

@app.route("/", methods=["GET"])
@cross_origin()
def homepage():
    try:
        return render_template("index.html")
    except Exception as e:
        logging.error(str(e))
        return "An error occurred."

@app.route('/data', methods=['POST','GET'])
@cross_origin()
def index():
    if request.method == 'POST':
        try:
            SearchString = request.form['yt_id'].replace('@', '')
            videos = request.form['#videos']
            url = "https://www.youtube.com/@" + SearchString + '/videos'

            # Storing the data
            data = []

            # Scroll count and html file 
            scrolls_count = max_scrolls(int(videos))
            html_file = videos_links(scrolls_count,url)
            
            # Extrating Titles and URLs
            video_urls = []
            videos_titles = []
            all_videos_metadata = html_file.find_all("a",{'id':"video-title-link"})
            for i in all_videos_metadata:
                videos_titles.append(i.text)
                video_urls.append(f'https://www.youtube.com{i.get("href")}')

            # Extracting data for videos 
            num_threads = 6
            with concurrent.futures.ThreadPoolExecutor(max_workers=num_threads) as executor:
                results = list(executor.map(process_video, video_urls))

            for videos_title,video_url, result in zip(videos_titles,video_urls, results):
                likes, genre, duration, views, uploads, description = result
                mydict = {"Title":videos_title, "URL":video_url, "Likes":likes,
                        "Genre":genre, "Duration":duration, "Views":views, 
                        "Uploads":uploads, "Description":description}
                data.append(mydict)
            logging.info("log my final result {}".format(data))

            return render_template('result.html', result=data)
        
        except Exception as e:
            logging.info(e)
            return f'try again {e}'
    
    else:
        return render_template('index.html')
        

if __name__ == "__main__":
    app.run(host="0.0.0.0")

