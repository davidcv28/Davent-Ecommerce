////////////////////////////////////////////////
///////////PRODUCT CART BUTTONS     ///////////
///////////////////////////////////////////////

const quantity__label =document.querySelector('#quantity__label');
const quantity__input = document.querySelector('#quantity__input');
const quantity__button__decrement = document.querySelector('#quantity__button__decrement');
const quantity__button__increment = document.querySelector('#quantity__button__increment');
let quantity = parseInt(quantity__label.textContent);

//// INCREMENT QUANTITY /////
quantity__button__increment.addEventListener('click', ()=>{
    if (quantity < 99){
        quantity += 1;
        quantity__label.textContent= String(quantity);
        quantity__input.value = quantity
    };
});

//// DECREMENT QUANTITY ////
quantity__button__decrement.addEventListener('click', ()=>{
    if (quantity > 1){
        quantity -= 1;
        quantity__label.textContent = String(quantity);
        quantity__input.value = quantity
    };
});


///////////////////////////////////////////////////////////
////////////// PRODUCT FORM COMMENTS /////////////////////
/////////////////////////////////////////////////////////

document.addEventListener('DOMContentLoaded', ()=>{
    const msj__error = document.querySelector('#msj__error');
    if (msj__error.textContent) {
        const msj__error__link = msj__error.querySelector('#msj__error__link');
        msj__error.querySelector('#comments__coment');
        msj__error__link.click();
        
    }
})