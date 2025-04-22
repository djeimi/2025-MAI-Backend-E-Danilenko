FROM python:3.13  
RUN mkdir /wholeProject
WORKDIR /wholeProject
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1 
RUN pip install --upgrade pip 
COPY requirements.txt  /wholeProject/
RUN pip install --no-cache-dir -r requirements.txt
COPY . /wholeProject/
RUN python manage.py collectstatic
EXPOSE 8000
CMD ["sh", "-c", "python manage.py migrate --noinput && gunicorn crochetProject.wsgi --bind 0.0.0.0:8000"]
