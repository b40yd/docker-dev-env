FROM nginx:latest
COPY ../repos/debian.list /etc/apt/sources.list.d/debian.list
RUN apt-get update -y
RUN apt install -y apt-transport-https ca-certificates
RUN apt-get install -y curl procps net-tools vim
RUN bash -c "$(curl -L https://setup.vector.dev)"
RUN apt-get install -y vector
RUN rm -rf /var/log/nginx/*.log