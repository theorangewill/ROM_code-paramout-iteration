#! /bin/bash

#Instalação de dependências
VERSION=1.11.4 
OS=linux 
ARCH=amd64
CURRDIR=$(pwd)
GOPATH=${HOME}/go
PATH=/usr/local/go/bin:${PATH}:${GOPATH}/bin

sudo DEBIAN_FRONTEND=noninteractive apt-get update -qy && \
	sudo DEBIAN_FRONTEND=noninteractive apt-get install -qy build-essential \
	libssl-dev uuid-dev libgpgme11-dev libseccomp-dev pkg-config squashfs-tools
	wget -O /tmp/go${VERSION}.${OS}-${ARCH}.tar.gz https://dl.google.com/go/go${VERSION}.${OS}-${ARCH}.tar.gz && \
	sudo tar -C /usr/local -xzf /tmp/go${VERSION}.${OS}-${ARCH}.tar.gz 
curl -sfL https://install.goreleaser.com/github.com/golangci/golangci-lint.sh | sh -s -- -b $(go env GOPATH)/bin v1.15.0
##Instalação do singularity
mkdir -p ${GOPATH}/src/github.com/sylabs && \
	cd ${GOPATH}/src/github.com/sylabs && \
	git clone https://github.com/sylabs/singularity.git && \
	cd singularity
git checkout v3.2.1
cd ${GOPATH}/src/github.com/sylabs/singularity && \
	./mconfig && \
	cd ./builddir && \
	make && \
	sudo make install
#echo "Verificando instalaçao"
singularity version 1>/dev/null && echo "Instalado com sucesso"
cd $CURRDIR
rm -rf $GOPATH
#Download da base de dados e preparação do código
echo "Baixando base de dados"
apt-get install -y unzip
mkdir dynamic_stall_data 
cd dynamic_stall_data
wget --no-check-certificate "https://onedrive.live.com/download?cid=68B743CBCE8A14C0&resid=68B743CBCE8A14C0%21107533&authkey=AIRCWrGDBz471sE" 
mv * qSpanAvg.cgns 
cd ..
#echo "Modificando arquivos para executar codigo"
sed -i '1s#/home/cfd/Desktop/hugo/#'"$CURRDIR"'/#' code/inputs.inp
sed -i '3s#/home/cfd/Desktop/hugo/ROM_code#'"$CURRDIR"'/#' code/inputs.inp
echo Instalando imagem do container
if [ $1 == "cpu" ]; then
	sed -i 's/tensorflow-gpu/tensorflow/' dnn_rom.def
fi
singularity build rom_dnn.sif dnn_rom.def
nvidia-modprobe -u -c=0
