
function clear_message(flashContainer){
    if (flashContainer){
        flashContainer.style.display = "none";
    }
}
function setClear(time, flash_container){

    setTimeout(()=>clear_message(flash_container), time)
}