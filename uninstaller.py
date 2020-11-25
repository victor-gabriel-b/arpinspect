import shutil
import os
from pathlib import Path
from geral import rodar, tirar_arquivo

res = rodar('action=$(yad --text "Você tem certeza que quer desinstalar o arpinspect e todos os seus arquivos? (Obs: Isso deletará completamente a pasta de instalação!)" \
--button=gtk-no:0 --button=gtk-yes:1)\nret=$?\necho $ret')

print("QUALQUER ARQUIVO QUE JÁ NÃO EXISTE OU NÃO PODE SER REMOVIDO SERÁ")
if res == "1":
  try:
    shutil.rmtree("/etc/arpinspect")
  except:
    print("Não consegui remover o /etc/arpinspect")

  DIR_INSTALACAO = tirar_arquivo(str(Path("/usr/bin/arpinspect").resolve()))
  try:
    shutil.rmtree(DIR_INSTALACAO)
  except:
    print("Não consegui remover o diretorio de instalação:", DIR_INSTALACAO)

  try:
    os.remove("/var/log/arpinspect")
  except:
    print("Não consegui remover o log (/var/log/arpinspect")

  try:
    os.remove("/etc/init.d/arpinspect")
  except:
    print("Arquivos de inicialização bugados ou inexistentes")

  try:
    os.system("update-rc.d arpinspect remove")
  except:
    print("Arquivos de inicialização bugados ou inexistentes")

  try:
    os.remove("/usr/bin/arpinspect")
  except:
    print("Não consegui remover o link no PATH (/usr/bin/arpinspect)")

  rodar('zenity --info --title="Desistalação do Programa" --text=" O Programa Foi Desistalado!" --width 300')
