import json

import pytest
from aiohttp.web import Response, json_response
from asynctest.mock import CoroutineMock, Mock

from tc_wkhtmltopdf.wk_result import WkResult


@pytest.mark.parametrize('stdo,stde,code', [
    (b'TESTTEST', b'ERROR', 1),
    (b'TESTTEST', b'', 0),
])
async def test_wk_result(stdo, stde, code):
    process = Mock(
        returncode=code,
        communicate=CoroutineMock(
            return_value=(stdo, stde),
        ),
    )
    wk_result = await WkResult.from_process(process)
    resp = await wk_result.to_response()
    if code:
        assert json.loads(resp.text) == {
            'status': 'error',
            'desc': stde.decode(),
        }
        assert resp.status == 400
    else:
        assert resp.status == 200
        assert resp.body == stdo
