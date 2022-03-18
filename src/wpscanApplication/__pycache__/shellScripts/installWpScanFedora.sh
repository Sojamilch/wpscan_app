#!/bin/sh

sudo dnf install ruby # Install Ruby

sudo dnf group install "Development Tools" 
sudo dnf install git gcc ruby-devel libxml2 libxml2-devel libxslt libxslt-devel libcurl-devel patch rpm-build #install dependencies

sudo gem install wpscan # install wpscan to usr/local/bin/wpscan

wpscan --update #update to latest version of wpscan/check if install worked

pip install wpwatcher #install the wpwatcher opensource plugin that auto formats emails/pdfs etc.

wpwatcher --template_conf > wpwatcher.conf # Create config file 
