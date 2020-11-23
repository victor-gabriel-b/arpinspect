import shutil
import os
from pathlib import Path
from geral import rodar

res = rodar('action=$(yad --text "Você tem certeza que quer desinstalar o arpinspect e todos os seus arquivos?" \
--button=gtk-no:0 --button=gtk-yes:1)\nret=$?\necho $ret')

if res == "1":
  shutil.rmtree("/etc/arpinspect")
  shutil.rmtree(Path("arpinspect").resolve())
  os.rm("/var/log/arpinspect")

  rodar('zenity --info --title="Desistalação do Programa" --text=" O Programa Foi Desistalado!" --width 300')
