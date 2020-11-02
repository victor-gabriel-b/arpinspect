# ARQUIVO PARA FUNÇÕES QUE SÃO USADAS POR MAIS DE UM SCRIPT

import datetime

global caminho_log
caminho_log = "/var/log/arpinspect"
# Escreve uma string no arquivo de log
def escrever_no_log(string):
  global caminho_log
  with open(caminho_log, "a") as arq:
    arq.write("[{}]:{}".format(datetime.datetime.now(), string))
