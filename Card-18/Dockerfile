# usa a imagem do Ubuntu
FROM ubuntu
# Instalando o apache
RUN apt-get update && apt-get install -y apache2
# seleciona o diretório que será utilizado nos próximos comandos
WORKDIR /var/www/html
# executa os comandos touch e echo no diretório
RUN touch arquivo.txt && echo "Cavalo" > arquivo.txt
# mapeando uma porta
EXPOSE 80
# inicia o apache e o mantém rodando
CMD ["apachectl", "-D", "FOREGROUND"]
# definindo um volume
VOLUME /var/www/html