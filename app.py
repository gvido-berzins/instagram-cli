from flask import (
    Flask, render_template, request
)

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    errors = []
    results = {}
    # if request.method == "POST":
        # # get url that the user has entered
        # try:
            # url = request.form['url']
            # r = requests.get(url)
            # print(r.text)
        # except:
            # errors.append(
                # "Unable to get URL. Please make sure it's valid and try again."
            # )
    return render_template('index.html', errors=errors, results=results)


@app.route('/login', methods=['GET', 'POST'])
def login():
    errors = []
    results = {}

    return render_template('login.html', errors=errors, results=results)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5598, debug=True)
