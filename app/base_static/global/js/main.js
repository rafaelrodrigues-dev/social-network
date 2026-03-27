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
});
