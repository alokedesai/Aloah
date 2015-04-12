import pdb
from flask import Flask, render_template, request, jsonify, Response, redirect, url_for, send_file
from azure.storage import BlobService
import os

app = Flask(__name__)
app.jinja_env.add_extension('jinja2.ext.do')
app.jinja_env.add_extension('jinja2.ext.loopcontrols')

blob_service = BlobService(account_name='aloah', account_key='t4gFHiiTQhPVYLqS3DI0EJ5loeEeU3vUqmIQFp57+UEfdL+FtRrhPAuB4i0Ad1S/pvxvO0DaI87FccGXw4Qstg==')

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        if file:
        	file_location = os.path.abspath(file.filename)
        	blob_service.put_block_blob_from_file('testcontainer',file.filename,file, x_ms_blob_content_type=file.content_type)
        	return redirect(url_for('list'))
    return render_template("index.html")
@app.route("/list")
def list():
	blobs = blob_service.list_blobs('testcontainer')

	return render_template("list.html", blobs = blobs)

@app.route("/download/<filename>")
def download(filename):
	temp = open("temp", "w")
	file_output = blob_service.get_blob_to_file('testcontainer', filename, temp)
	response = send_file("temp", as_attachment=True, attachment_filename=filename)
	os.remove("temp")

	return response

@app.route("/delete/<filename>")
def delete(filename):
	blob_service.delete_blob('testcontainer', filename) 

	return redirect(url_for("upload_file"))

if __name__ == '__main__':
    app.run(debug=True)