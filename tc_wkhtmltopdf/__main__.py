"""WKHTMLTOPDF service

Usage:
  tc_wkhtmltopdf run [--listen=<hostport>] [--exe-path=<path>]

Options:
  -h --help            Show this screen.
  --listen=<hostport>  Listen host and port [default: {TC_PDF_LISTEN}]
  --exe-path=<path>    wkhtmltopdf binary path [default: {TC_PDF_EXE}]
"""
import os
from pathlib import Path

import hostport
from aiohttp.web import Application, normalize_path_middleware, run_app
from aiohttp.web_exceptions import HTTPPermanentRedirect
from docopt import docopt
from loguru import logger

from . import types, views  # noqa: Z300


def setup_routes(app: Application):
    app.router.add_post('/pdf', views.pdf)


async def create_app(
    exe_path: str,
) -> Application:

    app = Application(middlewares=[
        normalize_path_middleware(
            append_slash=True,
            redirect_class=HTTPPermanentRedirect,
        ),
    ])
    try:
        app['SETTINGS'] = types.Settings(
            exe_path=Path(exe_path),
        )
    except Exception as e:
        logger.error(str(e))
        raise

    setup_routes(app)
    return app


def main() -> None:
    _oeg = os.environ.get
    args = docopt(__doc__.format(
        TC_PDF_LISTEN=_oeg('TC_PDF_LISTEN', 'localhost:8080'),
        TC_PDF_EXE=_oeg('TC_PDF_EXE', '/srv/src/wkhtmltopdf'),
    ))

    app = create_app(
        exe_path=args['--exe-path'],
    )

    listen = hostport.parse(args['--listen'])
    logger.info(f'run application on {listen.host}:{listen.port}')
    run_app(
        app=app,
        host=listen.host,
        port=listen.port,
    )


if __name__ == '__main__':
    main()
