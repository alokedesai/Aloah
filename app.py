import pdb
from flask import Flask, render_template, request, jsonify, Response, redirect, url_for
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
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form action="" method=post enctype=multipart/form-data>
      <p><input type=file name=file>
         <input type=submit value=Upload>
    </form>
    '''
@app.route("/list")
def list():
	blobs = blob_service.list_blobs('testcontainer')

	return render_template("list.html", blobs = blobs)

@app.route("/download/<filename>")
def download(filename):
	file_output = blob_service.get_blob('testcontainer', filename)
    # This is the key: Set the right header for the response
    # to be downloaded, instead of just printed on the browser
    # response.headers["Content-Disposition"] = "attachment; filename=" + filename
    
    # headers = {"Content-Disposition": "attachment; filename=%s" % filename}
    # with open(file_output, 'r') as f:
    # 	body = f.read()
    # return make_response((body, headers))
    return file_output
	


if __name__ == '__main__':
    app.run(debug=True)