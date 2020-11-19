DIR_INSTALACAO = "/opt/arpinspect"
PATH = "/usr/bin"

import os

def criar_diretorios(caminho):
  dirs = caminho.split("/")
  dirs_string = ""
  for i in dirs:
    dirs_string += i+"/"

  if os.path.isdir(dirs_string) == False:
    os.makedirs(dirs_string)  

criar_diretorios(DIR_INSTALACAO)
criar_diretorios(PATH)

print("Instalando...")
os.rename("main.py", "{}/main.py".format(DIR_INSTALACAO))
os.rename("geral.py", "{}/geral.py".format(DIR_INSTALACAO))
os.rename("interface.py", "{}/interface.py".format(DIR_INSTALACAO))
os.rename("manager.py", "{}/arpinspect.py".format(PATH))
print("Instalado!")