# =============================================================================
# QUESTÃO 6.1 - PREVISÃO DE DEMANDA
# Produto: Bússola de Bordo 702
# Modelo: Média móvel dos últimos 3 meses
# =============================================================================

import os
from datetime import date

import psycopg2


# =============================================================================
# CONFIGURAÇÃO DO BANCO
# =============================================================================

# A senha é obtida por variável de ambiente para não ficar exposta no código.
DB_CONFIG = {
    "host": "localhost",
    "port": 5432,
    "database": "postgres",
    "user": "postgres",
    "password": os.getenv("LIGHTHOUSE_DB_PASSWORD"),
}


# =============================================================================
# CONSULTA DOS DADOS
# =============================================================================

# Busca o dataset mensal previamente construído no schema staging.
QUERY = """
    SELECT
        mes,
        quantidade_vendida
    FROM staging.demanda_bussola_702
    WHERE mes <= DATE '2026-03-01'
    ORDER BY mes;
"""


# =============================================================================
# FUNÇÃO PRINCIPAL
# =============================================================================

def main():

    # Valida se a senha do banco foi configurada.
    if not DB_CONFIG["password"]:
        raise RuntimeError(
            "A variável LIGHTHOUSE_DB_PASSWORD não foi configurada."
        )

    # Conecta ao PostgreSQL.
    conexao = psycopg2.connect(**DB_CONFIG)

    try:

        cursor = conexao.cursor()

        # Carrega os dados mensais preparados no staging.
        cursor.execute(QUERY)

        registros = cursor.fetchall()

        cursor.close()

    finally:

        # Encerra a conexão com o banco.
        conexao.close()


    # =========================================================================
    # ORGANIZAÇÃO DOS DADOS
    # =========================================================================

    # Converte o resultado da consulta para um dicionário por mês.
    vendas = {
        mes: float(quantidade)
        for mes, quantidade in registros
    }


    # =========================================================================
    # DEFINIÇÃO DOS PERÍODOS
    # =========================================================================

    # O treinamento utiliza dados disponíveis até dezembro de 2025.
    data_limite_treino = date(2025, 12, 1)

    # O teste corresponde aos três primeiros meses de 2026.
    periodo_teste = [
        date(2026, 1, 1),
        date(2026, 2, 1),
        date(2026, 3, 1),
    ]


    # =========================================================================
    # PREPARAÇÃO DO HISTÓRICO
    # =========================================================================

    # Mantém somente os dados anteriores ao período de teste.
    historico = {
        mes: quantidade
        for mes, quantidade in vendas.items()
        if mes <= data_limite_treino
    }


    # =========================================================================
    # PREVISÃO COM MÉDIA MÓVEL DE 3 MESES
    # =========================================================================

    previsoes = {}

    for mes in periodo_teste:

        # Obtém os meses imediatamente anteriores ao mês previsto.
        meses_anteriores = sorted(
            mes_anterior
            for mes_anterior in historico
            if mes_anterior < mes
        )[-3:]


        # Garante que existam três meses disponíveis para a previsão.
        if len(meses_anteriores) < 3:
            raise RuntimeError(
                f"Não existem três meses anteriores disponíveis para "
                f"a previsão de {mes}."
            )


        # Calcula a média dos três meses anteriores.
        previsao = (
            sum(historico[mes_anterior] for mes_anterior in meses_anteriores)
            / 3
        )


        # Armazena a previsão do mês.
        previsoes[mes] = previsao


        # Adiciona a previsão ao histórico para a próxima previsão.
        #
        # Dessa forma:
        # Janeiro usa out/nov/dez de 2025.
        # Fevereiro usa nov/dez e a previsão de janeiro.
        # Março usa dez e as previsões de janeiro e fevereiro.
        historico[mes] = previsao


    # =========================================================================
    # COMPARAÇÃO ENTRE REAL E PREVISTO
    # =========================================================================

    resultados = []

    for mes in periodo_teste:

        venda_real = vendas.get(mes, 0)

        previsao = previsoes[mes]

        erro_absoluto = abs(
            venda_real - previsao
        )

        resultados.append(
            {
                "mes": mes,
                "venda_real": venda_real,
                "previsao": previsao,
                "erro_absoluto": erro_absoluto,
            }
        )


    # =========================================================================
    # CÁLCULO DO MAE
    # =========================================================================

    # O MAE corresponde à média dos erros absolutos do período de teste.
    mae = (
        sum(resultado["erro_absoluto"] for resultado in resultados)
        / len(resultados)
    )


    # =========================================================================
    # APRESENTAÇÃO DOS RESULTADOS
    # =========================================================================

    print("=" * 70)
    print("PREVISÃO DE DEMANDA - BÚSSOLA DE BORDO 702")
    print("=" * 70)

    print()
    print("Período de treino: até 31/12/2025")
    print("Período de teste : 01/01/2026 a 31/03/2026")
    print("Modelo           : Média móvel dos últimos 3 meses")
    print()

    print(
        f"{'Mês':<15}"
        f"{'Real':>15}"
        f"{'Previsão':>15}"
        f"{'Erro absoluto':>18}"
    )

    print("-" * 63)

    for resultado in resultados:

        print(
            f"{resultado['mes'].strftime('%m/%Y'):<15}"
            f"{resultado['venda_real']:>15.2f}"
            f"{resultado['previsao']:>15.2f}"
            f"{resultado['erro_absoluto']:>18.2f}"
        )

    print("-" * 63)

    print(
        f"{'MAE':<15}"
        f"{mae:>15.2f}"
    )

    print()
    print("=" * 70)


# =============================================================================
# PONTO DE ENTRADA
# =============================================================================

if __name__ == "__main__":
    main()
