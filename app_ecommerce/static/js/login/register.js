const input__text = document.querySelectorAll('.input__container--input');
const form__register = document.querySelector('#form__login__register');
const error__container = document.querySelector('#error__container');
form__register.addEventListener('submit', (e)=>{
    error__container.innerHTML = '';
    let error__input = false;
    input__text.forEach(input=>{ 
        input.classList.remove('input__container--input-error');
        if(input.value.trim() === ''){
            e.preventDefault();
            error__input = true;
            input.classList.add('input__container--input-error');
            input.focus();
        };
    });
    if(error__input){
        const error__message = document.createElement('h5');
        error__message.textContent = 'Debe completar todos los campos';
        error__message.classList.add('error__container--error');
        error__container.appendChild(error__message);
    };
});