FROM nginx:alpine
# Copy the entire site so login and registration pages are available
COPY . /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
