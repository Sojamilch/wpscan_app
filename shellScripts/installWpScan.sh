#!/bin/sh

sudo apt install ruby # Install Ruby

sudo apt-get install libcurl4-openssl-dev libxml2 libxml2-dev libxslt1-dev ruby-dev build-essential #install dependencies

sudo gem install wpscan # install wpscan to usr/local/bin/wpscan

wpscan --update #update to latest version of wpscan/check if install worked

wpwatcher --template_conf > wpwatcher.conf # Create config file 