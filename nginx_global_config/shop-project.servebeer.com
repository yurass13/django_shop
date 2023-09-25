upstream app{
    server 127.0.0.1:8000;
}

server {
    listen 80;

    server_name shop-project.servebeer.com www.shop-project.servebeer.com;
    acess_log logs/shop-project.servebeer.access.log;
    charset utf-8;

    client_max_body_size 75M;

    location / {
        include proxy_params;

        proxy_pass http://app;

        proxy_redirect off;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
    }
}
