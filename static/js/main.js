// ========================================
// SIDEBAR TOGGLE (Mobile)
// ========================================
document.addEventListener('DOMContentLoaded', function() {
    const menuToggle = document.getElementById('menuToggle');
    const sidebar = document.getElementById('sidebar');
    const sidebarOverlay = document.getElementById('sidebarOverlay');
    
    if (menuToggle && sidebar && sidebarOverlay) {
        // Abrir sidebar
        menuToggle.addEventListener('click', function() {
            sidebar.classList.add('show');
            sidebarOverlay.classList.add('show');
            document.body.style.overflow = 'hidden';
        });
        
        // Cerrar sidebar
        sidebarOverlay.addEventListener('click', function() {
            sidebar.classList.remove('show');
            sidebarOverlay.classList.remove('show');
            document.body.style.overflow = '';
        });
        
        // Cerrar al hacer clic en un link (mobile)
        const navItems = sidebar.querySelectorAll('.nav-item');
        navItems.forEach(item => {
            item.addEventListener('click', function() {
                if (window.innerWidth <= 768) {
                    sidebar.classList.remove('show');
                    sidebarOverlay.classList.remove('show');
                    document.body.style.overflow = '';
                }
            });
        });
    }
    
    // ========================================
    // DROPDOWNS
    // ========================================
    
    // Notification dropdown
    const notificationBtn = document.getElementById('notificationBtn');
    const notificationMenu = document.getElementById('notificationMenu');
    
    if (notificationBtn && notificationMenu) {
        notificationBtn.addEventListener('click', function(e) {
            e.stopPropagation();
            notificationMenu.classList.toggle('show');
            // Cerrar user menu si está abierto
            if (userMenu) userMenu.classList.remove('show');
        });
    }
    
    // User dropdown
    const userBtn = document.getElementById('userBtn');
    const userMenu = document.getElementById('userMenu');
    
    if (userBtn && userMenu) {
        userBtn.addEventListener('click', function(e) {
            e.stopPropagation();
            userMenu.classList.toggle('show');
            // Cerrar notification menu si está abierto
            if (notificationMenu) notificationMenu.classList.remove('show');
        });
    }
    
    // Cerrar dropdowns al hacer clic fuera
    document.addEventListener('click', function(e) {
        if (notificationMenu && !notificationMenu.contains(e.target) && !notificationBtn.contains(e.target)) {
            notificationMenu.classList.remove('show');
        }
        if (userMenu && !userMenu.contains(e.target) && !userBtn.contains(e.target)) {
            userMenu.classList.remove('show');
        }
    });
    
    // ========================================
    // CERRAR ALERTAS
    // ========================================
    const alertCloses = document.querySelectorAll('.alert-close');
    alertCloses.forEach(btn => {
        btn.addEventListener('click', function() {
            const alert = this.closest('.alert');
            alert.style.animation = 'slideOutUp 0.3s ease';
            setTimeout(() => {
                alert.remove();
            }, 300);
        });
    });
    
    // Auto-cerrar alertas después de 5 segundos
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
        setTimeout(() => {
            if (alert.parentElement) {
                alert.style.animation = 'slideOutUp 0.3s ease';
                setTimeout(() => {
                    alert.remove();
                }, 300);
            }
        }, 5000);
    });
});

// ========================================
// ANIMACIÓN DE SALIDA PARA ALERTAS
// ========================================
const style = document.createElement('style');
style.textContent = `
    @keyframes slideOutUp {
        from {
            opacity: 1;
            transform: translateY(0);
        }
        to {
            opacity: 0;
            transform: translateY(-20px);
        }
    }
`;
document.head.appendChild(style);

// ========================================
// SMOOTH SCROLL
// ========================================
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        const href = this.getAttribute('href');
        if (href !== '#' && href !== '#!') {
            e.preventDefault();
            const target = document.querySelector(href);
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        }
    });
});

// ========================================
// INDICADOR DE CARGA AL ENVIAR FORMULARIOS
// ========================================
const forms = document.querySelectorAll('form');
forms.forEach(form => {
    form.addEventListener('submit', function() {
        const submitBtn = this.querySelector('button[type="submit"]');
        if (submitBtn && !submitBtn.disabled) {
            const originalText = submitBtn.innerHTML;
            submitBtn.disabled = true;
            submitBtn.innerHTML = '<i class="bi bi-arrow-clockwise rotating"></i> Enviando...';
            
            // Prevenir doble envío
            setTimeout(() => {
                submitBtn.disabled = false;
                submitBtn.innerHTML = originalText;
            }, 3000);
        }
    });
});

