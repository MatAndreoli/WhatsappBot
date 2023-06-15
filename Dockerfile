FROM debian:stable-slim

USER root
RUN rm /bin/sh && ln -s /bin/bash /bin/sh

RUN echo "fksd"
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    python3-pip \
    git \
    npm

RUN curl -LO  https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
RUN apt-get install -y ./google-chrome-stable_current_amd64.deb
RUN rm google-chrome-stable_current_amd64.deb
RUN echo "Chrome: " && google-chrome --version

ENV NVM_DIR /usr/local/nvm
ENV NODE_VERSION 18.13.0
RUN curl -o- https://raw.githubusercontent.com/creationix/nvm/v0.31.2/install.sh | bash
RUN source $NVM_DIR/nvm.sh \
    && nvm install $NODE_VERSION \
    && nvm alias default $NODE_VERSION \
    && nvm use default

ENV NODE_PATH $NVM_DIR/versions/node/v$NODE_VERSION/lib/node_modules
ENV PATH $NVM_DIR/versions/node/v$NODE_VERSION/bin:$PATH


RUN pip install virtualenv --break-system-packages
ENV VIRTUAL_ENV=venv

WORKDIR /app

RUN virtualenv -p python3.11 ${VIRTUAL_ENV}
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

COPY package.json .
COPY package-lock.json .
RUN npm install

COPY requirements.txt .
RUN ${VIRTUAL_ENV}/bin/pip install -r requirements.txt

COPY . .

CMD [ "bash", "run_all.sh" ]
