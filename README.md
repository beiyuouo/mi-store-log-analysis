# mi-store-log-analysis

BigData Project

## How to use
0. Prerequire

- Hadoop
- Flume
- Zookeeper
- Kafka
- Storm
- Nginx
- Nodejs

1. 启动前端
```sh
cd mi-store-fn
npm install
npm run serve
```

2. 配置并启动后端
```sh
cd mi-store-bn
mysql -uroot -p<password> < storeDB.sql
mysql -uroot -p<password> -DstoreDB < analogDataSql.sql
node app.js
```

3. 配置Nginx
```sh

#user  nobody;
worker_processes  1;

#error_log  logs/error.log;
#error_log  logs/error.log  notice;
#error_log  logs/error.log  info;

pid        logs/nginx.pid;


events {
    worker_connections  1024;
}


http {
    include       mime.types;
    default_type  application/octet-stream;

    log_format  main  '$remote_addr - $remote_user [$time_local] "$request" '
                      '$status $body_bytes_sent "$http_referer" '
                      '"$http_user_agent" "$http_x_forwarded_for"';

    access_log  /var/log/nginx/access.log  main;

    sendfile        on;
    #tcp_nopush     on;

    #keepalive_timeout  0;
    keepalive_timeout  65;

    #gzip  on;

    server {
        listen       80;
        server_name  localhost;

        #charset koi8-r;

        #access_log  logs/host.access.log  main;

        location / {
            proxy_pass http://localhost:8080;
            # root   html;
            # index  index.html index.htm;
        }
        #error_page  404              /404.html;

        # redirect server error pages to the static page /50x.html
        #
        error_page   500 502 503 504  /50x.html;
        location = /50x.html {
            root   html;
        }

        # proxy the PHP scripts to Apache listening on 127.0.0.1:80
        #
        #location ~ \.php$ {
        #    proxy_pass   http://127.0.0.1;
        #}

        # pass the PHP scripts to FastCGI server listening on 127.0.0.1:9000
        #
        #location ~ \.php$ {
        #    root           html;
        #    fastcgi_pass   127.0.0.1:9000;
        #    fastcgi_index  index.php;
        #    fastcgi_param  SCRIPT_FILENAME  /scripts$fastcgi_script_name;
        #    include        fastcgi_params;
        #}

        # deny access to .htaccess files, if Apache's document root
        # concurs with nginx's one
        #
        #location ~ /\.ht {
        #    deny  all;
        #}
    }


    # another virtual host using mix of IP-, name-, and port-based configuration
    #
    #server {
    #    listen       8000;
    #    listen       somename:8080;
    #    server_name  somename  alias  another.alias;

    #    location / {
    #        root   html;
    #        index  index.html index.htm;
    #    }
    #}


    # HTTPS server
    #
    #server {
    #    listen       443 ssl;
    #    server_name  localhost;

    #    ssl_certificate      cert.pem;
    #    ssl_certificate_key  cert.key;

    #    ssl_session_cache    shared:SSL:1m;
    #    ssl_session_timeout  5m;

    #    ssl_ciphers  HIGH:!aNULL:!MD5;
    #    ssl_prefer_server_ciphers  on;

    #    location / {
    #        root   html;
    #        index  index.html index.htm;
    #    }
    #}

}

```


4. 配置并启动Kafka
```sh
# 启动kafka内置zookeeper
bin/zookeeper-server-start.sh config/zookeeper.properties
# 启动kafka
bin/kafka-server-start.sh config/server.properties
```
5. 配置并启动Flume

```sh[nginx-kafka.conf]
# Name the components on this agent
a1.sources = r1
a1.sinks = k1
a1.channels = c1

# Describe/configure the source
a1.sources.r1.type = exec
a1.sources.r1.command = tail -F /var/log/nginx/access.log

# Describe the sink
a1.sinks.k1.channel = c1
a1.sinks.k1.type = org.apache.flume.sink.kafka.KafkaSink
a1.sinks.k1.kafka.topic = test
a1.sinks.k1.kafka.bootstrap.servers = localhost:9092
a1.sinks.k1.kafka.flumeBatchSize = 2
a1.sinks.k1.kafka.producer.acks = 1
a1.sinks.k1.kafka.producer.linger.ms = 1
a1.sinks.k1.kafka.producer.compression.type = snappy

# Use a channel which buffers events in memory
a1.channels.c1.type = memory
a1.channels.c1.capacity = 1000
a1.channels.c1.transactionCapacity = 100

# Bind the source and sink to the channel
a1.sources.r1.channels = c1
a1.sinks.k1.channel = c1
```

启动Flume
```sh
flume-ng agent -c conf/ -f conf/nginx-kafka.conf -n a1
```

可以启动kafka消费者来看一下`test`话题中的内容
```sh
bin/kafka-console-customer.sh --topic test --bootstrap-server localhost:9092
```

6. 启动Spark消费Kafka数据并进行可视化

```sh
# 启动Hadoop保存checkpoint
bin/start-dfs.sh

# 提交Spark
spark-submit
    --master local[*] \
    --jars file:///opt/pkg/spark/jars/org.apache.commons_commons-pool2-2.6.2.jar,file:///opt/pkg/spark/jars/org.apache.kafka_kafka-clients-2.4.1.jar,file:///opt/pkg/spark/jars/mysql-connector-java-8.0.21.jar,file:///opt/pkg/spark/jars/spark-sql-kafka-0-10_2.12-3.0.1.jar,file:///opt/pkg/spark/jars/spark-token-provider-kafka-0-10_2.12-3.0.1.jar \
    file:///opt/pkg/spark/kafka/kafka_mysql.py
```

7. 启动数据可视化前端
```sh
python app.py
```

8. Windows端口映射
```sh
# 查看端口映射
netsh interface portproxy show v4tov4

# 添加端口映射
netsh interface portproxy add v4tov4 listenport=3090 listenaddress=192.168.0.106 connectaddress=192.168.186.100 connectport=80

# 删除端口映射
netsh interface portproxy delete v4tov4 listenport=3090 listenaddress=192.168.0.106


```


## 其他解决方案和软件安装
```sh
# Build log analysis workflow
# Copy dist/GeoLite2-City.mmdb to anywhere you like, and config it in log-analysis-workflow/src/main/resources/application.properties

# Download and install redis
wget https://download.redis.io/releases/redis-6.2.6.tar.gz
tar xzf redis-6.2.6.tar.gz
cd redis-6.2.6
make && make test && make install

# Lanuch redis server and client
nohup ./redis-server &
./redis-cli

# Test redis
127.0.0.1:6379> ping

# Also, you need to config redis and access.log in application.properties


# Visualization
# https://www.vultr.com/docs/how-to-install-goaccess-on-centos-7
sudo goaccess /var/log/nginx/access.log --log-format=COMBINED -a -o /var/www/html/report.html
```

# Reference
- https://github.com/fenlan/storm-nginx-log
- https://github.com/hai-27/store-server
- https://github.com/hai-27/vue-store
- https://github.com/allinurl/goaccess
- https://www.vultr.com/docs/how-to-install-goaccess-on-centos-7
- https://github.com/TurboWay/bigdata_practicese
- https://github.com/debatosh99/pyspark-kafka-mysql