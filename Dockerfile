FROM amd64/fedora:42

RUN dnf install -y \
	python3 \
	python3-pip \
	su \
	&& dnf clean all

# Set user and group
#ARG user=demo
#ARG group=demo
#ARG uid=1000
#ARG gid=1000
#RUN groupadd -g ${gid} ${group}
#RUN useradd -u ${uid} -g ${group} -s /bin/sh -m ${user} # <--- the '-m' create a user home directory

# creating user demo, usergroup(-G) demo, no home dir(-H), no password(-D)
#RUN groupadd demo && useradd demo -g demo -p demo
#USER ${uid}:${gid}

RUN pip install requests
RUN mkdir /srv/gitreposparser
WORKDIR /srv/gitreposparser
ADD parser.py ./

CMD ["bash"]
	