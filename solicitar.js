const form = document.getElementById("formSolicitar");
const areaForm = document.getElementById("areaForm");
const areaSucesso = document.getElementById("areaSucesso");

// Grupos em que é preciso marcar pelo menos uma opção
const grupos = [
  { nome: "tecnologia", erro: document.getElementById("erroTecnologia") },
  { nome: "material", erro: document.getElementById("erroMaterial") },
];

function grupoTemMarcado(nome) {
  return form.querySelectorAll(`input[name="${nome}"]:checked`).length > 0;
}

// ----- Máscaras -----
document.getElementById("telefone").addEventListener("input", (e) => {
  let n = e.target.value.replace(/\D/g, "").slice(0, 11);
  if (n.length > 10) {
    n = n.replace(/^(\d{2})(\d{5})(\d{4}).*/, "($1) $2-$3");
  } else if (n.length > 6) {
    n = n.replace(/^(\d{2})(\d{4})(\d{0,4}).*/, "($1) $2-$3");
  } else if (n.length > 2) {
    n = n.replace(/^(\d{2})(\d*)/, "($1) $2");
  }
  e.target.value = n;
});

document.getElementById("cnpj").addEventListener("input", (e) => {
  let n = e.target.value.replace(/\D/g, "").slice(0, 14);
  n = n
    .replace(/^(\d{2})(\d)/, "$1.$2")
    .replace(/^(\d{2})\.(\d{3})(\d)/, "$1.$2.$3")
    .replace(/\.(\d{3})(\d)/, ".$1/$2")
    .replace(/(\d{4})(\d)/, "$1-$2");
  e.target.value = n;
});

// Some o erro do grupo assim que a pessoa marca uma opção
grupos.forEach((g) => {
  form.querySelectorAll(`input[name="${g.nome}"]`).forEach((input) => {
    input.addEventListener("change", () => {
      if (grupoTemMarcado(g.nome)) g.erro.classList.remove("mostrar");
    });
  });
});

// ----- Envio -----
form.addEventListener("submit", (evento) => {
  evento.preventDefault();

  // Campos comuns e checkbox dos termos
  form.querySelectorAll(".campo, .form-check-input").forEach((campo) => {
    campo.classList.toggle("is-invalid", !campo.checkValidity());
  });

  // Grupos com várias opções
  let gruposOk = true;
  grupos.forEach((g) => {
    const ok = grupoTemMarcado(g.nome);
    g.erro.classList.toggle("mostrar", !ok);
    if (!ok) gruposOk = false;
  });

  if (!form.checkValidity() || !gruposOk) {
    const primeiroErro = form.querySelector(".is-invalid, .erro-grupo.mostrar");
    if (primeiroErro) primeiroErro.scrollIntoView({ behavior: "smooth", block: "center" });
    return;
  }

  // Reúne os dados (pronto para enviar ao back-end no futuro)
  const dados = {
    nome: form.nome.value,
    email: form.email.value,
    telefone: form.telefone.value,
    tipo: form.tipo.value,
    organizacao: form.organizacao.value,
    cnpj: form.cnpj.value,
    cidade: form.cidade.value,
    impressoras: Number(form.impressoras.value),
    tecnologias: [...form.querySelectorAll('input[name="tecnologia"]:checked')].map((i) => i.value),
    materiais: [...form.querySelectorAll('input[name="material"]:checked')].map((i) => i.value),
    mensagem: form.mensagem.value,
  };
  console.log("Solicitação de acesso:", dados);

  // Aqui entra a ligação com o back-end quando ele existir.
  // Por enquanto, só mostra a tela de sucesso.
  document.getElementById("emailEnviado").textContent = dados.email;
  areaForm.classList.add("d-none");
  areaSucesso.classList.remove("d-none");
  window.scrollTo({ top: 0, behavior: "smooth" });
});