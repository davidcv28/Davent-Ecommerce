const button__user__main__menu = document.querySelector('#button__user__main__menu');
const user__main__menu = document.querySelector('#user__main__menu');
button__user__main__menu.addEventListener('click', ()=>{
    user__main__menu.classList.toggle('slider__user__main-menu--movil');
});
