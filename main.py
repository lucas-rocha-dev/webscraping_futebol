import subprocess

scripts = ["full_serie_a_ws.py",
           "full_serie_b_ws.py",
          "full_premier_ws.py",
          "full_la_liga_ws.py",
           "artilharia_la_liga_ws.py"]




for script in scripts:
    try:
        subprocess.run(["python", script], check=True)
        print(f'{script} executado com sucesso!')     
                            
    except subprocess.CalledProcessError as e:
        print(f'Erro ao executar o {script}: {e}')
print('processos serie a concluidos')        




print('Deu tudo certo, todos scripts finalizados!')  