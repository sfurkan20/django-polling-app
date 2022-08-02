function validateForm(formElem){
    document.getElementsByTagName("input").forEach((elem)=>{
        if(elem.checked){
            return true;
        }
    })
    alert("Please select an option.")
    return false;
}