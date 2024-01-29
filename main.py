import tkinter as tk
from tkinter import filedialog
import paramiko
from concurrent.futures import ThreadPoolExecutor, as_completed
import csv
import queue

# Declarar a variável max_threads no escopo global
max_threads = 2

def reboot_antena(info_antena):
    try:
        ssh_client = paramiko.SSHClient()
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        
        ssh_client.connect(info_antena['hostname'], port=info_antena['port'], 
                            username=default_username, password=default_password)

        stdin, stdout, stderr = ssh_client.exec_command(comando_reboot)
        result = stdout.read().decode('utf-8').strip()

        ssh_client.close()
        
        result_queue.put(f'Reboot bem-sucedido em {info_antena["hostname"]} - {result}')
    except Exception as e:
        result_queue.put(f'Erro ao rebootar {info_antena["hostname"]}: {str(e)}')

def processar_antenas():
    result_text.delete(1.0, tk.END)
    start_button.config(state=tk.DISABLED)  # Desativar botão de iniciar

    with ThreadPoolExecutor(max_threads) as executor:
        futures = {executor.submit(reboot_antena, antena): antena for antena in antenas}

        for future in as_completed(futures):
            antena = futures[future]

            try:
                future.result()  # Aguardar a conclusão da thread
            except Exception as e:
                print(f'Erro ao processar {antena["hostname"]}: {str(e)}')

    start_button.config(state=tk.NORMAL)  # Reativar botão de iniciar

def atualizar_resultados():
    while not result_queue.empty():
        resultado = result_queue.get()
        result_text.insert(tk.END, resultado + '\n')
        result_text.update()

    root.after(100, atualizar_resultados)

# Função para selecionar arquivo CSV
def select_csv_file():
    file_path = filedialog.askopenfilename(filetypes=[('CSV Files', '*.csv')])
    if file_path:
        entry_csv_file.delete(0, tk.END)
        entry_csv_file.insert(0, file_path)

# Função para iniciar o reboot
def start_reboot():
    csv_file = entry_csv_file.get()
    username = entry_username.get()
    password = entry_password.get()

    with open(csv_file, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            antenas.append({
                'hostname': row['IP'],
                'port': int(row.get('Porta', 22)),
            })

    global default_username, default_password, comando_reboot
    default_username = username
    default_password = password

    processar_antenas()
    atualizar_resultados()

# Configurar a janela principal
root = tk.Tk()
root.title('Reboot de Antenas')

# Elementos da interface
tk.Label(root, text='Arquivo CSV:').pack(pady=5)
entry_csv_file = tk.Entry(root, width=40)
entry_csv_file.pack(pady=5)
tk.Button(root, text='Selecionar Arquivo', command=select_csv_file).pack(pady=5)

tk.Label(root, text='Nome de Usuário Padrão:').pack(pady=5)
entry_username = tk.Entry(root)
entry_username.pack(pady=5)

tk.Label(root, text='Senha Padrão:').pack(pady=5)
entry_password = tk.Entry(root, show='*')
entry_password.pack(pady=5)

start_button = tk.Button(root, text='Iniciar Reboot', command=start_reboot)
start_button.pack(pady=10)

result_text = tk.Text(root, height=10, width=50)
result_text.pack(pady=10)

comando_reboot = 'reboot'
antenas = []
result_queue = queue.Queue()

root.mainloop()
