const inputs = document.querySelectorAll('.insert-code__input--digit');

inputs.forEach((input, index) => {

  input.addEventListener('input', (e) => {
    const value = e.target.value;
    
    if (value && index < inputs.length - 1) {
      inputs[index + 1].focus(); 
    }
  });

  // Faz a tecla Backspace voltar ao input anterior ao apagar
  input.addEventListener('keydown', (e) => {
    if (e.key === 'Backspace' && !input.value && index > 0) {
      inputs[index - 1].focus(); // Volta para o campo anterior
    }
  });

  //permite ctrl V 
  input.addEventListener('paste', (e) => {
    e.preventDefault();
    const pasteData = e.clipboardData.getData('text').trim();

    // se o texto colado for numérico
    if (pasteData) {
      const digits = pasteData.slice(0, inputs.length).split('');
      
      digits.forEach((char, i) => {
        if (inputs[i]) {
          inputs[i].value = char;
        }
      });

      // foca no último campo preenchido 
      const nextFocusIndex = Math.min(digits.length, inputs.length - 1);
      inputs[nextFocusIndex].focus();
    }
  });
});