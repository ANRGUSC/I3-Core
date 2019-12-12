 FROM python:3.5
 ENV PYTHONUNBUFFERED 1
 RUN mkdir /code
 WORKDIR /code/
 ADD /frontend/requirements.txt /code/
 RUN pip install -r requirements.txt
 ADD . /code/
 RUN wget http://ftp.us.debian.org/debian/pool/main/g/glibc/multiarch-support_2.19-18+deb8u10_amd64.deb
 RUN dpkg -i multiarch-support_2.19-18+deb8u10_amd64.deb
 RUN wget http://ftp.us.debian.org/debian/pool/main/o/openssl/libssl1.0.0_1.0.1t-1+deb8u8_amd64.deb
 RUN dpkg -i libssl1.0.0_1.0.1t-1+deb8u8_amd64.deb
 RUN wget http://security.ubuntu.com/ubuntu/pool/main/c/c-ares/libc-ares2_1.10.0-2ubuntu0.2_amd64.deb
 RUN dpkg -i libc-ares2_1.10.0-2ubuntu0.2_amd64.deb
 WORKDIR /code/frontend/src/
