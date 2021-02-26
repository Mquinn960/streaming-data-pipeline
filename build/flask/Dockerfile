FROM python:3.6
RUN mkdir /var/api/
COPY ./resources/requirements.txt /var/api/
WORKDIR /var/api/
EXPOSE 5000
RUN pip install -r requirements.txt
CMD ["python", "server.py"]
