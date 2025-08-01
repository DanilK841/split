FROM python:3.9.5

WORKDIR /split

COPY split/req.txt req.txt

RUN pip install --upgrade pip
RUN pip install -r req.txt

COPY split .

# Collect static files
RUN python manage.py collectstatic --noinput
