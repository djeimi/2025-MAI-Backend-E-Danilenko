FROM ubuntu:25.04
ADD . /wholeProject
RUN apt-get update
RUN apt-get install -y python3 python3-pip
RUN pip3 install --break-system-package "psycopg[binary,pool]"
RUN pip3 install --break-system-package -r /wholeProject/requirements.txt 
EXPOSE 8000
USER nobody
WORKDIR /wholeProject
CMD /usr/local/bin/gunicorn crochetProject.wsgi --bind 0.0.0.0:8000