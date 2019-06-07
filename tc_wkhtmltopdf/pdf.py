import asyncio
from pathlib import Path
from shlex import quote
from typing import Iterable, List, NamedTuple, Optional, Type, TypeVar

from aiohttp.web import Request
from loguru import logger

from tc_wkhtmltopdf.types import Header, HtmlHeader, Settings
from tc_wkhtmltopdf.wk_result import WkResult

P = TypeVar('P', bound='Pdf')


class Pdf(NamedTuple):
    settings: Settings
    args: Iterable[str]
    html: bytes
    htmlheader: Optional[Path]

    @classmethod
    async def from_request(cls: Type[P], request: Request) -> P:
        settings: Settings = request.app['SETTINGS']
        htmlheader_type_raw = request.headers.get(Header.htmlheader.value)
        if htmlheader_type_raw is None:
            htmlheader_type = None
        else:
            htmlheader_type = HtmlHeader[htmlheader_type_raw]
        args = request.headers.get(Header.args.value, '')
        return cls(
            settings=settings,
            args=args.split(' ') if args else [],
            html=await request.read(),
            htmlheader=settings.htmlheader(htmlheader_type),
        )

    def build_args(self) -> List[str]:
        options = ['-q']
        args = ['-', '-']

        if self.htmlheader is not None:
            options.extend(['--html-header', f'{self.htmlheader}'])

        if self.args:
            options.extend(list(self.args))

        logger.debug('args: {}', options + args)
        return options + args

    async def wkhtml_run(self) -> WkResult:
        proc = await asyncio.create_subprocess_exec(
            str(self.settings.exe_path),
            *self.build_args(),
            stdin=asyncio.subprocess.PIPE,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        proc.stdin.write(self.html)
        proc.stdin.close()
        return await WkResult.from_process(proc)

    async def to_pdf(self) -> WkResult:
        logger.debug('Request content: {}', self.html)
        return await self.wkhtml_run()
