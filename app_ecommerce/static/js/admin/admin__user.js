import {close_modal, modal_open } from "../controls.js";
/////////////////////
/////MODAL REGISTER USER /////
/////////////////////
const  user__modal = document.querySelector('#user__modal'); 
/// OPEN MODAL ///
const  modal__user__open =document.querySelector('#user__button__open__modal');
modal__user__open.addEventListener('click', ()=>{
    modal_open(user__modal);
});

/// CLOSE MODAL ///
const user__button__close__modal = document.querySelector('#user__button__close__modal');
user__button__close__modal.addEventListener('click', ()=>{
    close_modal(user__modal);
});


///////////////////////////
//// DELETE MODAL USER ////
///////////////////////////
const delete__modal__user = document.querySelector('#delete__modal__user');
/// DELETE__ITEM ///
const delete__item__button = document.querySelectorAll('.delete__item__button');
const input_delete_text = delete__modal__user.querySelector('#input__delete__modal__username');
const delete__modal__cancel__button = document.querySelector('#delete__modal__cancel__button');
delete__item__button.forEach(item=>{
    item.addEventListener('click', ()=>{
    modal_open(delete__modal__user);
    delete__modal__cancel__button.addEventListener('click', ()=>{
        close_modal(delete__modal__user);
    });
    const label__text=delete__modal__user.querySelector('.username__label');
    let itemcontent = item.getAttribute('id');
    input_delete_text.value = itemcontent;
    label__text.textContent = itemcontent;
    });   
});


////////////////////////////////////
////////// MODAL UPDATE USER /////////
//////////////////////////////////
const user__update__modal = document.querySelector('#user__update__modal');
const userupdate__button__close__modal = user__update__modal.querySelector('#close__update__user__modal__button');
const update__modal__user__openbutton = document.querySelectorAll('.update__modal__user__button');


//// OPEN MODAL ///
update__modal__user__openbutton.forEach(button =>{
    button.addEventListener('click', ()=>{
        modal_open(user__update__modal);
        //DATA USER //
        const update__user__id = button.getAttribute('data-id-user');
        const update__user__name = button.getAttribute('data-name-user');
        const update__user__lastname = button.getAttribute('data-lastname-user');
        const update__user__username = button.getAttribute('data-username-user');
        const update__user__email = button.getAttribute('data-email-user');

        // INPUTS DATA USER //
        const update__input__user__id = document.querySelector('#input__modal__user__id'); // Get the ID input
        const update__input__user__first__name = document.querySelector('#id_user__update__modal-first_name');
        const update__input__user__last__name = document.querySelector('#id_user__update__modal-last_name');
        const update__input__user__username = document.querySelector('#id_user__update__modal-username');
        const update__input__user__email = document.querySelector('#id_user__update__modal-email');

        update__input__user__id.value = update__user__id; // Set the ID input value
        update__input__user__first__name.value = update__user__name;
        update__input__user__last__name.value = update__user__lastname;
        update__input__user__username.value = update__user__username;
        update__input__user__email.value = update__user__email;
            
    });
});


/// CLOSE MODAL ///

    userupdate__button__close__modal.addEventListener('click', ()=>{
    close_modal(user__update__modal);
});
