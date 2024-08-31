FROM amd64/fedora:42

RUN dnf update -y \
	&& dnf install -y \
	python3 \
	python3-pip \
	#su \
	&& dnf clean all

# Set user and group
ARG user=demo
ARG group=demo
ARG uid=1000
ARG gid=1000

RUN groupadd -g ${gid} ${group}
RUN useradd -u ${uid} -g ${group} -s /bin/sh -m ${user} # <--- the '-m' create a user home directory
USER ${uid}:${gid}

# install python modules
RUN pip3 install requests
WORKDIR ${user}

ARG REPOSITORY_LIST_URL
ENV REPOSITORY_LIST_URL $REPOSITORY_LIST_URL

ADD parser.py ./
ADD script.sh ./

CMD ["/bin/sh", "-c", "export"]
ENTRYPOINT ["./script.sh"]
	