FROM nginx:alpine

# Copy index.html as a template
COPY index.html /usr/share/nginx/html/index.template.html

# Expose port 80
EXPOSE 80

# Replace BACKEND_URL placeholder and set Nginx to listen on $PORT instead of 80
CMD ["/bin/sh", "-c", "sed -e \"s|__BACKEND_URL_PLACEHOLDER__|${BACKEND_URL}|g\" /usr/share/nginx/html/index.template.html > /usr/share/nginx/html/index.html && sed -i -e 's/listen  *80;/listen '\"${PORT:-8080}\"';/g' /etc/nginx/conf.d/default.conf && exec nginx -g 'daemon off;'"]
