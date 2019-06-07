from aiohttp.web import Response
from asynctest import patch
from asynctest.mock import CoroutineMock, Mock

wkhtmlrequest = '<h1>Hello World</h1>'


async def test_pdf_view(app, aiohttp_client):
    client = await aiohttp_client(app)
    wk_result = Mock(
        pdf=b'HELLO',
        stderr=None,
        code=0,
        to_response=CoroutineMock(
            return_value=Response(
                body=b'HELLO',
                content_type='application/pdf',
            ),
        ),
    )
    _wkhtmlrun = CoroutineMock(
        return_value=wk_result,
    )
    with patch('tc_wkhtmltopdf.pdf.Pdf.wkhtml_run', _wkhtmlrun):
        resp = await client.post('/pdf', data=wkhtmlrequest)

        assert resp.status == 200
        assert await resp.text() == 'HELLO'
