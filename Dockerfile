FROM josejuansanchez/kakadu:latest

RUN apt-get update && apt-get install -y curl libglu1-mesa cron proj-bin gdal-bin libpq-dev python3 python3-pip 

RUN cd ../

ADD . .

RUN python3 -m pip install --upgrade pip
RUN pip install --upgrade setuptools
RUN pip3 install -r requirements.txt

# ENTRYPOINT ["python3", "bdd/create_database.py"]
ENTRYPOINT ["/bin/bash", "./bdd/docker-entrypoint.sh"]

# CMD ["python3", "run_prod.py"]