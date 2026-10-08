function mostrarAlerta(estado) {
  const alertOverlay = document.createElement("div");
  alertOverlay.classList.add("alert-overlay");

  if (estado == 'success'){
    alertOverlay.innerHTML = `
    <div class="alert-container-success">
      <div class="alert-content-success">
        <img class="alert-icon-wrapper-success" src="/static/img/icons/check_icon.png" alt="">
        <p class="alert-message-success">Senha alterada <br> com sucesso</p>
        <button class="alert-button-success">Voltar</button>
      </div>
    </div>
`;

  // Adiciona o evento de fechar no botão
  const button = alertOverlay.querySelector(".alert-button-success");
  button.addEventListener("click", () => {
    alertOverlay.remove();
  });

  document.body.appendChild(alertOverlay);
}else if (estado == 'error'){
    alertOverlay.innerHTML = `
    <div class="alert-container-error">
    <div class="alert-content-error">
        <img class="alert-icon-wrapper-error" src="/static/img/icons/error_icon.png" alt="">
        <p class="alert-message-error">
            Todos os campos<br>
            obrigatórios
        </p>
        <button class="alert-button-error">Voltar</button>
    </div>
</div>
`;

  // Adiciona o evento de fechar no botão
  const button = alertOverlay.querySelector(".alert-button-error");
  button.addEventListener("click", () => {
    alertOverlay.remove();
  });

  document.body.appendChild(alertOverlay);
    
}
};