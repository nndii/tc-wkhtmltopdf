import asyncio
from pathlib import Path

import pytest
from aiohttp.streams import StreamReader
from aiohttp.test_utils import make_mocked_request
from asynctest.mock import Mock

from tc_wkhtmltopdf.pdf import Pdf
from tc_wkhtmltopdf.types import Header


async def create_stream(data: bytes):
    loop = asyncio.get_event_loop()
    protocol = Mock(_reading_paused=False)
    stream = StreamReader(protocol, loop=loop)
    stream.feed_data(data)
    stream.feed_eof()
    return stream


@pytest.fixture(scope='function')
async def pdf_request(app, headers=None):
    async def factory(headers):
        return make_mocked_request(
            app=app,
            method='POST',
            path='/pdf',
            headers=headers,
            payload=await create_stream(b'HELLO'),
        )
    return factory


@pytest.mark.asyncio
async def test_from_request(app, pdf_request):
    _request = await pdf_request({
        Header.args.value: '--zoom 5 --orientation album',
        Header.htmlheader.value: 'default',
    })
    pdf = await Pdf.from_request(_request)

    assert pdf.args == ['--zoom', '5', '--orientation', 'album']
    assert pdf.html == b'HELLO'
    assert pdf.htmlheader == pdf.settings.htmlheader_default


@pytest.mark.parametrize('args,htmlheader,result', [
    (
        ['--zoom', '5', '--test', 'test'],
        Path('/usr/local/default.html'),
        '-q --html-header /usr/local/default.html --zoom 5 --test test - -',
    ),
    (
        ['--zoom', '5', '--test', 'test'],
        None,
        '-q --zoom 5 --test test - -',
    ),
    (
        [],
        None,
        '-q - -',
    ),
])
async def test_build_args(app, args, htmlheader, result):
    pdf = Pdf(
        settings=app['SETTINGS'],
        args=args,
        htmlheader=htmlheader,
        html=b'',
    )
    assert ' '.join(pdf.build_args()) == result
