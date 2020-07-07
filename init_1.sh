sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt update && sudo apt install python3.6
rm /usr/bin/python3
ln -sf /usr/bin/python3.6 /usr/bin/python3
rm /usr/bin/pydoc3
ln -sf /usr/bin/pydoc3.6 /usr/bin/pydoc3

sudo wget https://bootstrap.pypa.io/ez_setup.py -O - | python3
sudo pip3 install --force-reinstall setuptools

sudo pip3 install django==2.1
sudo pip3 install gunicorn==19.5
sudo pip3 install mysqlclient
