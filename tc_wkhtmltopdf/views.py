from aiohttp.web import Request, Response

from tc_wkhtmltopdf.pdf import Pdf


async def pdf(request: Request) -> Response:
    pdf = await Pdf.from_request(request)
    wk_result = await pdf.to_pdf()
    return await wk_result.to_response()
