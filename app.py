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
        	blob_service.put_block_blob_from_file('testcontainer','aloah',file, x_ms_blob_content_type=file.content_type)
        	return redirect(url_for('test'))
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form action="" method=post enctype=multipart/form-data>
      <p><input type=file name=file>
         <input type=submit value=Upload>
    </form>
    '''
@app.route("/test")
def test():
	return "it worked!"
if __name__ == '__main__':
    app.run(debug=True)