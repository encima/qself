from flask import Flask, render_template

app = Flask(__name__)

@app.route('/spotify')
def callback():
    return render_template('redirect', req.args.code)

def shutdown_server():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()


def start_server():
    app.run(port=8080)
