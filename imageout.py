from flask import Flask, send_file, request
import barcode
from barcode.writer import ImageWriter
import qrcode
from io import BytesIO

app = Flask(__name__)

@app.route('/barcode/<text>')
def gen_barcode(text):
    code_type = request.args.get('type', 'code128')
    try:
        bc_class = barcode.get_barcode_class(code_type)
        bc = bc_class(text, writer=ImageWriter())
        buf = BytesIO()
        bc.write(buf)
        buf.seek(0)
        return send_file(buf, mimetype='image/png')
    except Exception as e:
        return str(e), 400

@app.route('/qrcode/<text>')
def gen_qrcode(text):
    img = qrcode.make(text)
    buf = BytesIO()
    img.save(buf, format='PNG')
    buf.seek(0)
    return send_file(buf, mimetype='image/png')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8503)