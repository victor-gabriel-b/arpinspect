# ArpInspect: Um programa de segurança de redes internas contra ataques ARP Spoof
#Copyright (C) 2020  Victor Gabriel Batista Reinaldo, Edclaudio Santos de araújo

# This program is free software; you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation; either version 2 of the License, or (at your option) any later version.

# This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License along with this program; if not, write to the Free Software Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.

# Informações de contato:
# Victor: victor.reinaldo@academico.ifpb.edu.br
# Edclaudio: edclaudio.santos@academico.ifpb.edu.br


# ARQUIVO PARA FUNÇÕES QUE SÃO USADAS POR MAIS DE UM SCRIPT

import datetime
import os
import subprocess

global caminho_kill
global caminho_log
global caminho_conf
caminho_log = "/var/log/arpinspect"
caminho_kill = "/etc/arpinspect/kill"]
caminho_conf = "/etc/arpinspect/conf"
caminho_senha = "/etc/arpinspect/passwd"

# Escreve uma string no arquivo de log
def escrever_no_log(string):
  print("Abriu a função de log")
  global caminho_log
  with open(caminho_log, "a") as arq:
    arq.write("[{}]:{}".format(datetime.datetime.now(), string))
  print("log gravado")

# Retira a ultima parte de um caminho, transformando o caminho de um arquivo no caminho do seu diretório
def tirar_arquivo(caminho):
  dirs = caminho.split("/")[:-1]
  dirs_string = ""
  for i in dirs:
    dirs_string += i+"/"

  return dirs_string

# Cria um arquivo no caminho especificado, criando também todos o diretorios necessários
def criar_arquivo(caminho, conteudo=""):
  # Quando for botar pra windows vai dar errado *_*
  dirs_string = (tirar_arquivo(caminho))

  if os.path.isdir(dirs_string) == False:
    os.makedirs(dirs_string)  

  with open(caminho,"w") as arq:
    arq.write(conteudo)

# Roda um comando do yad
def rodar(comando):
  saida = subprocess.Popen(comando, shell=True, 
           stdout=subprocess.PIPE, 
           stderr=subprocess.STDOUT)
           
  linhas = saida.stdout.read().decode("utf-8").split("\n")
  print("Input cru: ", linhas)

  i = 0
  while i<len(linhas):
    if linhas[i].find("WARNING") != -1:
      print("linha mt doida detectada:", linhas[i])
      del linhas[i]

    if linhas[i].find("Error") != -1:
      print("linha mt doida detectada:", linhas[i])
      del linhas[i]

    if linhas[i] == "":
      del linhas[i]
    i += 1

  if len(linhas) == 0:
    linhas.append("")

  print("Input recebido: ", linhas)
  return linhas[0]

# Cria o arquivo de configuração com suas configurações padrão
def inicializar_config():
  criar_arquivo(caminho_conf, "#Tempo de cada ciclo de execução\ntempo=60\n#Quantidade de pacotes por ciclo de execução que é considerada como um ataque\nqtd=5\n#Configura o mac do gateway. Você pode deixar como auto pra obter autromaticamente. (É fortemente recomendado setar manualmente essa configuração)\nmac_gateway=auto\n#Seta de forma fixa o ip do gateway. Você pode deixar como auto pra obter automaticamente.\nip_gateway=auto\n#Ativa ou desativa o bloqueio de ARP Replies gratuitos (true ou false).\nblock_arp_grat=true\n#Email que vai ser usado pra enviar notificações\nemail=")

# Realiza a configuração do bloqueio de arp replies gratuitos
def config_block_arp_grat(valor):
  config_atual = "block_arp_grat"
  # Ativa ou desativa o bloqueio de ARP Replies gratuitos (usando uma configuração disponível no linux)
  if valor == "true":
    os.system("echo 1 > /proc/sys/net/ipv4/conf/all/arp_accept")
  else:
    os.system("echo 0 > /proc/sys/net/ipv4/conf/all/arp_accept")

# Abre a tela de configurar inicializaçao no boot e faz as alterações necessárias
def config_init_gui():
  valor = rodar('action=$(yad --text "Você quer que o programa rode ao inicializar?" \
  --button=gtk-no:0 --button=gtk-yes:1)\nret=$?\necho $ret')

  if valor == "1":
    with open("/etc/init.d/arpinspect", "w") as arq:
      arq.write("#!/bin/sh\narpinspect start")

    os.system("update-rc.d arpinspect defaults")
        
  elif valor == "0":
    try:
      os.remove("/etc/init.d/arpinspect")
    except:
      print("Arquivos de inicialização bugados ou inexistentes")

    try:
      os.system("update-rc.d arpinspect remove")
    except:
      print("Arquivos de inicialização bugados ou inexistentes")

# Chama a interface de configuração e faz as alterações selecionadas pelo usuário
def editar_config_gui():
    # Lendo os valores do arquivo de configuração e formatando
    with open(caminho_conf, "r") as arq:
      configs = arq.readlines()
      str_valores = ""
      for i in range(len(configs)):
        config = configs[i].split("=")
        # Testar o ignorar de # ***
        if config[0][0] != "#":
          str_valores += "{}\t|{}|".format(config[0], config[1].replace("\n",""))
   
    # Mostrando a tela e obtendo input
    config_alterada = rodar('zenity --forms                                   \
      --text "Ver e editar configurações"  \
      --add-entry "Valor da configuração" --add-list="Valor e nome da configuração"    \
      --column-values "Config|Valor"               \
      --list-values="{}" --show-header'.format(str_valores)) 
      
    if config_alterada != "":   
        config_alterada = config_alterada.split("\t")[0]	
        config_alterada = config_alterada.split("|")

        # Alterando a configuração na lista		
        for i in range(len(configs)):
          if configs[i].split("=")[0].replace("\n","").replace("\t","") == config_alterada[1].replace("\n","").replace("\t",""):
            configs[i] = "{}={}\n".format(config_alterada[1].replace("\t",""), config_alterada[0])
            break	    

        # Escrevendo as novas configurações no arquivo
        with open(caminho_conf, "w") as arq:
          arq.writelines(configs)
            
          #Config 1 |10|Config 2    |20\
          #|Config 3   |30 |
    print("config_alterada:", config_alterada)
    try:
      if config_alterada[1] == "block_arp_grat":
        print(config_alterada) # Testar ***
        config_block_arp_grat(config_alterada[1]) #   Testar
    except IndexError:
      pass
      
    return config_alterada

# Chama a tela de edição de senha e faz as alterações necessárias
def editar_senha_gui():
    # Mostrando a tela e obtendo a senha nova
    senha = rodar("zenity --forms --title='Redefinir senha'  \
      --text='Informe sua senha'       \
      --add-password=Senha                 \
      --add-password='Confirme a senha'    \\")
    
    if senha != "":
        senha = senha.split("|")

        if senha[0]!=senha[1]:
          rodar('zenity --info --text "As senhas não batem."')

        else:
          # Escrevendo a senha no arquivo
          with open(caminho_senha, "w") as arq:
            arq.write(senha[0])
          return True

    else:
      rodar('zenity --info --text "A senha não foi definida."')
      return True

    return False