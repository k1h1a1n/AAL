FROM tryton/tryton:5.8

USER root

RUN pip3 install xlsxwriter

COPY /modules/ /usr/local/lib/python3.7/dist-packages/trytond/modules

COPY sao/www /var/lib/trytond/www

USER root

