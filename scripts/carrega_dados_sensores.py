import os
from datetime import datetime
import csv
import oracledb

# Função para conectar ao banco Oracle usando variáveis de ambiente
def connect_to_oracle():
    user = os.getenv('GAIA_DB_USER')
    password = os.getenv('GAIA_DB_PASSWORD')
    dsn = os.getenv('GAIA_DB_DSN')

    if not user or not password or not dsn:
        raise EnvironmentError("As variáveis de ambiente GAIA_DB_USER, GAIA_DB_PASSWORD e GAIA_DB_DSN devem estar definidas.")

    conn = oracledb.connect(
        user=user,
        password=password,
        dsn=dsn
    )
    return conn

# Função para carregar os dados do CSV para o banco de dados
def load_sensor_data(csv_file):
    # Conectar ao banco Oracle
    conn = connect_to_oracle()
    cursor = conn.cursor()

    with open(csv_file, 'r', encoding='utf-8') as file:
        reader = csv.reader(file)
        next(reader)  # Pular o cabeçalho do CSV
        
        for row in reader:
            id_area, id_sensor, dt_leitura, valor, tipo_valor = row

            # Converter a data/hora da string para um objeto datetime
            dt_leitura = datetime.strptime(dt_leitura, "%Y-%m-%d %H:%M")

            # Verificar se o registro já existe na tabela LEITURAS_SENSORES
            cursor.execute("""
                SELECT COUNT(*) FROM leituras_sensores
                WHERE id_area = :id_area AND id_sensor = :id_sensor AND dt_leitura = :dt_leitura
            """, {'id_area': id_area, 'id_sensor': id_sensor, 'dt_leitura': dt_leitura})

            exists = cursor.fetchone()[0]

            if exists:
                # Se já existir, atualiza o registro
                cursor.execute("""
                    UPDATE leituras_sensores
                    SET valor = :valor, tipo_valor = :tipo_valor
                    WHERE id_area = :id_area AND id_sensor = :id_sensor AND dt_leitura = :dt_leitura
                """, {
                    'valor': valor, 'tipo_valor': tipo_valor,
                    'id_area': id_area, 'id_sensor': id_sensor, 'dt_leitura': dt_leitura
                })
            else:
                # Se não existir, insere o novo registro
                cursor.execute("""
                    INSERT INTO leituras_sensores (id_area, id_sensor, dt_leitura, valor, tipo_valor)
                    VALUES (:id_area, :id_sensor, :dt_leitura, :valor, :tipo_valor)
                """, {
                    'id_area': id_area, 'id_sensor': id_sensor, 'dt_leitura': dt_leitura,
                    'valor': valor, 'tipo_valor': tipo_valor
                })

    # Confirmar as alterações no banco de dados
    conn.commit()

    # Fechar a conexão com o banco
    cursor.close()
    conn.close()

    print("Dados carregados com sucesso!")

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print(f"Uso: python ./{os.path.basename(__file__)} <arquivo_csv>")
    else:
        csv_file = sys.argv[1]
        load_sensor_data(csv_file)
