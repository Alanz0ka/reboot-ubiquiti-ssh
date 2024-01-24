
# Documentação do Script de Reboot de Antenas

## Visão Geral
Este script é projetado para realizar a operação de reboot em múltiplas antenas remotas utilizando conexões SSH. Ele utiliza a biblioteca `paramiko` para estabelecer conexões SSH e a biblioteca `concurrent.futures` para executar múltiplas operações de reboot em paralelo.

## Dependências
- `paramiko`
- `time`
- `concurrent.futures`

Instale a biblioteca `paramiko` usando o pip:

```bash
pip install paramiko
```

## Configuração
As antenas alvo são definidas na lista `antenas`. Cada antena é representada por um dicionário contendo:
- `hostname`: Endereço IP da antena.
- `port`: Porta para conexão SSH (usualmente 22).
- `username`: Nome de usuário para autenticação SSH.
- `password`: Senha para autenticação SSH.

Exemplo de configuração de antenas:
```python
antenas = [
    {
        'hostname': '192.168.12.249',
        'port': 22,
        'username': 'nomeDoUsuario',
        'password': 'senha123',
    },
    # Adicione mais antenas conforme necessário
]
```

## Uso
Para usar o script, basta executá-lo em um ambiente Python com as dependências instaladas. O script irá automaticamente se conectar a cada antena na lista `antenas` e executar o comando de reboot.

O número máximo de threads (conexões SSH simultâneas) é definido pela variável `max_threads`. Ajuste este valor conforme necessário para evitar sobrecarga na rede ou nos dispositivos.

## Função `reboot_antena`
A função `reboot_antena` é responsável por estabelecer uma conexão SSH com cada antena, enviar o comando de reboot e encerrar a conexão. Ela retorna uma mensagem indicando o sucesso ou falha da operação.

## Execução Paralela
O script utiliza `concurrent.futures.ThreadPoolExecutor` para executar a função `reboot_antena` em múltiplas threads, permitindo o reboot de várias antenas simultaneamente.

## Resultados
Após a execução do script, os resultados de cada operação de reboot (sucesso ou falha) são exibidos na tela.

## Segurança
**Aviso Importante**: O script contém informações sensíveis de autenticação. Certifique-se de manter estas informações em segurança e não as compartilhe publicamente.

## Exemplo de Saída
```
Reboot bem-sucedido em 192.168.12.249
Erro ao rebootar 192.168.12.24: [mensagem de erro]
```

---
