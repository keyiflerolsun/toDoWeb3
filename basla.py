# Bu araç @keyiflerolsun tarafından | @KekikAkademi için yazılmıştır.

from toDoWeb3 import app, onemli
from os import environ

port = int(environ.get("PORT", 6300))
host = "0.0.0.0"

if __name__ == '__main__':
    # app.run(debug = True, host = '0.0.0.0', port = port)

    onemli(f'\ntoDoWeb3 [bold red]{host}[yellow]:[/]{port}[/]\'de başlatılmıştır...\n')

    from waitress import serve
    serve(app, host = host, port = port)
    # serve(app, host = host, port = port, url_scheme = 'https')