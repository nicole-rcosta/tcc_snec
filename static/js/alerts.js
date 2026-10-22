function mostrarAlerta(mensagem,estado, link_botao, texto_botao) {
  const alertOverlay = document.createElement("div");
  alertOverlay.classList.add("alert-overlay");

  if (estado == 'success'){
    alertOverlay.innerHTML = `
    <div class="alert-container-success">
      <div class="alert-content-success">
        <img class="alert-icon-wrapper-success" src="/static/img/icons/check_icon.png" alt="">
        <p class="alert-message-success">${mensagem}</p>
        <a href="${link_botao}">
          <button class="alert-button-success">${texto_botao}</button>
        </a> 
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
        <p class="alert-message-error">${mensagem}</p>
        <a href="${link_botao}">
          <button class="alert-button-error">${texto_botao}</button>
        </a>
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