# FROM gunicorn:20.0.4
FROM python:3.8-slim

# パッケージのインストール
RUN apt-get update && apt-get install -y \
    tzdata vim \
    libmagic1 \
 && rm -rf /var/lib/apt/lists/*

# モジュールのインストール
WORKDIR /tmp/work
COPY requirements.txt ${PWD}
RUN pip3 install -r requirements.txt

# 環境変数の定義
ENV TZ=Asia/Tokyo
ENV USER user1

# # 一般権限のユーザーを追加
# RUN useradd -m ${USER} --uid 1000
# RUN gpasswd -a ${USER} sudo
# RUN echo "${USER}:password" | chpasswd

# # ユーザーの切替
# USER ${USER}

# CMD cd /home/user1/dev && gunicorn myprj.wsgi --bind=unix:/var/run/gunicorn/gunicorn.sock