const user__menu =document.querySelector('#user__menu');
const user__button__menu = document.querySelector('#user__button__menu');
if (user__button__menu) {
   user__button__menu.addEventListener('click', ()=>{
   user__menu.classList.toggle('nav__menu__movil--view');     
   });
};

///////////////////////////////
//////// BUYCART CONFIG //////
//////////////////////////////

document.addEventListener('click', (event) => {
   const buycart__button = event.target.closest('#buycart__button');
   const buycart__container = document.querySelector('#buycart__container');
   if (buycart__button) {
         if (buycart__container.hasAttribute('hidden')) {
            buycart__container.removeAttribute('hidden');
         } else {
            buycart__container.setAttribute('hidden', true);
         }
   }
});