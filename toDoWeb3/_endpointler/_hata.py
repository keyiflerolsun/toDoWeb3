# Bu araç @keyiflerolsun tarafından | @KekikAkademi için yazılmıştır.

from toDoWeb3 import app
from flask import make_response, jsonify, send_from_directory
import os

@app.route('/favicon.ico', methods=['GET'])
def favicon():
    return send_from_directory(directory=os.path.join(app.root_path, 'static'), path='images/favicon.ico', mimetype='image/x-icon')

@app.errorhandler(404)
def dort_yuz_dort(error):
    e_tip, e_bilgi = str(error).split(':')
    e_kod  = e_tip[:3]
    e_hata = e_tip[4:]
    return make_response(jsonify(kod=e_kod, hata=e_hata, bilgi=e_bilgi.strip()), 404)

@app.errorhandler(403)
def dort_yuz_uc(error):
    e_tip, e_bilgi = str(error).split(':')
    e_kod  = e_tip[:3]
    e_hata = e_tip[4:]
    return make_response(jsonify(kod=e_kod, hata=e_hata, bilgi=e_bilgi.strip()), 403)

@app.errorhandler(410)
def dort_yuz_on(error):
    e_tip, e_bilgi = str(error).split(':')
    e_kod  = e_tip[:3]
    e_hata = e_tip[4:]
    return make_response(jsonify(kod=e_kod, hata=e_hata, bilgi=e_bilgi.strip()), 410)

@app.errorhandler(500)
def bes_yuz(error):
    e_tip, e_bilgi = str(error).split(':')
    e_kod  = e_tip[:3]
    e_hata = e_tip[4:]
    return make_response(jsonify(kod=e_kod, hata=e_hata, bilgi=e_bilgi.strip()), 500)