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

document.addEventListener('DOMContentLoaded', () => {
    // Elementos da tela e do modal
    const btnContinuar = document.querySelector('.activities__button--continue');
    const btnConfirmarModal = document.querySelector('.confirmation__button--continue'); // Botão dentro do modal
    
    const modalQtdAlunos = document.querySelector('.confirmation__card-number');
    const modalListaAlunos = document.querySelector('.confirmation__list');

    // 1. Ação ao clicar em "Continuar" (Abre o Modal e preenche os dados)
    btnContinuar.addEventListener('click', (event) => {
        event.preventDefault(); // Impede o envio tradicional do formulário

        // Pega a quantidade de alunos digitada
        const qtdAlunos = document.querySelector('#students-count').value;
        if (qtdAlunos === '') {
            qtdAlunos = 0;
        }
        modalQtdAlunos.textContent = qtdAlunos;

        // Limpa a lista do modal antes de preencher
        modalListaAlunos.innerHTML = '';

        // Busca todas as linhas da tabela onde o checkbox está MARCADO
        const checkboxesMarcados = document.querySelectorAll('.activities__table-cell--check input[type="checkbox"]:checked');

        if (checkboxesMarcados.length === 0) {
            modalListaAlunos.innerHTML = '<li style="color:var(--text-secondary); text-align: center;">Nenhum aluno de contraturno selecionado.</li>';
        } else {
            checkboxesMarcados.forEach(checkbox => {
                // Sobe até a linha (tr) correspondente ao checkbox
                const linha = checkbox.closest('tr');
                const nomeAluno = linha.querySelector('.activities__table-cell--student').textContent;

                // Cria o elemento de lista no modal
                const item = document.createElement('li');
                item.textContent = nomeAluno;
                modalListaAlunos.appendChild(item);
            });
        }

        // Exibe o modal (ajuste para a classe ou estilo de exibição do seu CSS)
        modal.classList.add('ativo');
    });

    // 2. Ação ao clicar em "Confirmar" dentro do Modal (Dispara o fetch)
    btnConfirmarModal.addEventListener('click', async () => {
        const qtdAlunos = document.querySelector('#students-count').value;
        
        // Coleta apenas os RMs marcados
        const rmsContraturno = Array.from(
            document.querySelectorAll('.activities__table-cell--check input[type="checkbox"]:checked')
        ).map(cb => cb.value);
        
        const idTurma = modal.dataset.idTurma

        try {
            const response = await fetch(`/teacher/class_info/save/${idTurma}`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    quantidade_alunos: qtdAlunos,
                    rms_contraturno: rmsContraturno
                })
            });

            const resultado = await response.json();

            if (resultado.sucesso) {
                // Redireciona para a Tela 1 se der tudo certo
                window.location.href = resultado.redirect_url;
            } else {
                alert('Erro ao salvar: ' + resultado.erro);
            }
        } catch (error) {
            console.error('Erro na requisição:', error);
            alert('Falha na comunicação com o servidor.');
        }
    });
});