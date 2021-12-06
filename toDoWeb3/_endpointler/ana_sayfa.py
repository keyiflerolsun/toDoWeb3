# Bu araç @keyiflerolsun tarafından | @KekikAkademi için yazılmıştır.

from toDoWeb3 import app
from toDoWeb3.RamBase import cuzdan_tx_listesi
from flask import session, render_template

from datetime import datetime
from pytz import timezone

tarih = lambda : datetime.now(timezone("Turkey")).strftime("%d-%m-%Y %X")

from Lib.KekikBSC import KekikBSC

@app.route("/", methods=["GET", "POST"])
def ana_sayfa():
    if not session:
        return render_template(
            'ana_sayfa.html',
            baslik = "toDoWeb3",
            icerik = "toDoWeb3",
            tarih  = tarih()
        )

    bsc = KekikBSC(private_key = session['private_key'])

    try:
        tx_listesi = cuzdan_tx_listesi[session['cuzdan_hex']]
    except KeyError:
        tx_listesi = None

    return render_template(
        'ana_sayfa.html',
        baslik     = "toDoWeb3",
        icerik     = "toDoWeb3",
        tarih      = tarih(),
        kontrat    = bsc.kontrat_hex,
        session    = session,
        gorevlerim = bsc.benim_gorevlerim,
        tx_listesi = tx_listesi
    )