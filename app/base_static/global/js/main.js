// static/js/main.js

/**
 * Main interface logic for the social network
 */
document.addEventListener('DOMContentLoaded', () => {

    // ==========================================
    // 1. Adaptive dark mode initialization
    // ==========================================
    const applyTheme = () => {
        if (localStorage.theme === 'dark' || (!('theme' in localStorage) && window.matchMedia('(prefers-color-scheme: dark)').matches)) {
            document.documentElement.classList.add('dark');
        } else {
            document.documentElement.classList.remove('dark');
        }
    };
    // Apply immediately on load
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
    // 2. Read more / show less – INP < 200ms
    // ==========================================
    // Event delegation: a single listener manages all buttons,
    // including those added dynamically via infinite scroll.
    document.body.addEventListener('click', function (e) {
        const btnReadMore = e.target.closest('.btn-read-more');
        if (btnReadMore) {
            e.preventDefault();
            const expandable = btnReadMore.closest('.post-text-expandable');
            if (!expandable) return;

            const preview = expandable.querySelector('.post-text-preview');
            const fullText = expandable.querySelector('.post-text-full');
            const isExpanded = btnReadMore.getAttribute('aria-expanded') === 'true';

            if (isExpanded) {
                // Collapse
                preview.classList.remove('hidden');
                preview.removeAttribute('aria-hidden');
                fullText.classList.add('hidden');
                fullText.setAttribute('aria-hidden', 'true');
                btnReadMore.setAttribute('aria-expanded', 'false');
                btnReadMore.querySelector('span') && (btnReadMore.querySelector('span').textContent = 'Ler mais');
                // Fallback when the button text is a direct text node
                if (!btnReadMore.querySelector('span')) {
                    btnReadMore.childNodes[0].textContent = 'View more';
                }
            } else {
                // Expand
                preview.classList.add('hidden');
                preview.setAttribute('aria-hidden', 'true');
                fullText.classList.remove('hidden');
                fullText.removeAttribute('aria-hidden');
                btnReadMore.setAttribute('aria-expanded', 'true');
                if (!btnReadMore.querySelector('span')) {
                    btnReadMore.childNodes[0].textContent = 'View less';
                }
            }
            return; // Stop the logical propagation (not the DOM event)
        }
    });

    // ==========================================
    // 3. Micro-interactions: Like buttons
    // ==========================================
    // Event delegation on the body handles new dynamic posts without reattaching events
    document.body.addEventListener('click', function (e) {
        const btnLike = e.target.closest('.btn-like');
        if (btnLike) {
            e.preventDefault();
            const publicationId = btnLike.dataset.id
            const likeCountSpan = document.getElementById(`like-count-${publicationId}`)
            const csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content')
            fetch(`/p/${publicationId}/like/`, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': csrfToken,
                    'Content-Type': 'application/json'
                }
            })
                .then(response => {
                    if (response.redirected) {
                        window.location.href = `/a/login/?next=${encodeURIComponent(window.location.pathname)}`
                        return
                    }
                    if (response.status === 403) {
                        window.location.href = `/a/login/?next=${encodeURIComponent(window.location.pathname)}`
                        return
                    }
                    if (!response.ok) {
                        throw new Error(`HTTP error! status: ${response.status}`);
                    }
                    return response.json()
                })
                .then(data => {
                    if (data) {
                        likeCountSpan.textContent = `${data.likes_count}`
                    }
                })
                .catch(error => console.error('Error:', error))

            const icon = btnLike.querySelector('svg');
            const isLiked = btnLike.classList.contains('liked');
            if (isLiked) {
                // Unlike
                btnLike.classList.remove('liked');
                btnLike.classList.remove('text-red-500');
                btnLike.classList.add('text-gray-800', 'dark:text-gray-200');
                if (icon) {
                    icon.setAttribute('fill', 'none');
                    icon.classList.remove('animate-like-pop');
                }
            } else {
                // Like
                btnLike.classList.add('liked');
                btnLike.classList.remove('text-gray-800', 'dark:text-gray-200');
                btnLike.classList.add('text-red-500');
                if (icon) {
                    icon.setAttribute('fill', 'currentColor');
                    // Restart animation by forcing reflow
                    icon.classList.remove('animate-like-pop');
                    void icon.offsetWidth;
                    icon.classList.add('animate-like-pop');
                }
            }
        }
        // ==========================================
        //  Save buttons
        // ==========================================

        const btnSave = e.target.closest('.btn-save');
        if (btnSave) {
            e.preventDefault();
            const publicationId = btnSave.dataset.id
            const csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content')
            fetch(`/p/${publicationId}/save/`, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': csrfToken,
                    'Content-Type': 'application/json'
                }
            })
                .then(response => {
                    if (response.redirected) {
                        window.location.href = `/a/login/?next=${encodeURIComponent(window.location.pathname)}`
                        return
                    }
                    if (response.status === 403) {
                        window.location.href = `/a/login/?next=${encodeURIComponent(window.location.pathname)}`
                        return
                    }
                    if (!response.ok) {
                        throw new Error(`HTTP error! status: ${response.status}`);
                    }
                    return response.json()
                })
                .catch(error => console.error('Error:', error))

            const icon = btnSave.querySelector('svg');
            const isSaved = btnSave.classList.contains('saved');
            if (isSaved) {
                // Unsaved
                btnSave.classList.remove('saved');

                if (btnSave.closest('.dropdown-menu')) {
                    btnSave.classList.remove('text-blue-600', 'dark:text-blue-400', 'font-medium');
                    btnSave.classList.add('text-gray-700', 'dark:text-gray-200');
                } else {
                    btnSave.classList.remove('bg-white');
                    btnSave.classList.add('text-gray-800', 'dark:text-gray-200');
                }

                if (icon) {
                    icon.setAttribute('fill', 'none');
                    icon.classList.remove('animate-like-pop');
                }
                const saveText = btnSave.querySelector('.save-text');
                if (saveText) saveText.textContent = 'Save';
            } else {
                // Saved
                btnSave.classList.add('saved');

                if (btnSave.closest('.dropdown-menu')) {
                    btnSave.classList.remove('text-gray-700', 'dark:text-gray-200');
                    btnSave.classList.add('text-blue-600', 'dark:text-blue-400', 'font-medium');
                } else {
                    btnSave.classList.remove('text-gray-800', 'dark:text-gray-200');
                    btnSave.classList.add('bg-white');
                }

                if (icon) {
                    icon.setAttribute('fill', 'currentColor');
                    // Restart animation by forcing reflow
                    icon.classList.remove('animate-like-pop');
                    void icon.offsetWidth;
                    icon.classList.add('animate-like-pop');
                }
                const saveText = btnSave.querySelector('.save-text');
                if (saveText) saveText.textContent = 'Saved';
            }
        }

        // ==========================================
        //  Follow system
        // ==========================================
        const btnFollow = e.target.closest('.btn-follow');
        if (btnFollow) {
            e.preventDefault();
            const username = btnFollow.dataset.username;
            const csrfToken = document.querySelector('meta[name="csrf-token"]')?.getAttribute('content');

            if (username && csrfToken) {
                fetch(`/profile/${username}/follow`, {
                    method: 'POST',
                    headers: {
                        'X-CSRFToken': csrfToken,
                        'Content-Type': 'application/json'
                    }
                })
                .then(response => {
                    if (response.redirected) {
                        window.location.href = `/a/login/?next=${encodeURIComponent(window.location.pathname)}`;
                        return;
                    }
                    if (response.status === 403) {
                        window.location.href = `/a/login/?next=${encodeURIComponent(window.location.pathname)}`;
                        return;
                    }
                    if (!response.ok) {
                        throw new Error(`HTTP error! status: ${response.status}`);
                    }
                    return response.json();
                })
                .then(data => {
                    if (data) {
                        const isFollowing = data.is_following;
                        const textSpan = btnFollow.querySelector('span') || btnFollow;

                        if (!isFollowing) {
                            // Unfollow
                            btnFollow.classList.remove('following');
                            btnFollow.classList.remove('bg-gray-200', 'dark:bg-gray-800', 'text-gray-900', 'dark:text-white');
                            btnFollow.classList.add('bg-primary', 'text-white');
                            textSpan.textContent = 'Follow';
                        } else {
                            // Follow
                            btnFollow.classList.add('following');
                            btnFollow.classList.remove('bg-primary', 'text-white');
                            btnFollow.classList.add('bg-gray-200', 'dark:bg-gray-800', 'text-gray-900', 'dark:text-white');
                            textSpan.textContent = 'Following';
                        }
                    }
                })
                .catch(error => console.error('Error:', error));
            } else {
                // Fallback UI logic if missing data
                const isFollowing = btnFollow.classList.contains('following');
                const textSpan = btnFollow.querySelector('span') || btnFollow;

                if (isFollowing) {
                    // Unfollow
                    btnFollow.classList.remove('following');
                    btnFollow.classList.remove('bg-gray-200', 'dark:bg-gray-800', 'text-gray-900', 'dark:text-white');
                    btnFollow.classList.add('bg-primary', 'text-white');
                    textSpan.textContent = 'Follow';
                } else {
                    // Follow
                    btnFollow.classList.add('following');
                    btnFollow.classList.remove('bg-primary', 'text-white');
                    btnFollow.classList.add('bg-gray-200', 'dark:bg-gray-800', 'text-gray-900', 'dark:text-white');
                    textSpan.textContent = 'Following';
                }
            }
        }
    });

    // ==========================================
    // 4. Create post modal logic
    // ==========================================
    const modal = document.getElementById('create-post-modal');
    const btnOpenModalMobile = document.getElementById('mobile-create-post-btn');
    const btnCloseModal = document.getElementById('close-modal-btn');
    const modalOverlay = document.getElementById('modal-overlay');
    const modalContent = document.getElementById('modal-content');

    // Internal elements
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
        // Small delay so the CSS transition can run
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
            // Reset the form
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

    // Character count
    if (captionInput) {
        captionInput.addEventListener('input', () => {
            const currentLen = captionInput.value.length;
            charCounter.textContent = `${currentLen} / 2200`;
            if (currentLen > 2180) {
                charCounter.classList.add('text-red-500');
            } else {
                charCounter.classList.remove('text-red-500');
            }
            // Clear validation error when user starts typing
            if (captionInput.value.trim() !== '') {
                captionInput.classList.remove('border-red-500', 'dark:border-red-500');
            }
        });
    }

    // Image preview (optimized 4:5 upload)
    if (mediaInput) {
        mediaInput.addEventListener('change', function () {
            const file = this.files[0];
            if (file && file.type.startsWith('image/')) {
                const reader = new FileReader();
                reader.onload = function (e) {
                    mediaPreview.src = e.target.result;
                    mediaPreview.classList.remove('hidden');
                    uploadPlaceholder.classList.add('hidden');
                }
                reader.readAsDataURL(file);
            }
        });
    }

    // Upload micro-interaction
    if (btnSubmitPost) {
        btnSubmitPost.addEventListener('click', () => {
            // Validate caption input (must not be empty since model text is required)
            if (captionInput && captionInput.value.trim() === '') {
                captionInput.classList.add('border-red-500', 'dark:border-red-500');
                captionInput.focus();
                return;
            }

            const btnSpan = btnSubmitPost.querySelector('span');
            // Disable button
            btnSubmitPost.disabled = true;
            btnSpan.textContent = 'Sending...';
            btnSubmitPost.classList.add('opacity-80');

            // Show progress bar
            uploadProgress.classList.remove('hidden');
            progressBar.style.width = '10%';

            // Simulate loading 2.0 (fake promise delay for micro-interaction)
            let progress = 10;
            const interval = setInterval(() => {
                progress += Math.random() * 30;
                if (progress > 95) progress = 95;
                progressBar.style.width = `${progress}%`;
            }, 300);

            setTimeout(() => {
                clearInterval(interval);
                progressBar.style.width = '100%';

                // Success
                setTimeout(() => {
                    btnSpan.textContent = 'Published!';
                    successIcon.classList.remove('hidden');
                    btnSubmitPost.classList.remove('from-primary', 'to-blue-600');
                    btnSubmitPost.classList.add('from-secondary', 'to-green-500');

                    setTimeout(() => {
                        // Submit the form to the server!
                        const form = document.getElementById('create-post-form');
                        if (form) {
                            form.submit();
                        } else {
                            closeModal();
                            // Restore button for the next time in closeModal
                            setTimeout(() => {
                                btnSubmitPost.disabled = false;
                                btnSubmitPost.classList.remove('opacity-80', 'from-secondary', 'to-green-500');
                                btnSubmitPost.classList.add('from-primary', 'to-blue-600');
                            }, 300);
                        }
                    }, 1200);
                }, 300);
            }, 1500);
        });
    }

    // ==========================================
    // 5. Dropdown Mais Opções (Toggle e Click-away)
    // ==========================================
    document.body.addEventListener('click', function (e) {
        // Handle dropdown toggle
        const btnOptions = e.target.closest('.btn-options');
        if (btnOptions) {
            e.preventDefault();
            const container = btnOptions.closest('.dropdown-container');
            const menu = container.querySelector('.dropdown-menu');
            const isExpanded = btnOptions.getAttribute('aria-expanded') === 'true';

            // Close all other dropdowns first
            document.querySelectorAll('.dropdown-menu:not(.hidden)').forEach(openMenu => {
                if (openMenu !== menu) {
                    closeDropdown(openMenu);
                }
            });

            if (!isExpanded) {
                // Open
                menu.classList.remove('hidden');
                menu.classList.remove('dropdown-animate-out');
                menu.classList.add('dropdown-animate-in');
                btnOptions.setAttribute('aria-expanded', 'true');
            } else {
                // Close
                closeDropdown(menu);
            }
            return;
        }

        // Click-away listener
        if (!e.target.closest('.dropdown-container')) {
            document.querySelectorAll('.dropdown-menu:not(.hidden)').forEach(menu => {
                closeDropdown(menu);
            });
        }
    });

    function closeDropdown(menu) {
        const container = menu.closest('.dropdown-container');
        if (!container) return;
        const btn = container.querySelector('.btn-options');
        if (btn) btn.setAttribute('aria-expanded', 'false');

        menu.classList.remove('dropdown-animate-in');
        menu.classList.add('dropdown-animate-out');

        // Wait for animation to finish before hiding
        setTimeout(() => {
            if (menu.classList.contains('dropdown-animate-out')) {
                menu.classList.add('hidden');
            }
        }, 150);
    }

    // ==========================================
    // 6. Delete Confirmation Modal
    // ==========================================
    const confirmModal = document.getElementById('confirm-modal');
    const confirmOverlay = document.getElementById('confirm-overlay');
    const confirmContent = document.getElementById('confirm-content');
    const btnCancelConfirm = document.getElementById('confirm-cancel-btn');
    const confirmForm = document.getElementById('confirm-form');

    const closeConfirmModal = () => {
        if (!confirmModal) return;
        confirmContent.classList.remove('scale-100', 'opacity-100');
        confirmContent.classList.add('scale-95', 'opacity-0');
        confirmOverlay.classList.remove('opacity-100');
        confirmOverlay.classList.add('opacity-0');
        setTimeout(() => {
            confirmModal.classList.add('hidden');
        }, 200);
    };

    document.body.addEventListener('click', function (e) {
        const btnDelete = e.target.closest('.btn-delete');
        if (btnDelete) {
            e.preventDefault();
            const deleteUrl = btnDelete.getAttribute('data-delete-url');
            if (confirmForm && deleteUrl) {
                confirmForm.action = deleteUrl;
            }

            // Close any open dropdowns
            document.querySelectorAll('.dropdown-menu:not(.hidden)').forEach(menu => {
                closeDropdown(menu);
            });

            // Open modal
            if (confirmModal) {
                confirmModal.classList.remove('hidden');
                // Small delay for CSS transition
                setTimeout(() => {
                    confirmContent.classList.remove('scale-95', 'opacity-0');
                    confirmContent.classList.add('scale-100', 'opacity-100');
                    confirmOverlay.classList.remove('opacity-0');
                    confirmOverlay.classList.add('opacity-100');
                }, 10);
            }
        }
    });

    if (btnCancelConfirm) btnCancelConfirm.addEventListener('click', closeConfirmModal);
    if (confirmOverlay) confirmOverlay.addEventListener('click', closeConfirmModal);
});
