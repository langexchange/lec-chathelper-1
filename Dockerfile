FROM httpd:2.4.55

# SOME CONFIGURATION
ENV TZ=Asia/Bangkok
RUN adduser --no-create-home langchat

# COPY ./public-html/ /usr/local/apache2/htdocs/
WORKDIR /usr/local/share

RUN echo "deb-src http://deb.debian.org/debian bullseye main" >> /etc/apt/sources.list

RUN apt-get update \ 
    && apt-get install -y --no-install-recommends \
    curl 

# Python dependencies
RUN apt-get -y build-dep python3 \
    && apt-get -y install pkg-config \
    zlib1g-dev \
    libffi-dev

# Install OpenSSL for pip
RUN curl -O https://www.openssl.org/source/old/3.1/openssl-3.1.0-alpha1.tar.gz \
    && tar xzf openssl-3.1.0-alpha1.tar.gz
WORKDIR ./openssl-3.1.0-alpha1
RUN ./config \
    --prefix=/usr/local/custom-openssl \
    --libdir=lib \
    --openssldir=/etc/ssl \
    && make -j1 depend \
    && make -j8 \
    && make install_sw

# Install python-3.10.10
WORKDIR ..
RUN curl https://www.python.org/ftp/python/3.10.10/Python-3.10.10.tgz --output Python-3.10.10.tgz \
    && tar -zxvf Python-3.10.10.tgz
  
WORKDIR /usr/local/share/Python-3.10.10

RUN ./configure -C \
    --enable-shared \
    --with-openssl=/usr/local/custom-openssl \
    --with-openssl-rpath=auto \
    && make \
    && make install

RUN echo "/usr/local/lib" >> /etc/ld.so.conf


## Apache dependencies
RUN apt-get -y install libaprutil1-dev \
    libapr1 \
    libapr1-dev
    # build-essential

## My deps
RUN apt-get -y install vim

# Building mod_wsgi
WORKDIR ..
RUN curl -L https://github.com/GrahamDumpleton/mod_wsgi/archive/refs/tags/4.9.4.tar.gz > mod_wsgi-4.9.4.tgz
RUN tar -zxvf mod_wsgi-4.9.4.tgz
WORKDIR ./mod_wsgi-4.9.4

RUN ./configure --with-python=/usr/local/bin/python3 \
    && make \
    && make install \
    && make clean

# Update pip3
RUN pip3 install --no-cache-dir --upgrade pip



## Build dependencies for application
COPY --chown=:langchat ./lec_chathelper /usr/local/src/lec_chathelper
RUN pip3 install --no-cache-dir -r /usr/local/src/lec_chathelper/requirements.txt
WORKDIR /usr/local/apache2

## CELERY CONFIG
COPY --chown=:langchat ./lec_chathelper/chat/chatworker/conf/celeryd.default /etc/default/celeryd
RUN chmod 640 /etc/default/celeryd
COPY --chown=:langchat ./lec_chathelper/chat/chatworker/conf/celeryd.init /etc/init.d/celeryd
RUN mkdir -p /var/run/celery /var/log/celery
RUN chown langchat:langchat /var/run/celery /var/log/celery
RUN chmod 701 /root


COPY --chown=:langweb ./conf/hello.conf /usr/local/apache2/conf/httpd.conf

CMD ["httpd","-D","FOREGROUND"]
# RUN apachectl start
# ENTRYPOINT ["apachectl", "start"]
# CMD ["-c", "python manage.py runserver 0.0.0.0:8000"]