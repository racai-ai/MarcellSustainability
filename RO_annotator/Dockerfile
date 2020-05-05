FROM ubuntu:18.04 as intermediate
LABEL stage=intermediate
ARG DEBIAN_FRONTEND=noninteractive
RUN apt-get update && \
    apt-get install -y git wget curl make automake autoconf gcc g++ flex bison
RUN mkdir ner
RUN wget http://relate.racai.ro/resources/ner/ner.tar.bz2 -O /ner.tar.bz2 && tar -jxf ner.tar.bz2
RUN wget http://relate.racai.ro/resources/ner/COROLA.vectors.gz -O /ner/COROLA.vectors.gz && gunzip /ner/COROLA.vectors.gz
RUN wget http://relate.racai.ro/resources/ner/COROLA.words.gz -O /ner/COROLA.words.gz && gunzip /ner/COROLA.words.gz
RUN wget http://relate.racai.ro/resources/ner/combined_ctag.clean.PERLOCORG.4.ser.gz -O /ner/combined_ctag.clean.PERLOCORG.4.ser.gz
RUN wget http://relate.racai.ro/resources/ner/jdk1.8.0_191.tar.bz2 -O /ner/jdk1.8.0_191.tar.bz2 && tar -C /ner -jxf /ner/jdk1.8.0_191.tar.bz2 && rm -f /ner/jdk1.8.0_191.tar.bz2
RUN wget http://relate.racai.ro/resources/ner/stanford-ner-2018-10-16-mod.tar.bz2 -O /ner/stanford-ner-2018-10-16-mod.tar.bz2 && tar -C /ner -jxf /ner/stanford-ner-2018-10-16-mod.tar.bz2 && rm -f /ner/stanford-ner-2018-10-16-mod.tar.bz2
RUN wget http://relate.racai.ro/resources/ner/web.tar.bz2 -O /ner/web.tar.bz2 && tar -C /ner -jxf /ner/web.tar.bz2 && rm -f /ner/web.tar.bz2
RUN wget http://relate.racai.ro/resources/ner/fasttext-0.1.0-mod.tar.bz2 -O /ner/fasttext-0.1.0-mod.tar.bz2 && tar -C /ner -jxf /ner/fasttext-0.1.0-mod.tar.bz2 && rm -f /ner/fasttext-0.1.0-mod.tar.bz2
RUN cd /ner/fastText-0.1.0-mod && make fasttext && cd /
RUN wget http://relate.racai.ro/resources/ner/corola.300.20.5.bin -O /ner/corola.300.20.5.bin
RUN git clone https://github.com/racai-ai/IATE-EUROVOC-Annotator.git /ner/IATE-EUROVOC-Annotator-build
RUN cd /ner/IATE-EUROVOC-Annotator-build/src && make all && cd /
RUN mkdir /ner/IATE-EUROVOC-Annotator
RUN cp /ner/IATE-EUROVOC-Annotator-build/src/annotate /ner/IATE-EUROVOC-Annotator
RUN cp -r /ner/IATE-EUROVOC-Annotator-build/resources /ner/IATE-EUROVOC-Annotator
RUN rm -fr /ner/IATE-EUROVOC-Annotator-build
# Install Perl CPAN packages for NLPipe
# Install Perl5 only if it's not installed (it usually is)
RUN command -v perl >/dev/null || apt-get install -y perl
# Needed by BerkeleyDB Perl module (development only)
RUN apt-get update && apt-get install -y libdb5.3++-dev libdb5.3-dev zip unzip gpg makepatch libconfig-yaml-perl
RUN mkdir -p /root/.cpan/CPAN
RUN mkdir -p /root/perl
# Copy already configured (by Radu) CPAN .pm file
COPY docker/MyConfig.pm /root/.cpan/CPAN
RUN cpan -i Unicode::String
RUN cpan -i Algorithm::Diff
RUN cpan -i BerkeleyDB
RUN cpan -i File::Which
RUN cpan -i File::HomeDir
# Copy NLPipe resources
RUN wget http://relate.racai.ro/resources/nlpipe/nlpipe-resources.tar.gz -O /root/nlpipe-resources.tar.gz && \
    tar -C /root -xzvf /root/nlpipe-resources.tar.gz && rm -fv /root/nlpipe-resources.tar.gz
# End NLPipe install stuff

FROM ubuntu:18.04
ARG DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y cron zip unzip apache2 php7.2 libapache2-mod-php7.2 curl php7.2-mbstring php7.2-curl
RUN mkdir -p /var/www/site && a2enmod php7.2 && a2enmod rewrite
COPY --from=intermediate /ner/ /ner/
COPY --from=intermediate /ner/web/ /var/www/site/
COPY annotate/ /var/www/site/
RUN chmod a+rw /var/www/site/corrector
# Stuff for NLPipe platform (run-time)
# Install Perl5 only if it's not installed (it usually is)
RUN command -v perl >/dev/null || apt-get install -y perl
# Needed by BerkeleyDB Perl module; also add Python 3 into the mix
RUN apt-get update && apt-get install -y libdb5.3 libdb5.3++ python3.6 python3-pip
RUN mkdir /root/perl
RUN mkdir /root/.nlpipe
COPY --from=intermediate /root/perl/ /root/perl/
COPY --from=intermediate /root/.nlpipe/ /root/.nlpipe/
# These are the NLPipe Python 3.6 dependencies
RUN pip3 install nlpcube
RUN pip3 install filelock
RUN pip3 install flask
RUN pip3 install flask-restful
RUN pip3 install uwsgi
RUN pip3 install pytest
RUN mkdir /root/nlpipe
COPY nlpipe/ /root/nlpipe/
RUN cd /root/nlpipe && chmod a+rx *.sh && cd /
# These should PASS, othewise the build has to fail
COPY docker/perl-check-install.sh /root/
RUN chmod a+rx /root/perl-check-install.sh && /root/perl-check-install.sh
RUN cd /root/nlpipe && pytest -v tests && cd /
# End stuff for NLPipe platform

RUN sed -i "s/error_reporting = .*$/error_reporting = E_ERROR | E_WARNING | E_PARSE/" /etc/php/7.2/apache2/php.ini

ENV APACHE_RUN_USER www-data
ENV APACHE_RUN_GROUP www-data
ENV APACHE_LOG_DIR /var/log/apache2
ENV APACHE_LOCK_DIR /var/lock/apache2
ENV APACHE_PID_FILE /var/run/apache2.pid

ADD docker/apache-config.conf /etc/apache2/sites-enabled/000-default.conf

COPY docker/entrypoint.sh /
RUN chmod a+rx /entrypoint.sh
#COPY docker/tasks.cron /etc/cron.d/
#RUN chmod 0644 /etc/cron.d/tasks.cron
#RUN crontab /etc/cron.d/tasks.cron
#RUN touch /var/log/cron.log

CMD ["/entrypoint.sh"]
