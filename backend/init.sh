# Ubuntu 18.04 minimal
# install zsh and ohmyzsh
sudo apt install zsh
sh -c "$(curl -fsSL https://raw.github.com/robbyrussell/oh-my-zsh/master/tools/install.sh)"
# install pip
sudo apt install python3-pip
# install nginx dependent libs: pcre and zlib
sudo apt install nginx
# build nginx with LibreSSL and optimizing params
## ref link: http://nginx.org/en/docs/configure.html
curl -O https://www.openssl.org/source/openssl-1.1.1.tar.gz
tar -zxf openssl-1.1.1.tar.gz
curl -O http://nginx.org/download/nginx-1.15.6.tar.gz
tar -zxf nginx-1.15.5.tar.gz
cd nginx-1.15.5
./configure --with-openssl=.../openssl-1.1.1 --with-file-aio --with-threads --with-cc-opt="-O3"
# install virtualenv
## ! only for current user
pip3 install virtualenv

# start virtualenv and install required package
virtualenv -p python env
source env/bin/activate
pip install -r requirements.txt

# build scala and spark on single VM
## install scala
curl -o scala-2.12.7.tar.gz https://codeload.github.com/scala/scala/tar.gz/v2.12.7
tar -zxf scala-2.12.7.tar.gz
export SCALA_HOME=/home/$USER/scala-2.12.7
export PATH=$PATH:$SCALA_HOME/bin
# install JDK
sudo apt install openjdk-11-jdk
## install spark
### go to this site and choose mirror https://www.apache.org/dyn/closer.lua/spark/spark-2.3.2/spark-2.3.2-bin-hadoop2.7.tgz
curl -O http://apache.mirror.vexxhost.com/spark/spark-2.3.2/spark-2.3.2-bin-hadoop2.7.tgz
tar -zxf spark-2.3.2-bin-hadoop2.7.tgz
### set the env params
export SPARK_HOME=/home/$USER/spark-2.3.2-bin-hadoop2.7
export PATH=$PATH:$SPARK_HOME/bin:$SPARK_HOME/sbin
# set hardlink python->python3
sudo ln /usr/bin/python3 /usr/bin/python

# install mongodb
sudo apt install mongodb
# install spark-mongodb connector
pyspark --packages org.mongodb.spark:mongo-spark-connector_2.11:2.3.1


