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


#TODO: LIDAR COM HASHTAGS NO COMEÇO DAS LINHAS DE CONFIGURAÇÃO
caminho_senha = "/etc/arpinspect/passwd"
caminho_conf = "/etc/arpinspect/conf"
caminho_log = "/var/log/arpinspect"


from geral import rodar, editar_config_gui, editar_senha_gui


while True:
  tela_escolhida = rodar('zenity --list --column Selecionar --column Arquivos FALSE "Ver Log" TRUE "Editar Configurações" FALSE "Editar Senha" --radiolist')

  if tela_escolhida == "Ver Log":
    # Lê o arquivo de log e exibe na tela
    rodar("cat {} | zenity --text-info".format(caminho_log))

  elif tela_escolhida == "Editar Configurações":
    editar_config_gui() # ver se isso funciona ***

  elif tela_escolhida == "Editar Senha":
    editar_senha_gui()
    
  else:
    break