// CSS para el spinner rotando
const spinnerStyle = document.createElement('style');
spinnerStyle.textContent = `
    @keyframes rotating {
        from { transform: rotate(0deg); }
        to { transform: rotate(360deg); }
    }
    .rotating {
        animation: rotating 1s linear infinite;
    }
`;
document.head.appendChild(spinnerStyle);

// ========================================
// SIDEBAR TOGGLE (Mobile)
// ========================================
document.addEventListener('DOMContentLoaded', function() {
    const menuToggle = document.getElementById('menuToggle');
    const sidebar = document.getElementById('sidebar');
    const sidebarOverlay = document.getElementById('sidebarOverlay');
    
    if (menuToggle && sidebar && sidebarOverlay) {
        // Abrir sidebar
        menuToggle.addEventListener('click', function() {
            sidebar.classList.add('show');
            sidebarOverlay.classList.add('show');
            document.body.style.overflow = 'hidden';
        });
        
        // Cerrar sidebar
        sidebarOverlay.addEventListener('click', function() {
            sidebar.classList.remove('show');
            sidebarOverlay.classList.remove('show');
            document.body.style.overflow = '';
        });
        
        // Cerrar al hacer clic en un link (mobile)
        const navItems = sidebar.querySelectorAll('.nav-item');
        navItems.forEach(item => {
            item.addEventListener('click', function() {
                if (window.innerWidth <= 768) {
                    sidebar.classList.remove('show');
                    sidebarOverlay.classList.remove('show');
                    document.body.style.overflow = '';
                }
            });
        });
    }
    
    // ========================================
    // DROPDOWNS
    // ========================================
    
    // Notification dropdown
    const notificationBtn = document.getElementById('notificationBtn');
    const notificationMenu = document.getElementById('notificationMenu');
    
    if (notificationBtn && notificationMenu) {
        notificationBtn.addEventListener('click', function(e) {
            e.stopPropagation();
            notificationMenu.classList.toggle('show');
            // Cerrar user menu si está abierto
            if (userMenu) userMenu.classList.remove('show');
        });
    }
    
    // User dropdown
    const userBtn = document.getElementById('userBtn');
    const userMenu = document.getElementById('userMenu');
    
    if (userBtn && userMenu) {
        userBtn.addEventListener('click', function(e) {
            e.stopPropagation();
            userMenu.classList.toggle('show');
            // Cerrar notification menu si está abierto
            if (notificationMenu) notificationMenu.classList.remove('show');
        });
    }
    
    // Cerrar dropdowns al hacer clic fuera
    document.addEventListener('click', function(e) {
        if (notificationMenu && !notificationMenu.contains(e.target) && !notificationBtn.contains(e.target)) {
            notificationMenu.classList.remove('show');
        }
        if (userMenu && !userMenu.contains(e.target) && !userBtn.contains(e.target)) {
            userMenu.classList.remove('show');
        }
    });
    
    // ========================================
    // CERRAR ALERTAS
    // ========================================
    const alertCloses = document.querySelectorAll('.alert-close');
    alertCloses.forEach(btn => {
        btn.addEventListener('click', function() {
            const alert = this.closest('.alert');
            alert.style.animation = 'slideOutUp 0.3s ease';
            setTimeout(() => {
                alert.remove();
            }, 300);
        });
    });
    
    // Auto-cerrar alertas después de 5 segundos
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
        setTimeout(() => {
            if (alert.parentElement) {
                alert.style.animation = 'slideOutUp 0.3s ease';
                setTimeout(() => {
                    alert.remove();
                }, 300);
            }
        }, 5000);
    });
});

// ========================================
// ANIMACIÓN DE SALIDA PARA ALERTAS
// ========================================
const style = document.createElement('style');
style.textContent = `
    @keyframes slideOutUp {
        from {
            opacity: 1;
            transform: translateY(0);
        }
        to {
            opacity: 0;
            transform: translateY(-20px);
        }
    }
`;
document.head.appendChild(style);

// ========================================
// SMOOTH SCROLL
// ========================================
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        const href = this.getAttribute('href');
        if (href !== '#' && href !== '#!') {
            e.preventDefault();
            const target = document.querySelector(href);
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        }
    });
});

