const selectTurma = document.getElementById('student-activity');
const inputPeriodo = document.getElementById('student-period');

selectTurma.addEventListener('change', function() {
    // Pega a opção que está selecionada no momento
    const opcaoSelecionada = this.options[this.selectedIndex];
    
    // Obtém o valor do atributo data-periodo (retorna null se não existir)
    const periodo = opcaoSelecionada.getAttribute('data-periodo') || '';
    
    // Preenche o input
    inputPeriodo.value = periodo;
});