# -*- coding: utf-8 -*-

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


#O PROGRAMA USA A SENHA DO SEU EMAIL PARA LHE NOTIFICAR, TIRANDO ELA DE UM ARQUIVO. DÊ AS PERMISSÕES DE ACESSO CORRETAS AO ARQUIVO (DE PREFERÊNCIA, APENAS UM USUÁRIO PODE ACESSAR, E O PROGRAMA É EXECUTADO COMO SENDO DO MESMO USUÁRIO).
#Tem que ter TCPDump, python 3, getmac, netifaces, smtplib e ssl e scapy instalado

import os
from scapy.all import sniff
import netifaces
import getmac
import smtplib
import ssl
import datetime

global combs
combs = []  # Lista das combinações de endereços

global emails_a_enviar
emails_a_enviar = []

global senha

global caminho_conf
global caminho_log
global caminho_senha
caminho_senha = "/etc/arpinspect/passwd"
caminho_conf = "/etc/arpinspect/conf"
caminho_log = "/var/log/arpinspect"


# Cria um arquivo no caminho especificado, criando também todos o diretorios necessários
def criar_arquivo(caminho, conteudo=""):
  # Quando for botar pra windows vai dar errado *-*
  dirs = caminho.split("/")[:-1]
  dirs_string = ""
  for i in dirs:
    dirs_string += i+"/"

  if os.path.isdir(dirs_string) == False:
    os.makedirs(dirs_string)

  with open(caminho,"w") as arq:
    arq.write(conteudo)

# Variáveis de configuração
global tempo_ciclo  # Duração de um ciclo de execução do programa
global qtd_pacotes  # Quantidade de pacotes de um mesmo IP e mesmo MAC por ciclo que é considerada um ataque

global ip_gateway  # IP do gateway, por padrão é obtido pelo programa, mas pode ser alterado manualmente pelo arquivo de configuração
ip_gateway = netifaces.gateways()['default'][netifaces.AF_INET][0]

global mac_gateway  # MAC do gateway, por padrão é obtido pelo programa, mas pode ser alterado manualmente pelo arquivo de configuração
mac_gateway = getmac.get_mac_address(ip=ip_gateway, network_request= True)

global email_origem  # O email que será notificado e que enviára o email
email_origem = ""

# Obter configurações a partir do arquivo de configurações (normalmente /etc/arpinspect/conf)
def obter_config(caminho_conf): 
  global tempo_ciclo
  global qtd_pacotes
  global ip_gateway
  global mac_gateway
  global email_origem

  tempo_ciclo = 60
  qtd_pacotes = 5

  # Tenta obter as configurações, caso dê erro, cria o arquivo de configuração (caso não exista) com as configurações padrão já dentro
  try:
    with open(caminho_conf, "r") as conf:
      cfg_lista = conf.readlines()

      # Itera pelas linhas do arquivo de configuração, tomando as ações necessárias para cada configurar
      for i in cfg_lista:
        # Esse if exclui as linhas que começam com #
        if i[0] != "#":
          nome, valor = i.split("=")
          valor.replace("\n", "")
          
          if nome == "tempo":
            tempo_ciclo = int(valor)
          elif nome == "qtd":
            qtd_pacotes = int(valor)


          elif nome == "ip_gateway":
            # Ver se tem uma configuração manual válida, e usar a padrão (olha o que o sistema diz) caso não tenha
            partes = valor.split(".")
            
            certo = True
            for i in partes:
              if i.isnumeric():
                if int(i)>=0 and int(i)<=255:
                  continue
                else:
                  certo = False
                  break
              else:
                certo = False 
                break
            
            if certo:
              ip_gateway = valor
            else:
              ip_gateway = netifaces.gateways()['default'][netifaces.AF_INET][0]


          elif nome == "mac_gateway":
            # Ver se tem uma configuração manual válida, e usar a padrão (olha o que o sistema diz) caso não tenha
            partes = valor.split(":")
            qtd_letras = 0
            certo = True
            for i in partes:
              for j in i:
                qtd_letras += 1              
                if j =="A" or j=="B" or j=="C" or j=="D" or j== "E" or j== "F":
                  continue
                elif int(j) >=0 and int(j)<=9:
                  continue
                else:
                  certo = False
                  break

            if certo:
              mac_gateway = valor
            else:
              mac_gateway = getmac.get_mac_address(ip=ip_gateway, network_request=True)
          
          elif nome == "block_arp_grat":
            # Ativa ou desativa o bloqueio de ARP Replies gratuitos (usando uma configuração disponível no linux)
            if valor == "true":
              os.system("echo 1 > /proc/sys/net/ipv4/conf/all/arp_accept")
            else:
              os.system("echo 0 > /proc/sys/net/ipv4/conf/all/arp_accept")

          elif nome == "email":
            email_origem = valor.replace("\n", "")
 
  except:
    # Criar o arquivo com as configurações padrão, e então acessar novamente
    criar_arquivo(caminho_conf, "tempo=60\nqtd=5\n#mac_gateway=\n#ip_gateway=\nblock_arp_grat=true\nemail=")
    obter_config(caminho_conf)

obter_config(caminho_conf)

# Classe que serve pra armazenar as informações de um email à ser enviado
class Email:
  def __init__(self, ip, mac, tipo_ataque):
    self.ip = ip
    self.mac = mac
    self.tipo_ataque = tipo_ataque
    self.data_e_hora = datetime.datetime.now()


# Classe das combinações de endereços IP/MAC
# Guarda o IP, MAC e quantidade de pacotes detectados com essa combinação de IP e MAC (ambos sendo os de origem)
class CombEnderecos:
  
  def __init__(self,ip, mac):
    self.ip = ip
    self.mac = mac

    # Contador da quantidade de pacotes capturados com esse IP e MAC
    self.qtd_ocorr = 0

