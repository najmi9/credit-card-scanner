FROM python:3.11

WORKDIR /src/app

COPY . .

RUN python3 -m pip install --upgrade pip
RUN pip install -r requirements.txt

RUN apt update && apt install -y tesseract-ocr && apt install -y libmagic1

RUN apt update && apt install -y libgl1-mesa-glx

EXPOSE 7000

CMD [ "python", "server.py", "--reload" ]
