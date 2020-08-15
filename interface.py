import subprocess

caminho_senha = "/etc/arpdef/passwd"
caminho_conf = "/etc/arpdef/conf"
caminho_log = "/var/log/ArpDefender"

def rodar(comando):
  saida = subprocess.Popen(comando, encoding="utf-8",shell=True, 
           stdout=subprocess.PIPE, 
           stderr=subprocess.STDOUT)
  return saida.stdout.read().split("\n")[1]


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

    senha = senha.split("|")

    if senha[0]!=senha[1]:
      rodar('zenity --info --text "As senhas não batem, OTÁRIO."')

    else:
      # Escrevendo a senha no arquivo
      with open(caminho_senha, "w") as arq:
        arq.write(senha[0])
    

  else:
    break

