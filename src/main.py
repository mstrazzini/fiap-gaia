import os
from datetime import datetime
import oracledb

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

def exibir_menu():
    print("\n1. Registrar irrigação")
    print("2. Consultar processos de irrigação")
    print("3. Consultar leituras de sensores")
    print("4. Sair")

def registrar_irrigacao(conn):
    cursor = conn.cursor()

    # Solicitar as informações necessárias para registrar uma irrigação
    id_area = input("Digite o ID da área: ")
    data_inicio = input("Digite a data/hora de início (YYYY-MM-DD HH:MM): ")
    data_fim = input("Digite a data/hora de fim (YYYY-MM-DD HH:MM): ")

    # Verificar se a área existe
    cursor.execute("SELECT hectares, cultura FROM areas WHERE id = :id_area", {'id_area': id_area})
    result = cursor.fetchone()
    if not result:
        print("Área não encontrada!")
        return

    hectares, cultura = result

    # Obter o fator de irrigação da cultura
    cursor.execute("SELECT fator FROM fatores_irrigacao WHERE cultura = :cultura", {'cultura': cultura})
    fator_irrigacao = cursor.fetchone()[0]

    # Calcular a quantidade de água necessária
    quantidade_agua = calcular_quantidade_agua(data_inicio, data_fim, hectares, fator_irrigacao)

    # Inserir o processo de irrigação
    cursor.execute("""
        INSERT INTO irrigacoes (id_area, dt_inicio, dt_fim, qtd_agua)
        VALUES (:id_area, TO_TIMESTAMP(:data_inicio, 'YYYY-MM-DD HH24:MI'), TO_TIMESTAMP(:data_fim, 'YYYY-MM-DD HH24:MI'), :qtd_agua)
    """, {
        'id_area': id_area, 
        'data_inicio': data_inicio,
        'data_fim': data_fim,
        'qtd_agua': quantidade_agua
    })

    conn.commit()
    print(f"Irrigação registrada com sucesso! Quantidade de água: {quantidade_agua} litros.")


def consultar_irrigacoes(conn):
    cursor = conn.cursor()

    id_area = input("Digite o ID da área para consulta: ")

    cursor.execute("""
        SELECT dt_inicio, dt_fim, qtd_agua 
        FROM irrigacoes 
        WHERE id_area = :id_area ORDER BY dt_inicio DESC
    """, {'id_area': id_area})

    irrigacoes = cursor.fetchall()
    if not irrigacoes:
        print("Nenhuma irrigação encontrada para esta área.")
        return

    print(f"\nProcessos de Irrigação para a área {id_area}:")
    for irrigacao in irrigacoes:
        print(f"Data Início: {irrigacao[0]}, Data Fim: {irrigacao[1]}, Quantidade de Água: {irrigacao[2]} litros.")

def consultar_leituras_sensores(conn):
    cursor = conn.cursor()

    id_area = input("Digite o ID da área para consulta: ")

    # Consultar as leituras de cada sensor
    for id_sensor in [1, 2, 3]:  # IDs para S1, S2, S3
        cursor.execute("""
            SELECT dt_leitura, valor, tipo_valor 
            FROM leituras_sensores 
            WHERE id_area = :id_area AND id_sensor = :id_sensor
            ORDER BY dt_leitura DESC FETCH FIRST 10 ROWS ONLY
        """, {'id_area': id_area, 'id_sensor': id_sensor})

        leituras = cursor.fetchall()
        print(f"\nLeituras do Sensor {id_sensor} para a área {id_area}:")
        if leituras:
            for leitura in leituras:
                print(f"Data: {leitura[0]}, Valor: {leitura[1]}, Tipo: {leitura[2]}")
        else:
            print(f"Nenhuma leitura encontrada para o sensor {id_sensor}.")

def calcular_quantidade_agua(data_inicio, data_fim, hectares, fator_irrigacao):
    """
    Calcula a quantidade de água necessária para irrigar uma área com base nos hectares e no fator de irrigação.

    - Cada hectare requer 100 litros de água por hora.
    - O fator de irrigação da cultura será aplicado.
    """
    # Convertendo as strings de data/hora para objetos datetime
    inicio = datetime.strptime(data_inicio, "%Y-%m-%d %H:%M")
    fim = datetime.strptime(data_fim, "%Y-%m-%d %H:%M")

    # Calcular a duração da irrigação em horas
    duracao_horas = (fim - inicio).total_seconds() / 3600

    # Quantidade base de água por hectare
    agua_por_hectare_por_hora = 100

    # Calcular a quantidade total de água
    quantidade_agua = hectares * agua_por_hectare_por_hora * duracao_horas * fator_irrigacao
    return quantidade_agua

if __name__ == "__main__":
    conn = connect_to_oracle()

    while True:
        exibir_menu()
        opcao = input("Escolha uma opção: ")
        if opcao == "1":
            registrar_irrigacao(conn)
        elif opcao == "2":
            consultar_irrigacoes(conn)
        elif opcao == "3":
            consultar_leituras_sensores(conn)
        elif opcao == "4":
            print("Saindo...")
            break
        else:
            print("Opção inválida, tente novamente.")

    conn.close()
