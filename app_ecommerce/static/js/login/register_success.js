////Cuenta regresiva/////

const time = document.querySelector('#time');
const login__link = document.querySelector('#login__link');
function countdown() {

    for(let i = 0 ; i < 5 ; i++){
        setTimeout(()=>{
            a = Number(time.textContent) - 1;
            time.textContent = String(a);
            if(i === 5 - 1){
                login__link.click();
            }
        },1000 *(i+1))
        
    }
    
    
    
}
countdown();

