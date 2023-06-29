#Base Images
FROM ubuntu:latest

# nginx unstall
RUN apt -y update && apt -y upgrade
RUN apt -y install nginx
RUN echo "\ndaemon off;" >> /etc/nginx/nginx.conf
RUN chown -R www-data:www-data /var/lib/nginx

VOLUME ["/data", "/etc/nginx-site-enabled", "/var/log/nginx"]

WORKDIR /etc/nginx

# port
EXPOSE 80
EXPOSE 443

# server execution
CMD ["nginx"]