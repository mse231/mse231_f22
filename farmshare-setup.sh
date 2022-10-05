cd ~
wget https://github.com/openssl/openssl/archive/refs/tags/OpenSSL_1_1_1q.tar.gz
wget https://www.python.org/ftp/python/3.10.7/Python-3.10.7.tgz
tar -xvzf OpenSSL_1_1_1q.tar.gz
tar -xvzf Python-3.10.7.tgz
mkdir local
cd openssl-OpenSSL_1_1_1q 
./config --prefix=$HOME/local/openssl --openssldir=$HOME/local/openssl
make -j1 depend
make -j8
make install_sw 
cd ~/Python-3.10.7
./configure -C --with-openssl=$HOME/local/openssl --with-openssl-rpath=auto --prefix=$HOME/local/python-3.10.7 --enable-optimizations
make -j8
make altinstall
ln -s $HOME/local/python-3.10.7/bin/python3.10 $HOME/local/python-3.10.7/bin/python
ln -s $HOME/local/python-3.10.7/bin/python3.10 $HOME/local/python-3.10.7/bin/python3
ln -s $HOME/local/python-3.10.7/bin/pip3.10 $HOME/local/python-3.10.7/bin/pip
ln -s $HOME/local/python-3.10.7/bin/pip3.10 $HOME/local/python-3.10.7/bin/pip3
cd ~
echo 'PATH="$HOME/local/python-3.10.7/bin:$PATH"' >> ~/.profile
source ~/.profile
pip install --user tweepy
rm -rf Python-3.10.7.tgz
rm -rf Python-3.10.7
rm -rf OpenSSL_1_1_1q.tar.gz
rm -rf openssl-OpenSSL_1_1_1q
echo "DONE"
