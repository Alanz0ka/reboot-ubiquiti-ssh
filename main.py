import paramiko
import time
import concurrent.futures

# Lista de antenas com seus endereços IP internos e informações de conexão SSH
antenas = [
    {
        'hostname': '192.168.12.249',
        'port': 22,  
        'username': 'suporte',
        'password': 'Senha',
    },
    {
        'hostname': '192.168.12.24',
        'port': 22,  
        'username': 'suporte',
        'password': 'Senha',
    },
    
]

# Comando de reboot
comando_reboot = 'reboot'

def reboot_antena(info_antena):
    try:
        ssh_client = paramiko.SSHClient()
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        
        ssh_client.connect(info_antena['hostname'], port=info_antena['port'], 
                            username=info_antena['username'], password=info_antena['password'])

        time.sleep(30)
        stdin, stdout, stderr = ssh_client.exec_command(comando_reboot)

        ssh_client.close()
        
        return f'Reboot bem-sucedido em {info_antena["hostname"]}'
    except Exception as e:
        return f'Erro ao rebootar {info_antena["hostname"]}: {str(e)}'

# Número máximo de threads/conexões simultâneas
max_threads = 2

with concurrent.futures.ThreadPoolExecutor(max_threads) as executor:
    resultados = list(executor.map(reboot_antena, antenas))

# Exibir resultados
for resultado in resultados:
    print(resultado)