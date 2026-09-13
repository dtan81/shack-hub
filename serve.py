import json
from pathlib import Path
from urllib.request import urlopen
from urllib.error import URLError
from flask import Flask, send_from_directory, jsonify
app = Flask(__name__)
ROOT = Path(__file__).resolve().parent
@app.route('/')
@app.route('/hub')
def hub():
    return send_from_directory(ROOT, 'hub.html')
@app.route('/hosts.json')
def hosts():
    return send_from_directory(ROOT, 'hosts.json')
@app.route('/ping/<host_id>')
def ping(host_id):
    data = json.loads((ROOT / 'hosts.json').read_text())
    host = next((h for h in data.get('hosts', []) if h.get('id') == host_id), None)
    if not host:
        return jsonify({'ok': False}), 404
    url = host['url'].rstrip('/') + '/api/status'
    try:
        with urlopen(url, timeout=2.5) as r:
            body = json.loads(r.read().decode())
        return jsonify({'ok': True, 'system': body.get('system', {})})
    except (URLError, TimeoutError, ValueError, json.JSONDecodeError):
        return jsonify({'ok': False}), 502
if __name__ == '__main__':
    print('Shack Hub on 0.0.0.0:8081')
    app.run(host='0.0.0.0', port=8081, threaded=True)
