FROM python:3.7-alpine3.8
LABEL maintainer="Alexander Zelenyak <zzz.sochi@gmail.com>"

ADD http://media.ticketscloud.s3.amazonaws.com/__deploy__/wkhtmltopdf /usr/local/bin/wkhtmltopdf
RUN chmod +x /usr/local/bin/wkhtmltopdf && apk add libstdc++ glib libxrender libssl1.0 libxext freetype fontconfig ttf-freefont ghostscript-fonts

ADD static/headers/* /srv/src/static/headers/
ADD setup.py /srv/src/setup.py
ADD tc_wkhtmltopdf /srv/src/tc_wkhtmltopdf

RUN pip3 install /srv/src

ENTRYPOINT ["/usr/local/bin/python3", "-m", "tc_wkhtmltopdf", "run", "--listen", "0.0.0.0:8080", "--exe-path", "/usr/local/bin/wkhtmltopdf"]