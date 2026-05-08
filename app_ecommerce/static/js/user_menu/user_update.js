////////////////////////////////////
///IMAGE PERFIL CHANGE ////////////
///////////////////////////////////
function initImageUploadListeners() {

    const image__update__fileinput = document.querySelector('#image__update__fileinput');
    const fileinput__button__open = document.querySelector('#fileinput__button__open');
    const change__image__button = document.querySelector('#change__image__button');


    if (fileinput__button__open && image__update__fileinput) {
        fileinput__button__open.addEventListener('click', () => {
            image__update__fileinput.click();
        });
    }

    if (image__update__fileinput && change__image__button) {
        image__update__fileinput.addEventListener('change', () => {
            change__image__button.click();
        });
    }
}

initImageUploadListeners();


///SELECTION CHANGES FORM
document.body.addEventListener('htmx:afterSwap', function(evt) {

    if (evt.target.id === 'perfil__form' || evt.target.closest('#perfil__form')) {
        initImageUploadListeners();
    }
});
