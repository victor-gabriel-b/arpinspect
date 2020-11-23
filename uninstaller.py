import shutil
import os
from pathlib import Path
from geral import rodar

res = rodar('action=$(yad --text "Você tem certeza que quer desinstalar o arpinspect e todos os seus arquivos?" \
--button=gtk-no:0 --button=gtk-yes:1)\nret=$?\necho $ret')

if res == "1":
  try:
    shutil.rmtree("/etc/arpinspect")
  except:
    pass

  try:
    shutil.rmtree(Path("/usr/bin/arpinspect").resolve())
  except:
    pass

  try:
    os.remove("/var/log/arpinspect")
  except:
    pass

  try:
    os.remove("/etc/init.d/arpinspect")
  except:
    print("Arquivos de inicialização bugados ou inexistentes")

  try:
    os.system("update-rc.d arpinspect remove")
  except:
    print("Arquivos de inicialização bugados ou inexistentes")

  rodar('zenity --info --title="Desistalação do Programa" --text=" O Programa Foi Desistalado!" --width 300')
