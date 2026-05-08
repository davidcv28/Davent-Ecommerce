const login__user = document.querySelector('#login__user');
const login__password = document.querySelector('#login__password');
const login__form = document.querySelector('#login__form');
const error__container = document.querySelector('#error__container')

       
login__form.addEventListener('submit', (e)=>{
    
        if(login__user.value.trim() === '' || login__password.value.trim() === ''){   
        e.preventDefault();
        error__container.innerHTML=''
        if(login__user.value.trim() === ''){
            const message__error__user = document.createElement('h4');
            message__error__user.textContent="Porfavor Ingresar nombre de usuario"
            message__error__user.classList.add('error__container--message');
            error__container.appendChild(message__error__user);
        };
        if(login__password.value.trim() === ''){ 
            const message__error__password = document.createElement('h4');
            message__error__password.textContent="Porfavor Ingresar Contraseña de usuario"
            message__error__password.classList.add('error__container--message');
            error__container.appendChild(message__error__password);
        };
        
    };
    
});