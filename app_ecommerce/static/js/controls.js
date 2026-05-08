/// MODAL OPEN AND CLOSE ///
export function modal_open(modal__name) {
    ////OPEN MODAL ////
        modal__name.showModal();
        modal__name.removeAttribute('hidden');
        document.body.style.overflow = "hidden";
};
export function close_modal(modal__name) {
    ////CLOSE MODAL ////
        modal__name.close();
        modal__name.setAttribute('hidden', '')
        document.body.style.overflow = "scroll";
};


