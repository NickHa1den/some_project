const commentForm = document.forms.commentForm;
const commentFormContent = commentForm.content;
const commentFormParentInput = commentForm.parent;
const commentFormSubmit = commentForm.commentSubmit;
const commentPostId = commentForm.getAttribute('data-post-id');

commentForm.addEventListener('submit', createComment);

replyUser()

function replyUser() {
    document.querySelectorAll('.btn-reply').forEach(e => {
        e.addEventListener('click', replyComment);
    });
}

function replyComment() {
    const commentUsername = this.getAttribute('data-comment-username');
    const commentMessageId = this.getAttribute('data-comment-id');
    commentFormContent.value = `${commentUsername}, `;
    commentFormParentInput.value = commentMessageId;
}

async function createComment(event) {
    event.preventDefault();
    commentFormSubmit.disabled = true;
    commentFormSubmit.innerText = "Ожидаем ответа сервера";
    try {
        const response = await fetch(`/posts/${commentPostId}/comment/create/`, {
            method: 'POST',
            headers: {
                'X-CSRFToken': csrftoken,
                'X-Requested-With': 'XMLHttpRequest',
            },
            body: new FormData(commentForm),
        });
        const comment = await response.json();

        let commentTemplate = `<ul id="comment-thread-${comment.id}">
                                        <li class="card border-0 custom-card">
                                            <div class="card-body mb-0">
                                                <div class="row">
                                                    <div class="col-md-1">
                                                        <img class="custom-card comment-img" src="${comment.avatar}" alt="${comment.author}"/>
                                                    </div>
                                                    <div class="col-md-11">
                                                        <h5 class="card-title mt-0 ms-3">
                                                            <a href="${comment.get_absolute_url}">${comment.author}</a>
                                                        </h5>
                                                        <small class="fs-6 ms-3">${comment.created}</small>
                                                        <p class="card-text mt-2 ms-3">
                                                            ${comment.content}
                                                        </p>
                                                        <a class="btn btn-sm btn-outline btn-reply custom-btn mb-0 ms-3" href="#commentForm" data-comment-id="${comment.id}" data-comment-username="${comment.author}">Ответить</a>
                                                    </div>
                                                </div>
                                                <hr/>
                                            </div>
                                        </li>
                                    </ul>`;
        if (comment.is_child) {
            document.querySelector(`#comment-thread-${comment.parent_id}`).insertAdjacentHTML("beforeend", commentTemplate);
        } else {
            document.querySelector('.nested-comments').insertAdjacentHTML("beforeend", commentTemplate)
        }
        commentForm.reset()
        commentFormSubmit.disabled = false;
        commentFormSubmit.innerText = "Добавить комментарий";
        commentFormParentInput.value = null;
        replyUser();
    } catch (error) {
        console.log(error)
    }
}

