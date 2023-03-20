FROM python:3
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /spa
EXPOSE 8000
WORKDIR /spa

#COPY ./requirements.txt /spa/
COPY . /spa

RUN pip3 install -r requirements.txt --no-cache-dir

#FROM python:3
#EXPOSE 8000
#WORKDIR /spa

#COPY ./requirements.txt /spa/

#RUN pip3 install -r requirements.txt --no-cache-dir


#ENTRYPOINT ["python3"]
#CMD ["manage.py", "runserver", "0.0.0.0:8088"]



#Copy . .
#/home/andrey_mazo/PycharmProjects/DjangoProject5ViewSetGeneric/: .


#RUN pip freeze > requirements.txt 
#/spa
#COPY --chown=/home/andrey_mazo/PycharmProjects/DjangoProject5ViewSetGeneric/requirements.txt:/spa 
#Copy /home/andrey_mazo/PycharmProjects/DjangoProject5ViewSetGeneric/ .
#/home/andrey_mazo/lssn1docker/
#/root/DjangoProject5ViewSetGeneric
#WORKDIR /spa/DjangoProject5ViewSetGeneric

#RUN ["pip3", "install", "-r", "requirements.txt"]
#run cat requirements.txt

#WORKDIR /spa
#/DjangoProject5ViewSetGeneric
#EXPOSE 8000
# ENTRYPOINT ["python3"]

#ADD https://raw.githubusercontent.com/discdiver/pachy-vid/master/sample_vids/vid1.mp4 \
#/my_app_directory
#RUN ["pip3", "install", "-r", "requirements.txt"]
#ENTRYPOINT ["python3"]

# /home/andrey_mazo/PycharmProjects/DjangoProject5ViewSetGeneric/requirements.txt
#["pip3 install -r requirements.txt"]

#CMD ["manage.py", "runserver", "0.0.0.0:8088"]


#CMD python3 ./manage.py runserver 0.0.0.0:8000
#./manage.py", "runserver"]

