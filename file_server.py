from flask import Flask, request, send_file, abort, jsonify
from repo_utils import get_repo

app = Flask(__name__)
#app.config['REPO_PATH'] = '/home/plus/img_repo'
app.config['REPO_PATH'] = 'img_repo'

@app.route('/show/<filename>/')
def show(filename):
    if '..' in filename or filename.startswith('/'):
        abort(404)

    path = get_repo().get_file(filename)
    # add_etags needs to be False, otherwise flask will check the file in current path,
    # but the file doesn't exist in currrent path, so it will raise an Exception,
    return send_file(path)


@app.route('/upload/', methods=['POST'])
def upload():
    """Upload a new file."""
    name = request.form.get('name')
    is_sha1 = request.form.get('sha1', 0, int)
    filename = get_repo().save(request.files['upload'], name, bool(is_sha1))
    return jsonify(name=filename)


if __name__ == '__main__':
    app.run(debug=True)
