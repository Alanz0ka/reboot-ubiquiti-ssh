
# Documentação do Script de Reboot de Antenas

## Visão Geral
Este script Python, usando a interface gráfica `tkinter`, facilita o reboot remoto de antenas. Ele se conecta às antenas via SSH (com `paramiko`) e executa os comandos de reboot de maneira assíncrona, usando `concurrent.futures`. 

## Dependências
- `tkinter`
- `paramiko`
- `concurrent.futures`
- `csv`
- `queue`

Para instalar `paramiko`, use o comando:

```bash
pip install paramiko
```

## Configuração
Antes de executar o script, é necessário selecionar um arquivo CSV contendo as informações das antenas. Cada linha do arquivo deve incluir:
- `IP`: Endereço IP da antena.
- `Porta` (opcional): Porta para a conexão SSH, padrão é 22 se não especificado.

Além disso, é necessário fornecer o nome de usuário e senha padrões para as conexões SSH através da interface gráfica.

## Uso
Execute o script em um ambiente Python com as dependências instaladas. A interface gráfica permite ao usuário:
1. Selecionar o arquivo CSV.
2. Inserir nome de usuário e senha padrões.
3. Iniciar o processo de reboot clicando no botão correspondente.

O script processa cada antena listada no arquivo CSV, realizando o reboot em paralelo, respeitando o limite máximo de threads definido pela variável `max_threads`.

## Funções Principais

### `reboot_antena(info_antena)`
Estabelece uma conexão SSH com a antena especificada, executa o comando de reboot e fecha a conexão. Registra os resultados na `result_queue`.

### `processar_antenas()`
Inicia o processo de reboot para todas as antenas listadas, executando as operações em paralelo e atualizando a interface gráfica.

### `atualizar_resultados()`
Atualiza continuamente a interface gráfica com os resultados do reboot.

### `select_csv_file()`
Permite ao usuário selecionar um arquivo CSV através da interface gráfica.

### `start_reboot()`
Lê o arquivo CSV, as credenciais fornecidas e inicia o processo de reboot das antenas.

## Segurança
**Aviso Importante**: Este script manipula informações sensíveis de autenticação. Mantenha essas informações seguras e não as exponha publicamente.

## Exemplo de Saída na Interface Gráfica
```
Reboot bem-sucedido em 192.168.1.1 - Resultado
Erro ao rebootar 192.168.1.2: Timeout na conexão
```

## Execução da Interface Gráfica
O script utiliza `tkinter` para criar uma interface gráfica amigável, facilitando a interação com o usuário para o processo de reboot.

---

**Nota**: Este script é um exemplo de automação de tarefas de rede com interface gráfica, e deve ser usado com cautela em ambientes de produção.
