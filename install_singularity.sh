#Instalação de dependências
VERSION=1.11.4 
OS=linux 
ARCH=amd64
CURRDIR=$(pwd)
echo 'export GOPATH=${HOME}/go' >> ~/.bashrc
echo 'export PATH=/usr/local/go/bin:${PATH}:${GOPATH}/bin' >> ~/.bashrc
source ~/.bashrc
sudo apt-get update && \
	sudo apt-get install -y build-essential \
	libssl-dev uuid-dev libgpgme11-dev libseccomp-dev pkg-config squashfs-tools
	wget -O /tmp/go${VERSION}.${OS}-${ARCH}.tar.gz https://dl.google.com/go/go${VERSION}.${OS}-${ARCH}.tar.gz && \
	sudo tar -C /usr/local -xzf /tmp/go${VERSION}.${OS}-${ARCH}.tar.gz
curl -sfL https://install.goreleaser.com/github.com/golangci/golangci-lint.sh |
sh -s -- -b $(go env GOPATH)/bin v1.15.0
#Instalação do singularity
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
echo "Verificando instalaçao"
singularity version 1>/dev/null && echo "Instalado com sucesso"
cd $CURRDIR
rm -rf $GOPATH
#Download da base de dados e preparação do código
echo "Baixando base de dados"
mkdir cylinder_data 
cd cylinder_data
wget https://www.dropbox.com/sh/ji6i5u8valqyda8/AABtEYaZ7vG-62q6h4toQKBTa?dl=0
mv AABtEYaZ7vG-62q6h4toQKBTa?dl=0 cylinder.zip
unzip -q cylinder.zip
rm cylinder.zip 
cd ..
echo "Modificando arquivos para executar codigo"
sed -i '1s#/home/cfd/Desktop/hugo/#'"$CURRDIR"'#' code/inputs.inp
sed -i '3s#/home/cfd/Desktop/hugo/ROM_code#'"$CURRDIR"'/code#' code/inputs.inp
echo Instalando imagem do container
singularity build dnn_rom.sif dnn_rom.def
