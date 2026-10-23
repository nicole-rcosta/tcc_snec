const inputArquivoExcel = document.getElementById('arquivo-excel');
const nomeArquivoExcel = document.getElementById('nome-arquivo-excel');

inputArquivoExcel.addEventListener('change', function() {
if (this.files && this.files.length > 0) {
    nomeArquivoExcel.textContent = this.files[0].name;
} else {
    nomeArquivoExcel.textContent = 'Nenhum arquivo selecionado';
}
});

const inputArquivoCsv = document.getElementById('arquivo-csv');
const nomeArquivoCsv = document.getElementById('nome-arquivo-csv');

inputArquivoCsv.addEventListener('change', function() {
if (this.files && this.files.length > 0) {
    nomeArquivoCsv.textContent = this.files[0].name;
} else {
    nomeArquivoCsv.textContent = 'Nenhum arquivo selecionado';
}
});


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