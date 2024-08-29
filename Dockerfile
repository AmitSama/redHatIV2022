FROM amd64/fedora:42

RUN dnf install -y \
	python3 \
	python3-pip \
#	/usr/bin/randomusr/ \
	&& dnf clean all

CMD ["bash"]
	