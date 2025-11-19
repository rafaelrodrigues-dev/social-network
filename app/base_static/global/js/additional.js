document.querySelectorAll('.fa-heart').forEach(button =>{
    button.addEventListener('click', function() {
        const publicationId = this.dataset.id
        const likeCountSpan = this.nextElementSibling
        const csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content')
        fetch(`/p/${publicationId}/like/`,{
            method: 'POST',
            headers: {
                'X-CSRFToken': csrfToken,
                'Content-Type': 'application/json'
            }
        })
        .then(response => {
            if (response.status === 403) {
                window.location.href = '/a/login/'
                return
            }
            return response.json()
        })
        .then(data=> {
            if (data){
                likeCountSpan.textContent = `${data.likes_count}`
            }
        })
        .catch(error => console.error('Error:', error))
    })
})

document.addEventListener('DOMContentLoaded', function() {
    const btn = document.getElementById('view-more-comments');
    if (btn) {
        btn.addEventListener('click', function() {
            const nextPage = btn.getAttribute('data-next-page');
            fetch(`?comments_page=${nextPage}`)
                .then(response => response.text())
                .then(html => {
                    
                    const parser = new DOMParser();
                    const doc = parser.parseFromString(html, 'text/html');
                    const newComments = doc.querySelectorAll('#comments-list .post');
                    newComments.forEach(comment => {
                        document.getElementById('comments-list').appendChild(comment);
                    });

                    const newBtn = doc.getElementById('view-more-comments');
                    if (newBtn) {
                        btn.setAttribute('data-next-page', newBtn.getAttribute('data-next-page'));
                    } else {
                        btn.parentElement.remove();
                    }
                });
        });
    }
});