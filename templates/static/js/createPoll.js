function buildOption(optionNumber){
    let tempParentElement = document.createElement("div")
    tempParentElement.innerHTML += `<div class="form-group">
    <div><label for="option${optionNumber}">Option ${optionNumber}</label>${optionNumber != 1 ? '<i class="bi bi-dash-circle-dotted ml-2"></i>' : ''}</div>
    <input type="text" name="option${optionNumber}" maxlength="50">
    </div>`

    let element = tempParentElement.firstChild
    optionsDiv.appendChild(element)

    let removeIcon = element.querySelector("div i")
    if (removeIcon != null){
        removeIcon.addEventListener("click", (event)=>{
            removeOption(event.currentTarget.parentElement.parentElement)
        })
    }
    return element
}

var optionsDiv = null
$(document).ready(()=>{
    optionsDiv = document.getElementById("options")
})
var optionCount = 1

function addOption(text=""){
    if (optionCount >= 20){
        return
    }
    
    optionCount += 1
    optionElement = buildOption(optionCount)
    optionElement.querySelector("input").value = text
}

function removeOption(element){
    optionNumber = parseInt(element.querySelector("input").name.match(/[0-9]/))
    element.remove()
    for(let i = optionNumber + 1; i <= optionCount; i++){
        const inputElement = optionsDiv.querySelector(`input[name="option${i}"]`)
        let inputValue = inputElement.value
        inputElement.parentElement.remove()

        const newElement = buildOption(i - 1)
        newElement.querySelector("input").value = inputValue
    }
    optionCount -= 1
}