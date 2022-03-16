FROM "ubuntu:20.04"

RUN set -eux; \
    apt-get -yq update; \
    apt-get -yq install software-properties-common; \
    add-apt-repository -y ppa:deadsnakes/ppa; \
    apt-get -yq update; \
    apt-get -yq install python3.10 python3-pip python3.10-distutils default-jre jhove