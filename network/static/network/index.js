
function getcookie(name){
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`)
    if (parts.length == 2) return parts.pop().split(';').shift(); 
}

function second(y){
    const button = document.getElementById(`edit_${y}`)
    const parent = button.parentNode
    const editing_value = document.getElementById(`post_want_to_edit_${y}`)
    
   
    if (button.textContent === 'Edit'){

        const textarea = document.createElement('textarea')
        textarea.setAttribute('class', "form-control")
        textarea.setAttribute('id', `textarea_${y}`)
        textarea.setAttribute('rows', 3)
        textarea.textContent = editing_value.innerHTML
        parent.insertBefore(textarea, button.previousElementSibling)
        document.getElementById(`post_want_to_edit_${y}`).style.display = 'none'
        button.textContent = 'Save'

        //hide like icon and count
        document.getElementById(`image_${y}`).style.display = 'none'
        document.getElementById(`count_${y}`).style.display = 'none'
    }

    else if(button.textContent === 'Save')
    {   
        const changed_value = button.parentNode.firstElementChild.nextElementSibling
        let edit = document.getElementById(`post_want_to_edit_${y}`)
        fetch(`/edit/${y}`, {
                method : 'POST',
                headers : {'Content-type': 'application/json', 'X-CSRFToken' : getcookie("csrftoken")},
                body : JSON.stringify({
                    post : changed_value.value
                })
        })
        .then(response => response.json())
        .then(data => {
                edit.innerHTML = data['data']
        })
        parent.removeChild(button.parentNode.firstElementChild.nextElementSibling)

        document.getElementById(`post_want_to_edit_${y}`).style.display = 'block'

        button.textContent = 'Edit'
         //show like icon and count
         document.getElementById(`image_${y}`).style.display = 'block'
         document.getElementById(`count_${y}`).style.display = 'block'
    }
}

function like(value){
    let x = parseInt(document.getElementById(`count_${value}`).innerHTML)
    heart = document.getElementById(`image_${value}`)

    let count_value = document.getElementById(`count_${value}`)
    
    fetch(`like/${value}`,{
        method : 'POST',
        headers : {'Content-type': 'application/json', 'X-CSRFToken' : getcookie("csrftoken")},
    })
    .then(response => response.json())
    .then(data => {

        console.log(data)
        if (data['liked'] == true){
            x++
            count_value.innerHTML = x
            heart['src'] = `http://127.0.0.1:8000/static/images/red.svg`
        }
        else{
            x--
            count_value.innerHTML = x
            heart['src'] = `http://127.0.0.1:8000/static/images/white.svg`
        }
    })
}


function delete_post(value){

    const post = document.querySelector(`.post-container-${value}`)
    console.log(post)
    fetch(`delete/${value}`,{
        method : 'POST',
        headers : {'Content-type': 'application/json', 'X-CSRFToken' : getcookie("csrftoken")},
    })
    .then(response => response.json())
    .then(data => {
        console.log(data)
        post.innerHTML = ""
    })

}