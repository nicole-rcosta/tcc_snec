const abrirModal = document.getElementById('abrirModal')

abrirModal.addEventListener('click', ()=>{
    modal.classList.add('ativo')
})


const modal = document.getElementById('modal');
const fecharBtn = document.getElementById('fecharBtn');

function fecharModal() {
  modal.classList.remove('ativo'); // O CSS faz o fade-out sozinho a partir daqui
}

fecharBtn.addEventListener('click', fecharModal);

modal.addEventListener('click', function(event) {
  if (event.target === modal) {
    fecharModal();
  }
});



document.addEventListener('keydown', function(event) {

  if (event.key === 'Escape') {
    fecharModal()
  }
});