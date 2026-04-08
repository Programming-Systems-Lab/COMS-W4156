#!/bin/bash

sudo apt-get update
sudo apt-get install -y build-essential openjdk-7-jre openjdk-7-jdk vim git zip wget

wget http://downloads.typesafe.com/typesafe-activator/1.2.10/typesafe-activator-1.2.10-minimal.zip
unzip typesafe-activator-1.2.10-minimal.zip
chown -R vagrant:vagrant activator-1.2.10-minimal/
echo "PATH=/home/vagrant/activator-1.2.10-minimal/:$PATH" >> /home/vagrant/.bashrc
