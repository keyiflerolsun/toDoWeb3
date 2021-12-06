# Bu araç @keyiflerolsun tarafından | @KekikAkademi için yazılmıştır.

from toDoWeb3 import app
from toDoWeb3.RamBase import cuzdan_tx_listesi
from flask import request, render_template, session, make_response, jsonify

from Lib.KekikBSC import KekikBSC

@app.route("/gorev_tamamla", methods=["GET", "POST"])
def gorev_tamamla():
    if request.method == 'GET':
        return render_template('davetsiz.html')

    try:
        private_key = session['private_key']
        cuzdan_hex  = session['cuzdan_hex']
        gorev_id    = int(request.form['gorev_id'])

        bsc = KekikBSC(private_key=private_key)
        tamamlanan_gorev = bsc.gorev_tamamla(gorev_id)

        if cuzdan_hex not in cuzdan_tx_listesi.keys():
            cuzdan_tx_listesi[cuzdan_hex] = []

        cuzdan_tx_listesi[cuzdan_hex].append(tamamlanan_gorev)

        return jsonify(tamamlanan_gorev)
    except ValueError:
        pass
    except Exception:
        return make_response(jsonify(durum="cıks"), 418)