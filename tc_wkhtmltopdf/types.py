from enum import Enum
from pathlib import Path
from typing import NamedTuple, Optional

CWD = Path.cwd()


class HtmlHeader(Enum):
    """HtmlHeader types for --header-html arg to wkhtmltopdf."""

    default = 'default'


class Header(Enum):
    """Request headers names."""

    args = 'TC_PDF_ARGS'
    htmlheader = 'TC_PDF_HTMLHEADER'


class Settings(NamedTuple):
    exe_path: Path

    htmlheader_default: Path = CWD / 'static' / 'headers' / 'default.html'

    def htmlheader(
        self,
        htmlheader_type: Optional[HtmlHeader],
    ) -> Optional[Path]:

        if htmlheader_type is None:
            return None
        return getattr(self, f'htmlheader_{htmlheader_type.value}', None)
