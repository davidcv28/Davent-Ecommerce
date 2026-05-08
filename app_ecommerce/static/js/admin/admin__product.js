import {close_modal, modal_open } from "../controls.js";
///////////////////
//SET VARIABLES //
//////////////////
const modal__product = document.querySelector('#product__modal');
const  modal__product__open__button =document.querySelectorAll('.product__modal__open__button');
const modal__product__close__button = document.querySelector('#product__modal__close__button');
const modal__input__form__type = document.querySelector('#input__form__type');
const modal__product__title = document.querySelector('#product__modal--title');
const modal__product__button = document.querySelector('#product__modal--button');
const product__stock = document.querySelector('#product__stock');

/// MODAL VALIDATION INPUTS ///
product__stock.addEventListener('keydown', (e)=>{
    if (e.key === '.'  || e.key ===',') {
        e.preventDefault();
    };
});

/// OPEN MODAL /// 
modal__product__open__button.forEach(button__modal =>{

    button__modal.addEventListener('click', ()=>{
        const action = button__modal.getAttribute('data-name-product-actions');
        modal__product.querySelector('#product__modal__form').reset();
        if(action === 'product__register'){
            //////////////////////////////////
            /////MODAL REGISTER PRODUCT /////
            ////////////////////////////////
            modal__input__form__type.value ='add__product';
            modal__product__title.textContent='Registro de producto'
            modal__product__button.textContent = 'Registrar producto'
            modal_open(modal__product);
        }
        else{
            ///////////////////////////////
            /////MODAL UPDATE PRODUCT /////
            //////////////////////////////
            modal__input__form__type.value='update__product';
            modal__product__title.textContent='Editor de producto'
            modal__product__button.textContent='Guardar Cambios'

            //GET DATA PRODUCT //
            const product__data ={
                product__id: button__modal.getAttribute('data-id-product'),
                product__name : button__modal.getAttribute('data-name-product'),
                product__brand : button__modal.getAttribute('data-brand-product'),
                product__category : button__modal.getAttribute('data-category-product'),
                product__price : button__modal.getAttribute('data-price-product'),
                product__stock : button__modal.getAttribute('data-stock-product'),
                product__image : button__modal.getAttribute('data-image-product')
            };
            modal__product.querySelector('#product__id').value = product__data.product__id;
            modal__product.querySelector('#product__name').value = product__data.product__name;
            modal__product.querySelector('#product__brand').value = product__data.product__brand;
            modal__product.querySelector('#product__category').value = product__data.product__category;
            modal__product.querySelector('#product__price').value = product__data.product__price.replace(',','.');
            modal__product.querySelector('#product__stock').value = product__data.product__stock;
            
            modal_open(modal__product)
        };
    });
    
});

/// CLOSE MODAL ///
    modal__product__close__button.addEventListener('click', ()=>{
        close_modal(modal__product);
    })






///////////////////////////
//// DELETE MODAL PRODUCT ////
///////////////////////////
const delete__modal__product = document.querySelector('#delete__modal__product');
/// DELETE__ITEM ///
const delete__item__button = document.querySelectorAll('.delete__item__button');
const input_delete_text = delete__modal__product.querySelector('#input__delete__modal__id__product');
const delete__modal__cancel__button = document.querySelector('#delete__modal__cancel__button');
delete__item__button.forEach(item=>{
    item.addEventListener('click', ()=>{
    modal_open(delete__modal__product);
    delete__modal__cancel__button.addEventListener('click', ()=>{
        close_modal(delete__modal__product);
    });
    const label__text=delete__modal__product.querySelector('.product__name__label');
    let itemcontent = item.getAttribute('id');
    let itemnamecontent = item.getAttribute('data-name-product')
    input_delete_text.value = itemcontent;
    label__text.textContent = itemnamecontent;
    });   
});


////////////////////////////////////
////////// MODAL UPDATE PRODUCTS /////////
//////////////////////////////////
const product__update__modal = document.querySelector('#product__modal');
const product__update__modal__open__button = document.querySelector('.product__update__modal__open__button');
const product__update__modal__close__button = document.querySelector('#product__update__modal__close__button');

///OPEN UPDATE MODAL ///
/*product__update__modal__open__button.forEach(item =>{
    item.addEventListener('click', ()=>{
        // data-id-product="{{product.id}}" data-name-product = "{{product.name_product}}" data-brand-product="{{product.brand_product}}"  data-category-product="{{product.category_product}}" data-price-product="{{product.price_product}}" href="?updateproduct=" class="bi bi-pencil-square td--icon edit--icon product__update__modal__open__button"></i> <i title="Eliminar producto" id="{{product.id}}" data-name-product="{{product.name_product}}"
        ///PRODUCT DATA //
        const data__id__product = item.getAttribute('data-id-product');
        const data__name__product =  item.getAttribute('data-name-product');
        const data__brand__product = item.getAttribute('data-brand-product');
        const data__category__product = item.getAttribute('data-category-product');
        const data__price__product = item.getAttribute('data-price-product');
        const data__stock__product = item.getAttribute('data-stock-product');
        const data__image__product = item.getAttribute('data-image-product');
        //PRODUCT INPUT DATA //
        const data__input__name__product = item.getAttribute('form__product__update-name_product');
        const data__input__brand__product = item.getAttribute('form__product__update-brand_product');
        const data__input__category__product = item.getAttribute('form__product__update-category_product');
        const data__input__price__product = item.getAttribute('form__product__update-price_product');
        const data__input__stock__product = item.getAttribute('form__product__update-stock_product');
        const data__input__image__product = item.getAttribute('form__product__update-img_product');

        
    })
})
*/

/// OPEN BRAND MODAL ///
const open__brand__modal__button = document.querySelector('#open__brand__modal__button');
const close__brand__modal__button = document.querySelector('#close__brand__modal__button');
const brand__modal = document.querySelector('#brand__modal');

open__brand__modal__button.addEventListener('click', ()=>{
    modal_open(brand__modal);
    
});
close__brand__modal__button.addEventListener('click', ()=>{
    close_modal(brand__modal);
    document.body.style.overflow="hidden";
});
/// OPEN CATEGORY MODAL ///
const open__category__modal__button = document.querySelector('#open__category__modal__button');
const close__category__modal__button = document.querySelector('#close__category__modal__button');
const category__modal = document.querySelector('#category__modal');

open__category__modal__button.addEventListener('click', ()=>{
    modal_open(category__modal);
    
});
close__category__modal__button.addEventListener('click', ()=>{
    close_modal(category__modal);
    document.body.style.overflow="hidden";
});