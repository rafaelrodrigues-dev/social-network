document.querySelectorAll('.like-button').forEach(button =>{
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
            if(data.liked) {
                this.classList.add('liked')
            } else {
                this.classList.remove('liked')

            }
            likeCountSpan.textContent = `${data.likes_count}`
        }
        })
        .catch(error => console.error('Error:', error))
    })
})