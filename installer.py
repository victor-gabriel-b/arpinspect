import os
from geral import criar_arquivo, rodar, inicializar_config, editar_config_gui

# Obtendo o diretório de instalação
dir_instalacao = "/opt/arpinspect"
dir_instalacao = rodar('yad --file-selection --directory --title="Arpinspect - Selecione o diretório de instalação" --filename="/opt/arpinspect"')
if dir_instalacao == "":
  dir_instalacao = "/opt/arpinspect"

print()
print("Diretório de instalação recebido {}".format(dir_instalacao))

DIR_CONFIG = "/etc/arpinspect"
PATH = "/usr/bin"

CAMINHO_CONF = "{}/conf".format(DIR_CONFIG)
CAMINHO_SENHA = "{}/passwd".format(DIR_CONFIG)
CAMINHO_LOG = "/var/log/arpinspect"
CAMINHO_PID = "{}/pid".format(DIR_CONFIG)
CAMINHO_KILL = "{}/kill".format(DIR_CONFIG)



def definir_perms(arquivo, exec=False):
  os.chown(arquivo, 0, 0)

  os.system("chmod a-rwx {}".format(arquivo))
  os.system("chmod u+rw {}".format(arquivo))
  if exec:
    os.system("chmod u+x {}".format(arquivo))

# Cria um arquivo e muda suas permissões pra ser do root
def criar_arquivo_perm(arquivo, exec=False):
  criar_arquivo(arquivo)

  definir_perms(arquivo, exec)

def criar_diretorios(caminho):
  dirs = caminho.split("/")
  dirs_string = ""
  for i in dirs:
    dirs_string += i+"/"

  if os.path.isdir(dirs_string) == False:
    os.makedirs(dirs_string)  

criar_diretorios(dir_instalacao)

print("Instalando...")
os.rename("main.py", "{}/main.py".format(dir_instalacao))
os.rename("geral.py", "{}/geral.py".format(dir_instalacao))
os.rename("interface.py", "{}/interface.py".format(dir_instalacao))
os.rename("manager.py", "{}/manager.py".format(dir_instalacao))
os.rename("LICENSE", "{}/LICENSE".format(dir_instalacao))

print("Definindo permissões...")
definir_perms("{}/main.py".format(dir_instalacao), True)
definir_perms("{}/geral.py".format(dir_instalacao), True)
definir_perms("{}/interface.py".format(dir_instalacao), True)
definir_perms("{}/manager.py".format(dir_instalacao), True)

print("Inicializando arquivos de dados...")
criar_arquivo_perm(CAMINHO_CONF)
criar_arquivo_perm(CAMINHO_LOG)
criar_arquivo_perm(CAMINHO_SENHA)
criar_arquivo_perm(CAMINHO_KILL)
criar_arquivo_perm(CAMINHO_PID)

print("Criando link simbólico para o comando...")
print("ln -s {}/manager.py {}/arpinspect".format(dir_instalacao, PATH))
os.system("ln -s {}/manager.py {}/arpinspect".format(dir_instalacao, PATH))

inicializar_config()
print("Obtendo configurações iniciais...")
res = rodar('yad --text "Deseja Customizar as Configurações?" \
--button=yes-:0 --button=gtk-no:1')
if res == "Sim":
  print("OBTENDO INPUT")
  editar_config_gui()


print("Instalado!")