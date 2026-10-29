document.addEventListener('DOMContentLoaded', () => {
    // Elementos da tela e do modal
    const btnContinuar = document.querySelector('.activities__button--continue');
    const modal = document.querySelector('#modal-confirmacao'); // Ajuste o ID do seu modal
    const btnConfirmarModal = document.querySelector('#btn-confirmar-modal'); // Botão dentro do modal
    
    const modalQtdAlunos = document.querySelector('#modal-qtd-alunos');
    const modalListaAlunos = document.querySelector('#modal-lista-alunos');

    // 1. Ação ao clicar em "Continuar" (Abre o Modal e preenche os dados)
    btnContinuar.addEventListener('click', (event) => {
        event.preventDefault(); // Impede o envio tradicional do formulário

        // Pega a quantidade de alunos digitada
        const qtdAlunos = document.querySelector('#students-count').value;
        modalQtdAlunos.textContent = qtdAlunos;

        // Limpa a lista do modal antes de preencher
        modalListaAlunos.innerHTML = '';

        // Busca todas as linhas da tabela onde o checkbox está MARCADO
        const checkboxesMarcados = document.querySelectorAll('.activities__table-row input[type="checkbox"]:checked');

        if (checkboxesMarcados.length === 0) {
            modalListaAlunos.innerHTML = '<li>Nenhum aluno de contraturno selecionado.</li>';
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
        const rmsAtendidos = Array.from(
            document.querySelectorAll('.activities__table-row input[type="checkbox"]:checked')
        ).map(cb => cb.value);

        const idTurma = modal.dataset.idTurma; // ID da turma salvo num data-attribute ou obtido da URL

        try {
            const response = await fetch(`/teacher/class_info/save/${idTurma}`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    quantidade_alunos: qtdAlunos,
                    rms_atendidos: rmsAtendidos
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