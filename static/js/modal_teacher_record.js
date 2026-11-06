const modalSobrescrever = document.getElementById('modal-sobrescrever');

if (modalSobrescrever) {
  const fechar = () => modalSobrescrever.classList.remove('ativo');

  document.getElementById('confirmarSobrescrever').addEventListener('click', fechar);
}