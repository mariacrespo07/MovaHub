const form = document.getElementById("formLogin");
const campoSenha = document.getElementById("senha");
const btnOlho = document.getElementById("btnOlho");

// Mostrar / esconder senha
btnOlho.addEventListener("click", () => {
  const estaOculta = campoSenha.type === "password";
  campoSenha.type = estaOculta ? "text" : "password";

  const icone = btnOlho.querySelector("i");
  icone.className = estaOculta ? "bi bi-eye-slash" : "bi bi-eye";
});

// Validação do formulário
form.addEventListener("submit", (evento) => {
  evento.preventDefault();

  // Marca os campos inválidos em vermelho
  form.querySelectorAll(".campo").forEach((campo) => {
    campo.classList.toggle("is-invalid", !campo.checkValidity());
  });

  if (!form.checkValidity()) return;

  // Aqui entra a ligação com o back-end quando ele existir.
  // Por enquanto, só mostra uma mensagem de teste.
  alert("Login enviado! (falta conectar ao back-end)");
});