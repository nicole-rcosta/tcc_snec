const inputs = document.querySelectorAll('.insert-code__input--digit');

  inputs.forEach((input, index) => {
    // Digitou algo → vai pro próximo
    input.addEventListener('input', () => {
      // mantém só números
      input.value = input.value.replace(/\D/g, '');

      if (input.value && index < inputs.length - 1) {
        inputs[index + 1].focus();
      }
    });

    // Backspace em campo vazio → volta pro anterior
    input.addEventListener('keydown', (e) => {
      if (e.key === 'Backspace' && !input.value && index > 0) {
        inputs[index - 1].focus();
      }
    });

    // Seleciona o conteúdo ao focar (facilita sobrescrever)
    input.addEventListener('focus', () => input.select());
  });

  // Colar o código inteiro (ex: "12345") distribui pelos campos
  inputs[0].addEventListener('paste', (e) => {
    e.preventDefault();
    const digits = (e.clipboardData.getData('text') || '')
      .replace(/\D/g, '')
      .slice(0, inputs.length);

    digits.split('').forEach((digit, i) => {
      inputs[i].value = digit;
    });

    // foca no próximo campo vazio, ou no último se completou
    inputs[Math.min(digits.length, inputs.length - 1)].focus();
  });