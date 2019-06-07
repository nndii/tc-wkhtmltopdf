from pathlib import Path

import pytest
from aiohttp.web import Application

from tc_wkhtmltopdf.types import Settings
from tc_wkhtmltopdf.views import pdf


@pytest.fixture(scope='session')
def app():
    app = Application()
    app['SETTINGS'] = Settings(
        exe_path=Path(__file__),
    )
    app.router.add_post('/pdf', pdf)
    return app
