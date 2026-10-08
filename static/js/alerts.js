function mostrarAlerta(imagem, mensagem) {
  const alertOverlay = document.createElement("div");
  alertOverlay.classList.add("alert-overlay");

  alertOverlay.innerHTML = `
    <div class="alert-container">
      <div class="alert-content">
        <img class= 'alert-icon-wrapper' src="/static/img/icons/${imagem}" alt="">
        <p class="alert-message">${mensagem}</p>
        <button class="alert-button">Voltar</button>
      </div>
    </div>
  `;

  // Adiciona o evento de fechar no botão
  const button = alertOverlay.querySelector(".alert-button");
  button.addEventListener("click", () => {
    alertOverlay.remove();
  });

  document.body.appendChild(alertOverlay);
}