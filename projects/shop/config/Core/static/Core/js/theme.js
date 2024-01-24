const btnChangeTheme = document.querySelector('#btn-change-theme');
btnChangeTheme.addEventListener('click', () => setTheme(!isLightTheme()));

function isLightTheme() {
    return localStorage.getItem('theme') === 'true';
}

function setTheme(isLight) {
    const theme = isLight ? 'light' : 'dark';
    btnChangeTheme.src = isLight ? '/static/Core/img/sun.png' : '/static/Core/img/moon.png';
    document.body.setAttribute('data-bs-theme', theme);
    localStorage.setItem('theme', isLight);
}

setTheme(isLightTheme());