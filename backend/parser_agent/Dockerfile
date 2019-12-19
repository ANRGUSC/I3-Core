 FROM python:2.7
 ENV PYTHONUNBUFFERED 1
 RUN mkdir /code
 WORKDIR /code/
 ADD ./config.ini /code/
 ADD ./backend/parser_agent/ /code/
 RUN pip install -r requirements.txt
 CMD ["python","/code/parser_agent.py"]