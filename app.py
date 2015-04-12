from flask import Flask, render_template, request, jsonify, Response

app = Flask(__name__)
app.jinja_env.add_extension('jinja2.ext.do')
app.jinja_env.add_extension('jinja2.ext.loopcontrols')


@app.route('/')
def index():
	return render_template("index.html")

if __name__ == '__main__':
    app.run(debug=True)