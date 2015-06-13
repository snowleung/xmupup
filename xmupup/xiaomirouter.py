# coding: utf-8


from flask import send_file, Flask, make_response, request, render_template
from werkzeug import secure_filename


app = Flask(__name__)
INTERNAL_IP = '192.168.31.159'
INTERNAL_PORT = '5000'
INTERNAL_URL = 'http://{}:{}/get_files'.format(INTERNAL_IP,
                                            INTERNAL_PORT)

@app.route('/get_files', methods=['get', 'post'])
def get_files():
    """"""
    template = 'files.html'
    name = request.args.get('name')
    if not name:
        if request.method == 'POST':
            # save upload file
            f = request.files['file']
            f.save('./static/' + secure_filename(f.filename))
        import os
        files = os.listdir('./static')
        datas = {
            'files': ['{}?name={}'.format(INTERNAL_URL, f) for f in sorted(files)]}
        return make_response(render_template(template, **datas))
    else:
        f = open('./static/{}'.format(name))
        return send_file(f, attachment_filename='{}'.format(name), as_attachment=True)


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0')
