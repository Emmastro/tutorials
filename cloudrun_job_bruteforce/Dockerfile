FROM kalilinux/kali-bleeding-edge

RUN apt-get update && apt-get install -y python3-pip

RUN apt-get update -y 

RUN apt-get install -y john

COPY . .

RUN pip3 install -r requirements.lock.txt

CMD ["python3", "main.py"]