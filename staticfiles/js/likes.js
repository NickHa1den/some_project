let btn = document.getElementById("like-button")
let num_of_likes = document.getElementById("num")

btn.addEventListener("click", likePost)

function likePost(e) {
    e.preventDefault()
    let post_id = "{{post.id}}"
    let url = "{% url 'blog:like' %}"
    const data = {id: post_id}

    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            "X-Requested-With": "XMLHttpRequest",
            'X-CSRFToken': csrftoken
        },
        body: JSON.stringify(data),
        credentials: "same-origin"
    })
        .then(res => {
            console.log(res.status);
            return res.json();
        })
        .then(data => {
            console.log(data)

            if (data["check"] === 1) {
                btn.classList.remove("fa-regular")
                btn.classList.add('fa-solid')
            } else if (data["check"] === 0) {
                btn.classList.add("fa-regular")
                btn.classList.remove('fa-solid')
            }

            num_of_likes.innerHTML = data["num_of_likes"]
            console.log(num_of_likes);
        })
        .catch(error => {
            console.log(error);
        })
}