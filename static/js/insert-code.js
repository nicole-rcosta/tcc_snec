const inputs = document.querySelectorAll('.insert-code__input--digit');

  inputs.forEach((input, index) => {
    // digitou algo vai pro próximo
    input.addEventListener('input', () => {
      // permite só números
      input.value = input.value.replace(/\D/g, '');

      if (input.value && index < inputs.length - 1) {
        inputs[index + 1].focus();
      }
    });

    // backspace em campo vazio  volta pro anterior
    input.addEventListener('keydown', (e) => {
      if (e.key === 'Backspace' && !input.value && index > 0) {
        inputs[index - 1].focus();
      }
    });

    // seleciona o conteúdo ao focar (facilita sobrescrever)
    input.addEventListener('focus', () => input.select());
  });

  // permite control v
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

// faz com que os 5 inputs retornem apenas 1 código 

const form = document.querySelector('.insert-code__container');
const codigoCompleto = document.querySelector('#codigo-completo');

form.addEventListener('submit', (event) => {
    const codigo = Array.from(inputs)
        .map(input => input.value)
        .join('');

    // impede o envio se não houver cinco dígitos
    if (codigo.length !== 5) {
        event.preventDefault();
        alert('Digite os 5 dígitos do código.');
        return;
    }

    // junta os cinco inputs em um único valor
    codigoCompleto.value = codigo; 
// 
});
