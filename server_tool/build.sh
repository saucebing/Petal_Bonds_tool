#!/bin/bash
# Open the UDP 8777 port in Tencent Web Console

#nonapi:
# scp server executable to /server/game
mkdir -p /server/game
mkdir -p /server/api
cp tcg.service /etc/systemd/system/
systemctl start tcg

#api nohttps:
# scp files in TCGEngineAPI dir which is decompressed from TCGEngineAPI.zip to /server/api/
# yum -y install mongodb-org
# systemctl start mongod
# yum -y install nodejs npm
# cd /server/api
# npm install
# npm install forever -g
# npm audit fix --force
# forever start --uid tcgapi -a server.js 
# forever list # forever restart tcgapi # forever stop tcgapi

#api https:
#register a domain name
# yum install -y snapd
# systemctl start snapd
# snap install core
# # Open a new terminal session
# snap refresh core
# snap install --classic certbot
# ln -s /var/lib/snapd/snap /snap
# snap install --classic certbot
# ln -s /snap/bin/certbot /usr/bin/certbot

# yum install perl-ExtUtils-MakeMaker
# wget https://www.kernel.org/pub/software/scm/git/git-2.7.0.tar.gz
# yum -y groupinstall Development
# ./configure --prefix=/usr/local/git --with-perl=/bin/perl
# yum install zlib-devel
# make all -j
# make install -j
# #update PATH and LD_LIBRARY_PATH

# wget --no-check-certificate https://curl.haxx.se/download/curl-7.80.0.tar.gz
# yum -y install openssl
# ./configure --prefix=/usr/local --with-ssl
# make -j
# make install -j
# ldconfig
# certbot certonly --standalone -d petalbonds.top
# ls /etc/letsencrypt/live/petalbonds.top

# email:
# # modify config.js:
# smtp_enabled: true,
# smtp_name: "PetalBonds Support",    //Name of sender in emails
# smtp_email: "petalbonds@163.com",           //Email used to send
# smtp_server: "smtp.163.com",          //SMTP server URL
# smtp_port: "465",
# smtp_user: "petalbonds@163.com",            //SMTP auth user
# smtp_password: "APYDOSTDPDUOEEHQ",        //SMTP auth password
