// static/js/main.js

/**
 * Lógica principal da Interface da Rede Social
 */
document.addEventListener('DOMContentLoaded', () => {
    
    // ==========================================
    // 1. Inicialização do Dark Mode Adaptativo
    // ==========================================
    const applyTheme = () => {
        if (localStorage.theme === 'dark' || (!('theme' in localStorage) && window.matchMedia('(prefers-color-scheme: dark)').matches)) {
            document.documentElement.classList.add('dark');
        } else {
            document.documentElement.classList.remove('dark');
        }
    };
    // Chama logo ao carregar
    applyTheme();

    const themeToggleBtn = document.getElementById('theme-toggle');
    if (themeToggleBtn) {
        themeToggleBtn.addEventListener('click', () => {
            document.documentElement.classList.toggle('dark');
            const isDark = document.documentElement.classList.contains('dark');
            localStorage.setItem('theme', isDark ? 'dark' : 'light');
        });
    }

    // ==========================================
    // 2. Micro-interações: Botões de Curtir
    // ==========================================
    // Optamos por Event Delegation no body para lidar com novos posts dinâmicos sem reativar eventos
    document.body.addEventListener('click', function(e) {
        const btnLike = e.target.closest('.btn-like');
        if (btnLike) {
            e.preventDefault();
            const icon = btnLike.querySelector('svg');
            
            const isLiked = btnLike.classList.contains('liked');
            if (isLiked) {
                // Remover o curtir
                btnLike.classList.remove('liked');
                btnLike.classList.remove('text-red-500');
                btnLike.classList.add('text-gray-500', 'dark:text-gray-400');
                if(icon) {
                    icon.setAttribute('fill', 'none');
                    icon.classList.remove('animate-like-pop');
                }
            } else {
                // Adicionar o curtir
                btnLike.classList.add('liked');
                btnLike.classList.remove('text-gray-500', 'dark:text-gray-400');
                btnLike.classList.add('text-red-500');
                if(icon) {
                    icon.setAttribute('fill', 'currentColor');
                    // Recomeçar animação forçando reflow
                    icon.classList.remove('animate-like-pop');
                    void icon.offsetWidth;
                    icon.classList.add('animate-like-pop');
                }
            }
        }

    // ==========================================
    // 3. Sistema de Seguir
    // ==========================================
        const btnFollow = e.target.closest('.btn-follow');
        if (btnFollow) {
            e.preventDefault();
            const isFollowing = btnFollow.classList.contains('following');
            const textSpan = btnFollow.querySelector('span') || btnFollow;
            
            if (isFollowing) {
                // Deixar de seguir
                btnFollow.classList.remove('following');
                btnFollow.classList.remove('bg-gray-200', 'dark:bg-gray-800', 'text-gray-900', 'dark:text-white');
                btnFollow.classList.add('bg-primary', 'text-white');
                textSpan.textContent = 'Seguir';
            } else {
                // Seguir
                btnFollow.classList.add('following');
                btnFollow.classList.remove('bg-primary', 'text-white');
                btnFollow.classList.add('bg-gray-200', 'dark:bg-gray-800', 'text-gray-900', 'dark:text-white');
                textSpan.textContent = 'Seguindo';
            }
        }
    });

    // ==========================================
    // 4. Lógica do Modal de Criação de Post
    // ==========================================
    const modal = document.getElementById('create-post-modal');
    const btnOpenModalMobile = document.getElementById('mobile-create-post-btn');
    const btnCloseModal = document.getElementById('close-modal-btn');
    const modalOverlay = document.getElementById('modal-overlay');
    const modalContent = document.getElementById('modal-content');
    
    // Elementos Internos
    const mediaInput = document.getElementById('media-input');
    const mediaPreview = document.getElementById('media-preview');
    const uploadPlaceholder = document.getElementById('upload-placeholder');
    const captionInput = document.getElementById('caption-input');
    const charCounter = document.getElementById('char-counter');
    const btnSubmitPost = document.getElementById('submit-post-btn');
    
    const uploadProgress = document.getElementById('upload-progress');
    const progressBar = document.getElementById('progress-bar');
    const successIcon = document.getElementById('success-icon');

    const openModal = () => {
        if (!modal) return;
        modal.classList.remove('hidden');
        // Pequeno delay para a transição CSS funcionar
        setTimeout(() => {
            modalContent.classList.remove('scale-95', 'opacity-0');
            modalContent.classList.add('scale-100', 'opacity-100');
            modalOverlay.classList.remove('opacity-0');
            modalOverlay.classList.add('opacity-100');
        }, 10);
    };

    const closeModal = () => {
        if (!modal) return;
        modalContent.classList.remove('scale-100', 'opacity-100');
        modalContent.classList.add('scale-95', 'opacity-0');
        modalOverlay.classList.remove('opacity-100');
        modalOverlay.classList.add('opacity-0');
        setTimeout(() => {
            modal.classList.add('hidden');
            // Reset do form
            mediaInput.value = '';
            mediaPreview.src = '';
            mediaPreview.classList.add('hidden');
            uploadPlaceholder.classList.remove('hidden');
            captionInput.value = '';
            charCounter.textContent = '0 / 2200';
            btnSubmitPost.querySelector('span').textContent = 'Share';
            successIcon.classList.add('hidden');
            uploadProgress.classList.add('hidden');
            progressBar.style.width = '0%';
        }, 300);
    };

    if (btnOpenModalMobile) btnOpenModalMobile.addEventListener('click', openModal);
    if (btnCloseModal) btnCloseModal.addEventListener('click', closeModal);
    if (modalOverlay) modalOverlay.addEventListener('click', closeModal);

    // Contagem de Caracteres
    if (captionInput) {
        captionInput.addEventListener('input', () => {
            const currentLen = captionInput.value.length;
            charCounter.textContent = `${currentLen} / 2200`;
            if (currentLen > 2180) {
                charCounter.classList.add('text-red-500');
            } else {
                charCounter.classList.remove('text-red-500');
            }
        });
    }

    // Preview de Imagem (Upload 4:5 otimizado)
    if (mediaInput) {
        mediaInput.addEventListener('change', function() {
            const file = this.files[0];
            if (file && file.type.startsWith('image/')) {
                const reader = new FileReader();
                reader.onload = function(e) {
                    mediaPreview.src = e.target.result;
                    mediaPreview.classList.remove('hidden');
                    uploadPlaceholder.classList.add('hidden');
                }
                reader.readAsDataURL(file);
            }
        });
    }

    // Micro-interação de Upload
    if (btnSubmitPost) {
        btnSubmitPost.addEventListener('click', () => {
            const btnSpan = btnSubmitPost.querySelector('span');
            // Desabilita botão
            btnSubmitPost.disabled = true;
            btnSpan.textContent = 'Sending...';
            btnSubmitPost.classList.add('opacity-80');
            
            // Exibe barra
            uploadProgress.classList.remove('hidden');
            progressBar.style.width = '10%';
            
            // Simula loading 2.0 (Fake promise delay para micro-interação)
            let progress = 10;
            const interval = setInterval(() => {
                progress += Math.random() * 30;
                if (progress > 95) progress = 95;
                progressBar.style.width = `${progress}%`;
            }, 300);

            setTimeout(() => {
                clearInterval(interval);
                progressBar.style.width = '100%';
                
                // Sucesso
                setTimeout(() => {
                    btnSpan.textContent = 'Published!';
                    successIcon.classList.remove('hidden');
                    btnSubmitPost.classList.remove('from-primary', 'to-blue-600');
                    btnSubmitPost.classList.add('from-secondary', 'to-green-500');
                    
                    setTimeout(() => {
                        closeModal();
                        // Restaura botão para próxima vez no closeModal
                        setTimeout(() => {
                            btnSubmitPost.disabled = false;
                            btnSubmitPost.classList.remove('opacity-80', 'from-secondary', 'to-green-500');
                            btnSubmitPost.classList.add('from-primary', 'to-blue-600');
                        }, 300);
                    }, 1200);
                }, 300);
            }, 1500);
        });
    }

});
