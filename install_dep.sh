#! /bin/bash

#Instalação de dependências
VERSION=1.11.4 
OS=linux 
ARCH=amd64
CURRDIR=$(pwd)
GOPATH=${HOME}/go
PATH=/usr/local/go/bin:${PATH}:${GOPATH}/bin
while [ "x$(sudo lsof /var/lib/dpkg/lock-frontend)" != "x" ] ; do
    sleep 30
done
sudo apt install -y gccgo-go
sudo DEBIAN_FRONTEND=noninteractive apt-get update -qy && \
	sudo DEBIAN_FRONTEND=noninteractive apt-get install -qy build-essential \
	libssl-dev uuid-dev libgpgme11-dev libseccomp-dev pkg-config squashfs-tools && \
	wget -O /tmp/go${VERSION}.${OS}-${ARCH}.tar.gz https://dl.google.com/go/go${VERSION}.${OS}-${ARCH}.tar.gz && \
	sudo tar -C /usr/local -xzf /tmp/go${VERSION}.${OS}-${ARCH}.tar.gz 
curl -sfL https://install.goreleaser.com/github.com/golangci/golangci-lint.sh | sh -s -- -b $(go env GOPATH)/bin v1.15.0
#Download da base de dados e preparação do código
echo "Baixando base de dados"
sudo apt-get install -y unzip
mkdir dynamic_stall_data 
cd dynamic_stall_data
wget --no-check-certificate "https://onedrive.live.com/download?cid=68B743CBCE8A14C0&resid=68B743CBCE8A14C0%21107533&authkey=AIRCWrGDBz471sE" 
mv * qSpanAvg.cgns 
cd ..
cd ROM_code-paramout-iteration/
#echo "Modificando arquivos para executar codigo"
sed -i '1s#/home/cfd/Desktop/hugo/#'"$CURRDIR"'/#' code/inputs.inp
sed -i '3s#/home/cfd/Desktop/hugo/ROM_code#'"$CURRDIR"'/#' code/inputs.inp
echo Instalando imagem do container
if [ $1 == "cpu" ]; then
	sed -i 's/tensorflow-gpu/tensorflow/' dnn_rom.def
fi
sudo apt-get update
sudo apt-get install -y software-properties-common python3
#sudo add-apt-repository ppa:jonathonf/python-3.6
sudo apt-get update
sudo apt-get install -y python3.6 time
sudo update-alternatives --install /usr/bin/python python /usr/bin/python3.6 1
sudo update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.6 1
sudo update-alternatives --set python /usr/bin/python3.6
sudo update-alternatives --set python3 /usr/bin/python3.6
sudo apt-get install -y wget 
sudo curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
python get-pip.py
sudo rm -f get-pip.py
sudo apt-get install -y python3.6-dev gcc g++ gfortran 
python3.6 -m pip install numpy matplotlib scipy Cython scikit-optimize 
python3.6 -m pip install tensorflow-gpu
python3.6 -m pip install smt
sudo wget https://support.hdfgroup.org/ftp/HDF5/releases/hdf5-1.10/hdf5-1.10.5/src/hdf5-1.10.5.tar.gz && tar zxvfp hdf5-1.10.5.tar.gz && cd hdf5-1.10.5
./configure && make && make install
cd .. && rm -rf hdf5-1.10.5
sudo apt-get install -y git
git clone -b master https://github.com/CGNS/CGNS.git && cd CGNS/src
./configure && make && make install

nvidia-modprobe -u -c=0
