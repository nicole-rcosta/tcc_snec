document.addEventListener('DOMContentLoaded', () => {
    const themeBtn = document.getElementById('themeToggleBtn');
    const themeIcon = document.getElementById('themeIcon');
    const htmlElement = document.documentElement;

    // Função para aplicar o tema e atualizar o ícone
    function applyTheme(theme) {
        htmlElement.setAttribute('data-theme', theme);
        htmlElement.style.colorScheme = theme;
        localStorage.setItem('app-theme', theme);

        if (theme === 'dark') {
            themeIcon.className = 'bi bi-sun-fill';
        } else {
            themeIcon.className = 'bi bi-moon-fill';
        }
    }

    // Carrega o tema salvo ou usa o padrão ('light')
    const savedTheme = localStorage.getItem('app-theme') || 'light';
    applyTheme(savedTheme);

    // Evento do clique no botão
    if (themeBtn) {
        themeBtn.addEventListener('click', () => {
            const currentTheme = htmlElement.getAttribute('data-theme');
            const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
            applyTheme(newTheme);
        });
    }
});