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

global caminho_log
caminho_log = "/var/log/arpinspect"
# Escreve uma string no arquivo de log
def escrever_no_log(string):
  global caminho_log
  with open(caminho_log, "a") as arq:
    arq.write("[{}]:{}".format(datetime.datetime.now(), string))
