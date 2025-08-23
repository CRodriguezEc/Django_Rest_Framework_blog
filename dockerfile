FROM python:3.9

#   Install SSH Client
#   Actualizamos el repositorio e instalamos el cliente SSH
RUN apt-get update && apt-get install -y openssh-client

#
#   Set environments variables
#   Esto desactiva el que los contenidos de salida o errores que genere el aplicativo 
#   se almacenen en memoria, previa visualizacion al usuario. 
#   
ENV PYTHONUNBUFFERED 1

#   Set the working directory
#   Se determina el directorio de trabajo del aplicativo
WORKDIR /app

#   Copy requirements.txt file
COPY requirements.txt /app/requirements.txt

#   Install python dependencies
RUN pip install -r requirements.txt

#   Copy the application to the working directory
#   Copiamos toda la aplicacion al directorio de trabajo creado
COPY . /app

#   Start the SSH tunnel
CMD python manage.py runserver 0.0.0.0:8081





