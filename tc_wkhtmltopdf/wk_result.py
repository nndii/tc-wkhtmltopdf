from asyncio.subprocess import Process
from http import HTTPStatus
from typing import NamedTuple, Optional, Type, TypeVar

from aiohttp.web import Response, json_response

W = TypeVar('W', bound='WkResult')


class WkResult(NamedTuple):
    pdf: Optional[bytes]
    stderr: Optional[str]
    code: int

    @classmethod
    async def from_process(cls: Type[W], process: Process) -> W:
        stdout, _stderr = await process.communicate()
        stderr = _stderr.decode('utf8')
        return cls(
            pdf=stdout if stdout else None,
            stderr=stderr if stderr else None,
            code=process.returncode,
        )

    async def to_response(self) -> Response:
        if self.code == 0 and self.pdf is not None:
            return Response(
                body=self.pdf,
                content_type='application/pdf',
            )

        return json_response(
            data={
                'status': 'error',
                'desc': self.stderr,
            },
            status=HTTPStatus.BAD_REQUEST,
        )
