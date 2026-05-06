from flask import Flask, send_file, request
import barcode
from barcode.writer import ImageWriter
import qrcode
from io import BytesIO

app = Flask(__name__)

@app.route('/code/<text>')
def gen_barcode(text):
    code_type = request.args.get('type', 'code128')
    width = float(request.args.get('width', 100))
    height = float(request.args.get('height', 30))
    size = int(request.args.get('size', 10))
    border = int(request.args.get('border', 4))

    if code_type == 'qrcode':
        img = qrcode.make(text, box_size=size, border=border)
        buf = BytesIO()
        img.save(buf, format='PNG')
        buf.seek(0)
        return send_file(buf, mimetype='image/png')

    try:
        bc_class = barcode.get_barcode_class(code_type)
        options = {
            'module_width': width / 100,
            'module_height': height,
            'font_size': int(height * 0.5),
            'text_distance': 10,
            'quiet_zone': 2,
        }
        if code_type == 'code39':
            bc = bc_class(text, writer=ImageWriter(), add_checksum=False)
        else:
            bc = bc_class(text, writer=ImageWriter())
        buf = BytesIO()
        bc.write(buf, options=options)
        buf.seek(0)
        return send_file(buf, mimetype='image/png')
    except Exception as e:
        return str(e), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8503)