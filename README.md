# DNN-ROM code 
The DNN-ROM code can be used for construction of reduced order models, ROMs, of fluid flows. The code employs a combination of flow modal decomposition and regression analysis. Spectral proper orthogonal decomposition, SPOD, is applied to reduce the dimensionality of the model and, at the same time, filter the POD temporal modes. The regression step is performed by a deep feedforward neural network, DNN, and the current framework is implemented in a context similar to the sparse identification of non-linear dynamics algorithm, SINDy. Test cases such as the compressible flow past a cylinder and the turbulent flow computed by a large eddy simulation of a plunging airfoil under dynamic stall are provided. For more details, see https://arxiv.org/abs/1903.05206. 

# Trabalho 
Este repositório fornece o código preparado para execução do trabalho prático da disciplina MO833, incluindo scripts de automatização e uma receita de container que executa a aplicação.

# Instâncias utilizadas

Recomendamos a utilização de dois tipos de instâncias para validação. Para utilizar o tensorflow na CPU, utilizamos da família c5. Já para o tensorflow na GPU, utilizamos as instâncias das famílias p2 e p3.

#Imagens

Para imagens, recomendamos pelo menos 70GB de disco, para garantir espaço de armazenamento dos resultados. 
Para utilização do tensorflow na CPU, utilizamos a imagem Ubuntu Server 18.04 LTS [ami-024a64a6685d05041]. 
Para utilizalção de tensorflow na GPU, utilizamos a imagem Deep Learning AMI (Ubuntu) Version 18.1 [ami-024a64a6685d05041], que já possui os drivers CUDA instalados.

# Receita

Para criar o container a partir da receita, basta executar:
* Tensorflow para CPU:
```sh
sudo ./install_dep.sh cpu
```
* Tensorflow para GPU:
```sh
sudo ./install_dep.sh 
```

Ao final da execução, será criado um container de nome *rom_dnn.sif*.

*Obs: Não esqueça de utilizar --nv caso esteja executando a receita em uma instância com GPUs.*

# Script de execução
Para executar o código, basta executar o script shell dentro da pasta *code*
```sh
cd code && sh run.sh
```
Para executar apenas utilizando o método de paramount iteration, utilize:
```sh
cd code && sh run.sh <p_number> <full_number>
```
Onde *<p_number>* é o número de iterações em paramount, e *<full_number>* é o número de execuções utilizadas para validação do método paramount.
A execução apresentada consiste de 5 execuções em *paramount iteration*, seguidas de 5 execuções do número de iterações que estimula uma execução cheia (*full_number*).
Outra alternativa é executar o script *./exec_script* na raíz do repositório, que executará 
