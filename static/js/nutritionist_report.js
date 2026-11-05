document.addEventListener("DOMContentLoaded", () => {
    // Carrega a lista quando a página termina de abrir
    carregarAlunosAlmoco();
});

/**
 * Busca via API REST os alunos previstos para o dia atual no contraturno
 * e preenche dinamicamente a tabela do relatório.
 */
async function carregarAlunosAlmoco() {
    try {
        const response = await fetch('/api/nutri/alunos-almoco');
        const dados = await response.json();

        // Atualiza os contadores no HTML se os elementos existirem
        const totalElement = document.getElementById('total-almoco');
        const totalElementDashboard = document.getElementById('total-almoco-dashboard');
        const dataElement = document.getElementById('data-hoje');

        if (totalElement) totalElement.innerText = dados.total_dia;
        if (dataElement) dataElement.innerText = `Informação Referente ao dia: ${dados.data_hoje}`;

        const tbody = document.getElementById('tabela-alunos-body');
        if (!tbody) return;

        tbody.innerHTML = '';

        if (!dados.alunos || dados.alunos.length === 0) {
            tbody.innerHTML = `
                <tr class="dashboard__table-row">
                    <td colspan="5" style="text-align: center; padding: 1.5rem; color: var(--color-red)">
                        Nenhum aluno cadastrado no contraturno para hoje.
                    </td>
                </tr>`;
            return;
        }

        // Renderiza cada linha mantendo os padrões e classes CSS BEM do seu grupo
        dados.alunos.forEach(aluno => {
            const tr = document.createElement('tr');
            tr.className = 'dashboard__table-row';

            tr.innerHTML = `
                <td class="dashboard__table-cell--rm" data-label="RM">${aluno.rm}</td>
                <td class="dashboard__table-cell--student" data-label="Aluno">${aluno.aluno}</td>
                <td class="dashboard__table-cell--year" data-label="Ano">${aluno.ano}</td>
                <td class="dashboard__table-cell--activity" data-label="Atividade">${aluno.atividade}</td>
                <td class="dashboard__table-cell--status" data-label="Estado">
                    <label class="dashboard__checkbox-label">
                        <input 
                            type="checkbox" 
                            class="dashboard__checkbox-input" 
                            ${aluno.status ? 'checked' : ''} 
                            onchange="salvarPresenca(${aluno.rm}, this.checked)"
                        />
                        <span class="dashboard__checkbox-custom" aria-hidden="true"></span>

                    </label>
                </td>
            `;
            tbody.appendChild(tr);
        });
    } catch (erro) {
        console.error('Erro ao buscar lista de alunos:', erro);
    }
}

/**
 * Envia o status do checkbox para o Back-end atualizar no MySQL
 * @param {number} rmAluno - Registro Matrícula do Aluno
 * @param {boolean} statusAtendido - True para presente, False para ausente
 */
async function salvarPresenca(rmAluno, statusAtendido) {
    try {
        const response = await fetch('/api/nutri/atualizar-almoco', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                rm: rmAluno,
                atendido: statusAtendido
            })
        });

        const resultado = await response.json();
        if (!resultado.sucesso) {
            alert('Atenção: Não foi possível atualizar o status no banco de dados.');
        }
    } catch (erro) {
        console.error('Erro ao salvar presença:', erro);
    }
}