FROM ubuntu:24.04
ENV DEBIAN_FRONTEND=noninteractive

RUN sed -i "s@archive.ubuntu.com@teach.giize.com/mirrors@g" /etc/apt/sources.list.d/ubuntu.sources && \
    sed -i "s@security.ubuntu.com@teach.giize.com/mirrors@g" /etc/apt/sources.list.d/ubuntu.sources && \
    apt-get update && \
    apt-get install -y \
    python3 \
    python3-pip \
    python3-venv \
    pkg-config \
    libmysqlclient-dev && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN python3 -m venv /venv
ENV PATH="/venv/bin:$PATH"



COPY requirements.txt .
COPY --chmod=644 pip.conf /etc/
RUN  pip install -r requirements.txt

COPY . .

ENV PYTHONPATH=/opt/myblog/
ENTRYPOINT ["python3", "main.py"]