# base image
FROM python:3.11

# specify working directory
WORKDIR /code

# copy package list
COPY ./requirements.txt /code/requirements.txt

# install packages
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# copy application code
COPY ./app /code/app

# copy pretrained models
COPY .cvlib /root/.cvlib

# expose port
EXPOSE 80

# run server
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]