import psycopg2

def connection():
    try:
        conn = psycopg2.connect(
            database="portal_energia",
            user="postgres",
            host='localhost',
            password="12345678",
            port=5432
        )
        return conn
    except psycopg2.Error as e:
        raise Exception(f"Erro de Conexão com o Banco de Dados: {e}")


def cadastrar_usuario_db(p_usuario, p_nome, p_email, p_senha, p_tipo_usuario, p_cpf, p_cnpj):
    conn = None
    try:
        conn = connection()
        cur = conn.cursor()
        p_tipo_permissao = "BASICO"
        cur.execute("CALL CadastrarNovoUsuarioCompleto(%s, %s, %s, %s, %s, %s, %s, %s, %s);",
                    (p_usuario, p_nome, p_email, p_senha, p_tipo_usuario,
                     p_tipo_permissao, p_cpf, p_cnpj, None))
        conn.commit()
        conn.close()
        return (True, "Usuário cadastrado com sucesso!")
    except Exception as e:
        conn.rollback()
        conn.close()
        return (False, f"Erro ao cadastrar usuário:\n{e}")


def cadastrar_imovel_db(rua, numero, bairro, cidade, estado, cep, concessionaria, status_reg, tipo_imovel, id_usuario):
    conn = None
    try:
        conn = connection()
        cur = conn.cursor()
        cur.execute("""
                    INSERT INTO LOCALIZACAO (rua, numero, bairro, cidade, estado, cep)
                    VALUES (%s, %s, %s, %s, %s, %s) RETURNING id_loc;
                    """, (rua, numero, bairro, cidade, estado, cep))
        id_loc = cur.fetchone()[0]

        cur.execute("""
                    INSERT INTO IMOVEL (concessionaria, status_reg, tipo, id_loc)
                    VALUES (%s, %s, %s, %s) RETURNING id_imovel;
                    """, (concessionaria, status_reg, tipo_imovel, id_loc))
        id_imovel = cur.fetchone()[0]

        cur.execute("""
                    INSERT INTO USUARIO_IMOVEL (id_usuario, id_imovel)
                    VALUES (%s, %s);
                    """, (id_usuario, id_imovel))

        conn.commit()
        conn.close()
        return (True, f"Imóvel (ID: {id_imovel}) adicionado ao usuário {id_usuario} com sucesso!")
    except Exception as e:
        conn.rollback()
        conn.close()
        return (False, f"Erro ao adicionar imóvel:\n{e}")


def listar_imoveis_db():
    conn = None
    try:
        conn = connection()
        cur = conn.cursor()
        cur.execute("SELECT id_usuario, usuario FROM USUARIO;")
        usuarios = cur.fetchall()

        if not usuarios:
            return (True, ["Nenhum usuário encontrado no sistema!"])

        linhas_resultado = ["Imóveis por Usuário"]
        for id_usuario, nome_usuario in usuarios:
            cur.execute("SELECT ContarImoveisPorUsuario(%s);", (id_usuario,))
            total_imoveis = cur.fetchone()[0]
            linhas_resultado.append(f"ID: {id_usuario} do usuário: {nome_usuario}. Possui {total_imoveis} imóvel(is)")
        conn.close()
        return (True, linhas_resultado)

    except Exception as e:
        conn.close()
        return (False, [f"Erro ao listar imóveis:\n{e}"])
