const form = document.getElementById('formLogin');
const campoEmail = document.getElementById('email');
const campoSenha = document.getElementById('senha');
const btnOlho = document.getElementById('btnOlho');
const btnEntrar = form.querySelector('.btn-entrar');

// caixa de mensagem criada via JS (serve para erro e para sucesso)
const caixaMsg = document.createElement('div');
caixaMsg.className = 'alert d-none';
caixaMsg.setAttribute('role', 'alert');
btnEntrar.before(caixaMsg);

btnOlho.addEventListener('click', () => {
  const mostrando = campoSenha.type === 'text';
  campoSenha.type = mostrando ? 'password' : 'text';
  btnOlho.querySelector('i').className = mostrando ? 'bi bi-eye' : 'bi bi-eye-slash';
});

function mostrarMensagem(msg, tipo) {
  caixaMsg.textContent = msg;
  caixaMsg.className = `alert alert-${tipo}`; // 'danger' ou 'success'
}

function esconderMensagem() {
  caixaMsg.classList.add('d-none');
}

form.addEventListener('submit', async (e) => {
  e.preventDefault();
  esconderMensagem();

  const emailOk = campoEmail.checkValidity();
  const senhaOk = campoSenha.checkValidity();
  campoEmail.classList.toggle('is-invalid', !emailOk);
  campoSenha.classList.toggle('is-invalid', !senhaOk);
  if (!emailOk || !senhaOk) return;

  btnEntrar.disabled = true;
  btnEntrar.textContent = 'Entrando...';

  let loginOk = false;

  try {
    const resposta = await fetch('/api/login', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        email: campoEmail.value.trim(),
        senha: campoSenha.value,
        tipo: form.dataset.tipo
      })
    });

    let dados;
    try {
      dados = await resposta.json();
    } catch {
      mostrarMensagem(`Resposta inesperada (HTTP ${resposta.status}). Abra a página por http://127.0.0.1:8000.`, 'danger');
      return;
    }

    if (resposta.ok) {
      loginOk = true;
      mostrarMensagem(`Login efetuado com sucesso! Bem-vindo(a), ${dados.nome}.`, 'success');
      btnEntrar.textContent = 'Redirecionando...';
      setTimeout(() => {
        window.location.href = dados.redirect;
      }, 1500);
    } else {
      mostrarMensagem(dados.erro || 'Não foi possível entrar.', 'danger');
    }
  } catch (err) {
    console.error(err);
    mostrarMensagem('Não foi possível conectar ao servidor. Ele está rodando?', 'danger');
  } finally {
    // em caso de sucesso, o botão fica travado até o redirecionamento
    if (!loginOk) {
      btnEntrar.disabled = false;
      btnEntrar.textContent = 'Entrar na plataforma';
    }
  }
});