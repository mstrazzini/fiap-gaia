"""
Script para carregar dados de sensores de um arquivo CSV para o banco Oracle

Utilização: python sensors_load.py <arquivo_csv>
"""
import csv
import cx_Oracle

def connect_to_oracle():
    """
    Conecta ao banco Oracle e retorna a conexão
    """
    conn = cx_Oracle.connect("usuario", "senha", "host:porta/nome_servico")
    return conn

def load_sensor_data(csv_file):
    """
    Insere ou atualiza os dados de sensores de um arquivo CSV no banco Oracle
    """
    conn = connect_to_oracle()
    cursor = conn.cursor()

    with open(csv_file, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            id_area, id_sensor, data_hora, valor = row
            cursor.execute("""
                MERGE INTO leituras_sensores ls
                USING (SELECT :id_area AS id_area, :id_sensor AS id_sensor, :data_hora AS data_hora FROM dual) src
                ON (ls.id_area = src.id_area AND ls.id_sensor = src.id_sensor AND ls.data_hora = src.data_hora)
                WHEN MATCHED THEN
                    UPDATE SET ls.valor = :valor
                WHEN NOT MATCHED THEN
                    INSERT (id_area, id_sensor, data_hora, valor)
                    VALUES (:id_area, :id_sensor, :data_hora, :valor)
            """, {'id_area': id_area, 'id_sensor': id_sensor, 'data_hora': data_hora, 'valor': valor}
            )

    conn.commit()
    cursor.close()
    conn.close()

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: python script.py <csv_file>")
    else:
        csv_file = sys.argv[1]
        load_sensor_data(csv_file)
