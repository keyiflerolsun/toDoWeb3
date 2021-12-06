# Bu araç @keyiflerolsun tarafından | @KekikAkademi için yazılmıştır.

from toDoWeb3 import app
from toDoWeb3.RamBase import cuzdan_tx_listesi
from flask import request, render_template, session, make_response, jsonify

from Lib.KekikBSC import KekikBSC

@app.route("/gorev_olustur", methods=["GET", "POST"])
def gorev_olustur():
    if request.method == 'GET':
        return render_template('davetsiz.html')

    try:
        private_key     = session['private_key']
        cuzdan_hex      = session['cuzdan_hex']
        yeni_gorev_text = request.form['yeni_gorev_text']

        bsc = KekikBSC(private_key=private_key)
        olusan_gorev = bsc.gorev_olustur(yeni_gorev_text)

        if cuzdan_hex not in cuzdan_tx_listesi.keys():
            cuzdan_tx_listesi[cuzdan_hex] = []

        cuzdan_tx_listesi[cuzdan_hex].append(olusan_gorev)

        return jsonify(olusan_gorev)
    except ValueError:
        return make_response(jsonify(durum="cıks"), 400)
    except Exception:
        return make_response(jsonify(durum="cıks"), 418)