sudo easy_install pip
sudo pip install virtualenv
virtualenv --no-site-packages ~/envs/hub-ology
source ~/envs/hub-ology/bin/activate
pip install networkx
pip install numpy 
pip install -e git+https://github.com/matplotlib/matplotlib.git#egg=matplotlib
pip install PIL
pip install geopy
