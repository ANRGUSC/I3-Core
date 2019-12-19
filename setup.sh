git clone https://github.com/ANRGUSC/iotm.git
if [ ! -d iotm ]; then
    echo "Error the git repository was not cloned"
fi

git clone https://github.com/ANRGUSC/I3-SDK.git
if [ ! -d I3-SDK ]; then
    echo "Error the git repository was not cloned"
fi

echo "Checking for docker."
sudo apt-get remove docker docker-engine docker.io containerd runc
sudo apt-get update

echo "Installing docker"
sudo apt-get install     apt-transport-https     ca-certificates     curl     gnupg-agent     software-properties-common

curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
sudo add-apt-repository    "deb [arch=amd64] https://download.docker.com/linux/ubuntu \
   $(lsb_release -cs) \
   stable"
sudo apt-get update
sudo apt-get install docker-ce docker-ce-cli containerd.io
sudo curl -L "https://github.com/docker/compose/releases/download/1.23.1/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
docker-compose --version

sudo apt-get python
sudo apt-get python-pip
pip install requests
pip install paho-mqtt