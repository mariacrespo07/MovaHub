import json
import mimetypes
import secrets
import time
from http.cookies import SimpleCookie
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

from auth_service import autenticar
from config import HOST, PORT, SESSAO_DURACAO

# Estruturas em memória para controle de sessão e rate limiting
SESSOES = {}
TENTATIVAS = {}
MAX_TENTATIVAS = 5
JANELA = 300  # 5 minutos em segundos

# raiz do projeto (a pasta acima de backend/), onde ficam os HTML do front
RAIZ_DIR = Path(__file__).resolve().parent.parent

# só estes tipos de arquivo podem ser entregues ao navegador
EXTENSOES_PERMITIDAS = {
    ".html", ".css", ".js",
    ".png", ".jpg", ".jpeg", ".gif", ".webp", ".svg", ".ico",
    ".woff", ".woff2", ".ttf",
}

# pastas que nunca devem ser acessadas pelo navegador
PASTAS_BLOQUEADAS = {"backend", "sql", ".git", "__pycache__", "node_modules", "app"}


def excedeu_tentativas(ip: str) -> bool:
    agora = time.time()
    recentes = [t for t in TENTATIVAS.get(ip, []) if agora - t < JANELA]
    TENTATIVAS[ip] = recentes
    return len(recentes) >= MAX_TENTATIVAS


class Handler(BaseHTTPRequestHandler):

    # ---------- utilitários ----------
    def _json(self, status, corpo, headers=None):
        dados = json.dumps(corpo, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(dados)))
        for k, v in (headers or {}).items():
            self.send_header(k, v)
        self.end_headers()
        self.wfile.write(dados)

    def _sessao_atual(self):
        cookie = SimpleCookie(self.headers.get("Cookie", ""))
        if "sessao" not in cookie:
            return None, None
        token = cookie["sessao"].value
        sessao = SESSOES.get(token)
        if not sessao or sessao["expira"] < time.time():
            SESSOES.pop(token, None)
            return None, None
        return token, sessao

    # ---------- GET ----------
    def do_GET(self):
        caminho = self.path.split("?")[0]

        if caminho == "/api/me":
            _, sessao = self._sessao_atual()
            if not sessao:
                return self._json(401, {"erro": "Não autenticado."})
            return self._json(200, sessao["dados"])

        self._servir_arquivo(caminho)

    def _servir_arquivo(self, caminho):
        if caminho == "/":
            caminho = "/index.html"

        # decodifica %20 etc. e monta o caminho dentro da raiz
        from urllib.parse import unquote
        caminho = unquote(caminho)
        arquivo = (RAIZ_DIR / caminho.lstrip("/")).resolve()

        # 1) precisa estar dentro da raiz do projeto ou em suas subpastas permitidas
        if RAIZ_DIR not in arquivo.parents and arquivo != RAIZ_DIR:
            return self.send_error(404, "Arquivo não encontrado")

        # 2) não pode estar em pasta bloqueada nem ser arquivo oculto (.gitignore, .env...)
        partes = arquivo.relative_to(RAIZ_DIR).parts
        if any(p in PASTAS_BLOQUEADAS or p.startswith(".") for p in partes):
            return self.send_error(404, "Arquivo não encontrado")

        # 3) só extensões permitidas
        if arquivo.suffix.lower() not in EXTENSOES_PERMITIDAS or not arquivo.is_file():
            return self.send_error(404, "Arquivo não encontrado")

        tipo, _ = mimetypes.guess_type(str(arquivo))
        conteudo = arquivo.read_bytes()
        self.send_response(200)
        self.send_header("Content-Type", tipo or "application/octet-stream")
        self.send_header("Content-Length", str(len(conteudo)))
        self.end_headers()
        self.wfile.write(conteudo)

    # ---------- POST ----------
    def do_POST(self):
        if self.path == "/api/login":
            return self._login()
        if self.path == "/api/logout":
            return self._logout()
        self._json(404, {"erro": "Rota não encontrada."})

    def _login(self):
        ip = self.client_address[0]
        if excedeu_tentativas(ip):
            return self._json(429, {"erro": "Muitas tentativas. Aguarde alguns minutos."})

        try:
            tamanho = int(self.headers.get("Content-Length", 0))
            if tamanho <= 0 or tamanho > 10_000:
                raise ValueError
            corpo = json.loads(self.rfile.read(tamanho))
            email = str(corpo.get("email", "")).strip().lower()
            senha = str(corpo.get("senha", ""))
            tipo = str(corpo.get("tipo", ""))
        except (ValueError, json.JSONDecodeError):
            return self._json(400, {"erro": "Requisição inválida."})

        if not email or not senha:
            return self._json(400, {"erro": "Informe e-mail e senha."})

        try:
            dados, erro = autenticar(email, senha, tipo)
        except Exception as e:  # erro de banco, etc.
            print("Erro no login:", e)
            return self._json(500, {"erro": "Erro interno. Tente novamente."})

        if erro:
            TENTATIVAS.setdefault(ip, []).append(time.time())
            return self._json(401, {"erro": erro})

        TENTATIVAS.pop(ip, None)
        token = secrets.token_urlsafe(32)
        SESSOES[token] = {"dados": dados, "expira": time.time() + SESSAO_DURACAO}

        cookie = (f"sessao={token}; HttpOnly; SameSite=Strict; Path=/; "
                  f"Max-Age={SESSAO_DURACAO}")
        self._json(200, {"ok": True, "redirect": dados["redirect"], "nome": dados["nome"]},
                   headers={"Set-Cookie": cookie})

    def _logout(self):
        token, _ = self._sessao_atual()
        if token:
            SESSOES.pop(token, None)
        self._json(200, {"ok": True},
                   headers={"Set-Cookie": "sessao=; HttpOnly; Path=/; Max-Age=0"})


if __name__ == "__main__":
    print("Raiz do projeto:", RAIZ_DIR)
    servidor = ThreadingHTTPServer((HOST, PORT), Handler)
    print(f"Servidor rodando em http://{HOST}:{PORT}")
    try:
        servidor.serve_forever()
    except KeyboardInterrupt:
        print("\nServidor encerrado.")