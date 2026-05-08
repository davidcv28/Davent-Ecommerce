///////SLIDER CONTAINER ////////
const slider__button__icon = document.querySelector('#slider__button__icon');
const slider__container = document.querySelector('.slider__container');
const labels__container__body__label__input =document.querySelector('.labels__container__body__label--input');
slider__button__icon.addEventListener('click',()=>{
    slider__container.classList.toggle('slider__container--movil');
})


//FILTERS BUTTON ///
const filter__button = document.querySelectorAll('.filter__container');
filter__button.forEach(button =>{
 button.addEventListener('click', ()=>{
    const filter__container__arrow = button.querySelectorAll('.filter__container__title--icon');
    const filter__item = button.querySelectorAll('.filter__item');
    filter__item.forEach(item=>{
        item.classList.toggle('filter__item--view');
    });
    
    filter__container__arrow.forEach(item=>{
        item.classList.toggle('filter__container__title--icon-arrow');
    })
    
 });
});

//FILTER LABELS //
filter__labels = document.querySelectorAll('.filter__item--link');
filter__container = document.querySelector('#labels__container');

category__labels__count = 0;
brand__labels__count = 0;
price__labels__count = 0;
filter__labels.forEach(label =>{
    label.addEventListener('click', ()=>{
        const input__item = document.createElement('input');
        const label__item = document.createElement('label');
        label__item.classList.add('labels__container__body--label');
        input__item.classList.add('labels__container__body__label--input');
        let no__item = true;
        input__item.value = label.textContent;     
       
        filter__container.querySelectorAll('.labels__container__body--label').forEach(item=>{
            if (input__item.value === item.querySelector('.labels__container__body__label--input').value) {
                no__item = false;
            }
        });
        if(no__item){
            if (label.classList.contains('category__label') && category__labels__count <3) {
                input__item.name ='category__item';
                category__labels__count += 1;
                label__item.textContent = "Categoria = "
                label__item.appendChild(input__item);
                label__item.addEventListener('click', ()=>{
                    label__item.remove();
                })
                filter__container.appendChild(label__item);
            };
            if (label.classList.contains('brand__label') && brand__labels__count <3) {
                input__item.name ='brand__item';
                brand__labels__count += 1;
                label__item.textContent = "Marca = "
                label__item.appendChild(input__item);
                label__item.addEventListener('click', ()=>{
                    label__item.remove();
                })
                filter__container.appendChild(label__item);
            };
            if (label.classList.contains('price__label') && price__labels__count <1) {
                input__item.name ='price__item';
                price__labels__count += 1;
                label__item.appendChild(input__item);
                label__item.addEventListener('click', ()=>{
                    label__item.remove();
                })
                filter__container.appendChild(label__item);
            };
        };
        
    });
});

