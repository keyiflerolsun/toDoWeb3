# Bu araç @keyiflerolsun tarafından | @KekikAkademi için yazılmıştır.

from toDoWeb3 import app
from flask import request, render_template, session, make_response, jsonify

from Lib.KekikBSC import KekikBSC

@app.route("/cuzdan_ekle", methods=["GET", "POST"])
def cuzdan_ekle():
    if request.method == 'GET':
        return render_template('davetsiz.html')

    try:
        private_key = request.form['private_key']
        cuzdan_adi  = request.form['cuzdan_adi']

        bsc = KekikBSC(private_key=private_key)

        session['cuzdan_hex']  = bsc.cuzdan
        session['cuzdan_adi']  = cuzdan_adi
        session['private_key'] = private_key

        return jsonify({
            "durum"      : "tm",
            "cuzdan_adi" : cuzdan_adi,
            "cuzdan_hex" : bsc.cuzdan,
            "private_key": private_key,
            "network"    : bsc.network_adi
        })
    except ValueError:
        return make_response(jsonify(durum="cıks"), 400)
    except Exception:
        return make_response(jsonify(durum="cıks"), 418)