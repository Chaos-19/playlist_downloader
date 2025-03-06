'''
from concurrent.futures import ThreadPoolExecutor
from flask import Blueprint, render_template,request
import yt_dlp
import json

api_ytvd = Blueprint('api_ytvd', __name__)
executor = ThreadPoolExecutor()

def fetch_metadata(ytv_url):
    with yt_dlp.YoutubeDL({}) as ydl:
        return ydl.extract_info(ytv_url, download=False)

@api_ytvd.route('/ytv-metadata', methods=['GET', 'POST'])
def get_ytv_metadata():
    if request.method == 'GET':
        ytv_url = request.args.get('url')
    else:  # POST
        data = request.get_json()
        ytv_url = data.get("url")

    if not ytv_url:
        return jsonify({"error": "Missing 'url' parameter"}), 400

    future = executor.submit(fetch_metadata, ytv_url)
    info = future.result(timeout=3000)  # Waits up to 30 seconds
    
    print(json.dumps({
        "title": info.get('title'),
        "total_videos": len(info.get('entries', []))
    }))

    return jsonify({
        "title": info.get('title'),
        "total_videos": len(info.get('entries', []))
    })

@api_ytvd.route('/ytv-download')
def get_ytv():
    return "Logged out"
'''
from flask import Blueprint, request, jsonify
from app.tasks import fetch_metadata

api_ytvd = Blueprint('api_ytvd', __name__)

@api_ytvd.route('/ytv-metadata', methods=['GET', 'POST'])
def get_ytv_metadata():
    """API endpoint to fetch YouTube metadata asynchronously."""
    if request.method == 'GET':
        ytv_url = request.args.get('url')
    else:  # POST
        data = request.get_json()
        ytv_url = data.get("url")

    if not ytv_url:
        return jsonify({"error": "Missing 'url' parameter"}), 400

    task = fetch_metadata.delay(ytv_url)  # Run Celery task in the background
    return jsonify({"task_id": task.id, "status": "Processing"}), 202

@api_ytvd.route('/task-status/<task_id>', methods=['GET'])
def get_task_status(task_id):
    """API endpoint to check the status of a Celery task."""
    from celery.result import AsyncResult
    from app import celery

    task_result = AsyncResult(task_id, app=celery)
    return jsonify({"task_id": task_id, "status": task_result.status, "result": task_result.result})