// ========================================
// INDICADOR DE CARGA AL ENVIAR FORMULARIOS
// ========================================
document.querySelectorAll('form').forEach(form => {
    form.addEventListener('submit', function() {
        const submitBtn = this.querySelector('button[type="submit"]');
        if (submitBtn && !submitBtn.disabled) {
            const originalText = submitBtn.innerHTML;
            submitBtn.disabled = true;
            submitBtn.innerHTML = '<i class="bi bi-arrow-clockwise rotating"></i> Enviando...';
            
            // Prevenir doble envío
            setTimeout(() => {
                submitBtn.disabled = false;
                submitBtn.innerHTML = originalText;
            }, 3000);
        }
    });
});

// CSS para el spinner rotando
const spinnerStyle = document.createElement('style');
spinnerStyle.textContent = `
    @keyframes rotating {
        from { transform: rotate(0deg); }
        to { transform: rotate(360deg); }
    }
    .rotating {
        animation: rotating 1s linear infinite;
    }
`;
document.head.appendChild(spinnerStyle);

// ========================================
// AUTH FORMS - LOGIN & REGISTER
// ========================================

// Toggle password visibility
const togglePasswordButtons = document.querySelectorAll('.toggle-password');
togglePasswordButtons.forEach(button => {
    button.addEventListener('click', function() {
        const targetId = this.getAttribute('data-target');
        const targetInput = document.getElementById(targetId);
        const icon = this.querySelector('i');
        
        if (targetInput.type === 'password') {
            targetInput.type = 'text';
            icon.classList.remove('bi-eye');
            icon.classList.add('bi-eye-slash');
        } else {
            targetInput.type = 'password';
            icon.classList.remove('bi-eye-slash');
            icon.classList.add('bi-eye');
        }
    });
});

// Cerrar mensajes de auth
const messageCloses = document.querySelectorAll('.message-close');
messageCloses.forEach(btn => {
    btn.addEventListener('click', function() {
        const message = this.closest('.message');
        message.style.animation = 'slideOutUp 0.3s ease';
        setTimeout(() => {
            message.remove();
        }, 300);
    });
});

// Password strength indicator (solo en registro)
const password1 = document.getElementById('password1');
const strengthBar = document.getElementById('strengthBar');

if (password1 && strengthBar) {
    password1.addEventListener('input', function() {
        const password = this.value;
        let strength = 0;
        
        if (password.length >= 8) strength++;
        if (/[A-Z]/.test(password)) strength++;
        if (/[0-9]/.test(password)) strength++;
        if (/[^A-Za-z0-9]/.test(password)) strength++;
        
        strengthBar.className = 'strength-bar';
        
        if (strength === 0) {
            strengthBar.style.width = '0';
        } else if (strength === 1) {
            strengthBar.classList.add('weak');
        } else if (strength === 2) {
            strengthBar.classList.add('fair');
        } else if (strength === 3) {
            strengthBar.classList.add('good');
        } else {
            strengthBar.classList.add('strong');
        }
    });
}

// Password match validation (registro)
const password2 = document.getElementById('password2');
const passwordMatch = document.getElementById('passwordMatch');

if (password1 && password2 && passwordMatch) {
    function checkPasswordMatch() {
        if (password2.value.length === 0) {
            passwordMatch.textContent = '';
            passwordMatch.className = 'password-match';
            return;
        }
        
        if (password1.value === password2.value) {
            passwordMatch.textContent = '✓ Las contraseñas coinciden';
            passwordMatch.className = 'password-match match';
        } else {
            passwordMatch.textContent = '✗ Las contraseñas no coinciden';
            passwordMatch.className = 'password-match no-match';
        }
    }
    
    password1.addEventListener('input', checkPasswordMatch);
    password2.addEventListener('input', checkPasswordMatch);
}

// Email validation
const emailInput = document.getElementById('email');
if (emailInput) {
    emailInput.addEventListener('blur', function() {
        const email = this.value;
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        const wrapper = this.closest('.input-wrapper');
        
        if (email && !emailRegex.test(email)) {
            wrapper.classList.add('error');
        } else {
            wrapper.classList.remove('error');
        }
    });
    
    emailInput.addEventListener('input', function() {
        const wrapper = this.closest('.input-wrapper');
        wrapper.classList.remove('error');
    });
}

// Mejorar respuesta táctil en todos los enlaces y botones
document.querySelectorAll('a, button').forEach(el => {
    el.addEventListener('touchstart', function() {
        // Esto ayuda a que el navegador detecte mejor los toques
    }, { passive: true });
});