# Função para tratamento inicial do pacote
# É chamada assim que um pacote é recebido, servindo pra verificar se o pacote deve ser analisado e repassar para a função analisa_pacote caso seja
def trata_pacote(pacote):
  mac = pacote.src

  # Verificando se o MAC de origem não é desta máquina
  for i in netifaces.interfaces():
    for j in netifaces.ifaddresses(i)[netifaces.AF_LINK]:
      if j["addr"] == mac:
        return

  # Verificando se o pacote é ARP Reply
  if pacote.op == 2:
    # .src é o MAC de origem, .psrc é o ip de origem
    analisa_pacote(pacote.psrc,pacote.src)

# Função pra enviar um email
def enviar_email(assunto, conteudo):
  global senha
  global email_origem
  
  if email_origem == "":
    with open(caminho_log, "a") as arq:
      arq.write("Nenhum email foi inserido. Nada será enviado.\n")
      return
  

  # Formatando a mensagem
  mensagem = 'Subject: {}\n\n{}'.format(assunto,conteudo).encode("utf-8")

  # Enviando o email
  
  server.sendmail(email_origem, email_origem, mensagem)
  



# Verifica cada combinacao ip/mac, vendo se é igual à do pacote recebido
# Caso seja, aumenta o contador da combinação
# Caso contrário, cria uma nova combinação
def analisa_pacote(ip, mac):
  global combs
  global ip_gateway
  global mac_gateway
  global emails_a_enviar

  # Verificando se o IP de origem do pacote é o mesmo do gateway, porém com um MAC diferente do configurado associado à ele
  if ip == ip_gateway and mac != mac_gateway:
    with open(caminho_log, "a") as arq:
      # Registrando ataque no log e adicionando um email para ser enviado

      arq.write("MAC diferente do configurado dizendo ter o ip do Gateway ({}) detectado: de {} (original) para {}\n".format(ip, mac_gateway, mac))
      emails_a_enviar.append(Email(ip, mac, "spoof_gateway"))

  # Vendo se pacotes com esses mesmos IP e MAC já foram encontrados. Caso sim, Adiciona a contagem de vezes encontradas (qtd_ocorr). Caso contrário, cria um novo objeto e seta sua contagem pra 1 
  for c in combs:
    if c.ip == ip and c.mac == mac:
      c.qtd_ocorr += 1
      return
    
  # Criando novo objeto
  nova_comb = CombEnderecos(ip, mac)
  nova_comb.qtd_ocorr += 1
  combs.append(nova_comb)
  

def main():
  global emails_a_enviar
  global combs
  global mac_gateway
  global caminho_conf
  global caminho_log
  global caminho_senha


  sniff(filter="arp", prn=trata_pacote, timeout=tempo_ciclo)

  # Loop de checagem de ataque
  for i in combs:
    if i.qtd_ocorr >= qtd_pacotes:
      # Ao detectar um ataque, o programa roda um comando de shell para criar uma regra no Iptables, definindo que todos os pacotes com aquele ip e mac devem ser descartados

      os.system("iptables -A INPUT -s {} -m mac --mac-source {} -j DROP".format(i.ip,i.mac))
      with open(caminho_log,"a") as arq:
        arq.write("Ataque Detectado (número excessivo de pacotes ARP Reply): {} {}\n".format(i.ip,i.mac))

        # Pode ser válido verificar se foi realmente bloqueado mesmo antes de mandar ***
        enviar_email("Notificação do ArpInspect", "Ataque Detectado (número excessivo de pacotes ARP Reply): {} {}\n\nO host mencionado foi bloqueado de entrar na tabela ARP através do IPtables".format(i.ip,i.mac))


  emails_enviados = []
  # Enviar os emails sem repetir o mesmo várias vezes, pode ter outra forma mais eficiente ***
  for email in emails_a_enviar:
    # Adicionar verificação de tipo caso necessário aqui
    ja_enviado = False
    for enviado in emails_enviados:
      if enviado.ip == email.ip and enviado.mac == email.mac and enviado.tipo_ataque == email.tipo_ataque:
        ja_enviado = True
        break
      
    if ja_enviado == False:
      emails_enviados.append(email)
      enviar_email("Notificação do ArpInspect","Um MAC diferente do configurado dizendo ter o ip do Gateway ({}) foi detectado em um de seus hosts({}): de {} (original) para {}.\n\n O MAC em questão não foi bloqueado, pois pode se tratar de uma mudança legítima.".format(email.ip, os.uname()[1], mac_gateway, email.mac))


# Testando se o arquivo de log existe, e criando ele caso não exista
try:
  with open(caminho_log,"r") as arq:
    arq.read()
except:
  criar_arquivo(caminho_log,"COMEÇO DO LOG\n")

# Preparando pra envio de emails dentro do programa
with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=ssl.create_default_context()) as server:

  # Obtendo a senha para o uso do email
  try:
    with open(caminho_senha, "r") as arq:
      senha = arq.read() # Variável global estabelecida anteriormente

  #except IOError
  except:
    criar_arquivo(caminho_senha)
    with open(caminho_log, "w") as arq:
      arq.write("Arquivo de senha não encontrado. Criando arquivo vazio em {}\n".format(caminho_senha))
      
  # Tentando logar no email
  try:
    server.login(email_origem, senha)
  except:
    pass

  # Setando a senha pra nulo, espero que seja efetivo
  senha = None

  # Loop principal de execução do programa
  # Cada iteração é considerada um ciclo de execução do programa
  while True:
    combs = []
    emails_a_enviar = []

    main()




