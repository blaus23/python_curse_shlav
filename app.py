#!/usr/bin/python3

from flask import Flask, request, render_template, send_file, send_from_directory
import os
import time

app = Flask(__name__)

# Custom 404 page
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

# Custom 500 page
@app.errorhandler(500)
def page_not_found(e):
    return render_template('500.html'), 500

# Remove the image file and image itself
def removeFile(path):
    os.system(rf'rm -rf {path}')

# Download the image.tar to the client pc
def downloadFile (path):
    try:
        return send_file(path, as_attachment=True)
    finally:
        removeFile(path)

# Main page index.html
@app.route('/')
def my_form():
    return render_template('index.html')

# Gets the input from user in the form, download the docker image to the server
# And calls the downloadFile function
@app.route('/', methods=['GET','POST'])
def my_form_post():
    text = request.form['text']
    
    # Getting rid of the / in the docker image name
    if '/' in text:
        text_download = (text.split('/'))[0]
    else:
        text_download = text

    pull_cmd = rf'docker pull {text}'
    save_cmd = rf'docker save -o {text_download}.tar {text}'

    # Pull & save the docker image
    os.system(pull_cmd)
    os.system(save_cmd)

    # Download the image to the user's Desktop
    os.system(rf'chmod 700 {text}.tar')
    path = rf'{text}.tar'
    return downloadFile(path)

def main():

    # Clean the docker stuff before running the app
    clean_system_cmd = rf'/usr/bin/docker system prune -f'
    os.system(clean_system_cmd)

    # Runs the app in the local IP address in port 80 (http)
    #app.run(host='0.0.0.0', port='80')

    # Runs the app in the local IP address in port 443 (https)
    app.run(host='0.0.0.0', port='443', ssl_context=('ssl/cert.pem', 'ssl/key.pem'))

if __name__ == '__main__':
    main()
