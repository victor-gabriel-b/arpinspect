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

import subprocess
#TODO: LIDAR COM HASHTAGS NO COMEÇO DAS LINHAS DE CONFIGURAÇÃO
caminho_senha = "/etc/arpinspect/passwd"
caminho_conf = "/etc/arpinspect/conf"
caminho_log = "/var/log/arpinspect"

def rodar(comando):
  saida = subprocess.Popen(comando, shell=True, 
           stdout=subprocess.PIPE, 
           stderr=subprocess.STDOUT)
           
  linhas = saida.stdout.read().decode("utf-8").split("\n")
  
  i = 0
  while i<len(linhas):
    if "Gtk-WARNING" in linhas[i]:
        del linhas[i]
    i += 1

  return linhas[0]


while True:
  tela_escolhida = rodar('zenity --list --column Selecionar --column Arquivos FALSE "Ver Log" TRUE "Editar Configurações" FALSE "Editar Senha" --radiolist')

  if tela_escolhida == "Ver Log":
    # Lê o arquivo de log e exibe na tela
    rodar("cat {} | zenity --text-info".format(caminho_log))

  elif tela_escolhida == "Editar Configurações":
    # Lendo os valores do arquivo de configuração e formatando
    with open(caminho_conf, "r") as arq:
      configs = arq.readlines()
      str_valores = ""
      for i in range(len(configs)):
        config = configs[i].split("=")
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


  elif tela_escolhida == "Editar Senha":
    # Mostrando a tela e obtendo a senha nova
    senha = rodar("zenity --forms --title='Redefinir senha'  \
      --text='Informe sua senha'       \
      --add-password=Senha                 \
      --add-password='Confirme a senha'    \\")
    
    if senha != "":
        senha = senha.split("|")

        if senha[0]!=senha[1]:
          rodar('zenity --info --text "As senhas não batem, OTÁRIO."')

        else:
          # Escrevendo a senha no arquivo
          with open(caminho_senha, "w") as arq:
            arq.write(senha[0])
    

  else:
    break