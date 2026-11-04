from database import get_connection
from security import verificar_senha

MSG_INVALIDO = "E-mail ou senha incorretos."


def autenticar(email: str, senha: str, tipo: str):
    """Retorna (dados_do_usuario, None) se der certo, ou (None, mensagem_de_erro)."""
    if tipo not in ("aacd", "fabricante"):
        return None, "Tipo de login inválido."

    conn = get_connection()
    try:
        cursor = conn.cursor(dictionary=True)

        # 1) busca o usuário pelo e-mail e pelo tipo do portal
        cursor.execute(
            """SELECT id_usuario, nome_usuario, email, senha_usuario, tipo, status_usuario
               FROM usuario
               WHERE email = %s AND tipo = %s""",
            (email, tipo),
        )
        usuario = cursor.fetchone()

        # mensagem genérica: não revela se o e-mail existe ou não
        if not usuario or not verificar_senha(senha, usuario["senha_usuario"]):
            return None, MSG_INVALIDO

        if usuario["status_usuario"] != "ativo":
            return None, "Usuário inativo. Entre em contato com o administrador."

        dados = {
            "id_usuario": usuario["id_usuario"],
            "nome": usuario["nome_usuario"],
            "email": usuario["email"],
            "tipo": tipo,
        }

        # 2) confere o vínculo na tabela específica
        if tipo == "aacd":
            cursor.execute(
                """SELECT f.id_funcionario_aacd, f.cargo,
                          u.id_unidade, u.nome_unidade
                   FROM aacd_funcionario f
                   JOIN unidade_aacd u ON u.id_unidade = f.id_unidade
                   WHERE f.id_usuario = %s AND u.status_unidade = 'ativo'""",
                (usuario["id_usuario"],),
            )
            vinculo = cursor.fetchone()
            if not vinculo:
                return None, "Seu usuário não está vinculado a uma unidade AACD ativa."
            dados["vinculo"] = vinculo
            dados["redirect"] = "dashboard-aacd.html"

        else:  # fabricante
            cursor.execute(
                """SELECT fu.id_fabricante_usuario, fu.cargo, fu.administrador,
                          fb.id_fabricante, fb.razao_social
                   FROM fabricante_usuario fu
                   JOIN fabricante fb ON fb.id_fabricante = fu.id_fabricante
                   WHERE fu.id_usuario = %s""",
                (usuario["id_usuario"],),
            )
            vinculos = cursor.fetchall()
            if not vinculos:
                return None, "Seu usuário não está vinculado a nenhum fabricante."
            for v in vinculos:
                v["administrador"] = bool(v["administrador"])
            dados["vinculos"] = vinculos  # um usuário pode ter vários fabricantes
            dados["redirect"] = "dashboard-fabricante.html"

        return dados, None
    finally:
        conn.close()