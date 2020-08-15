# arpinspect
Uma ferramenta para proteção de redes contra ataques ARP Spoof criada como parte da disciplina projeto integrador no IFPB.

O PROGRAMA INCLUI A OPÇÃO DE SER NOTIFICADO POR EMAIL, E ESTA USA A SUA SENHA PARA ENVIAR UM EMAIL A SI MESMO. USE COM CUIDADO, TENDO CERTEZA DE QUE AS PERMISSÕES DO ARQUIVO DE SENHA (/etc/arpinspect/passwd) ESTÃO CONFIGURADA CORRETAMENTE.

Para usar o programa, é melhor executá-lo em background (com um comando como: nohup tar -czf iso.tar.gz Templates/* &).
Para acessar as opções de configuração do programa, use o arquivo de configurações: /etc/arpinspect/conf
O log do programa é localizado no seguinte arquivo: /var/log/arpinspect
