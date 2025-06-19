// Main JavaScript for the property website

document.addEventListener('DOMContentLoaded', function() {
    // Mobile menu toggle
    const mobileMenuButton = document.querySelector('.navbar-toggler');
    const mobileMenu = document.querySelector('#mainNav');
    
    if (mobileMenuButton && mobileMenu) {
        mobileMenuButton.addEventListener('click', function() {
            mobileMenu.classList.toggle('show');
        });
    }
    
    // Smooth scrolling for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            e.preventDefault();
            
            const targetId = this.getAttribute('href');
            if (targetId === '#') return;
            
            const targetElement = document.querySelector(targetId);
            if (targetElement) {
                targetElement.scrollIntoView({
                    behavior: 'smooth'
                });
            }
        });
    });
    
    // Property image gallery functionality
    const propertyThumbnails = document.querySelectorAll('.thumbnail');
    if (propertyThumbnails.length > 0) {
        propertyThumbnails.forEach(thumb => {
            thumb.addEventListener('click', function() {
                const mainImage = document.querySelector('.main-image img');
                if (mainImage) {
                    mainImage.src = this.src;
                }
                
                // Update active thumbnail
                propertyThumbnails.forEach(t => t.classList.remove('active'));
                this.classList.add('active');
            });
        });
    }
    
    // Contact form validation
    const contactForm = document.querySelector('.contact-form');
    if (contactForm) {
        contactForm.addEventListener('submit', function(e) {
            let isValid = true;
            const requiredFields = this.querySelectorAll('[required]');
            
            requiredFields.forEach(field => {
                if (!field.value.trim()) {
                    field.classList.add('is-invalid');
                    isValid = false;
                } else {
                    field.classList.remove('is-invalid');
                }
            });
            
            if (!isValid) {
                e.preventDefault();
                
                // Scroll to first invalid field
                const firstInvalid = this.querySelector('.is-invalid');
                if (firstInvalid) {
                    firstInvalid.scrollIntoView({
                        behavior: 'smooth',
                        block: 'center'
                    });
                    firstInvalid.focus();
                }
            }
        });
    }
    
    // Initialize Bootstrap tooltips
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function(tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
    
    // Back to top button
    const backToTopButton = document.createElement('button');
    backToTopButton.innerHTML = '<i class="fas fa-arrow-up"></i>';
    backToTopButton.className = 'btn btn-primary-custom back-to-top';
    backToTopButton.style.position = 'fixed';
    backToTopButton.style.bottom = '20px';
    backToTopButton.style.right = '20px';
    backToTopButton.style.display = 'none';
    backToTopButton.style.zIndex = '99';
    backToTopButton.style.borderRadius = '50%';
    backToTopButton.style.width = '50px';
    backToTopButton.style.height = '50px';
    document.body.appendChild(backToTopButton);
    
    window.addEventListener('scroll', function() {
        if (window.pageYOffset > 300) {
            backToTopButton.style.display = 'block';
        } else {
            backToTopButton.style.display = 'none';
        }
    });
    
    backToTopButton.addEventListener('click', function() {
        window.scrollTo({
            top: 0,
            behavior: 'smooth'
        });
    });
    
    // Property search filters - show more options
    const showMoreFilters = document.querySelector('.show-more-filters');
    if (showMoreFilters) {
        showMoreFilters.addEventListener('click', function(e) {
            e.preventDefault();
            const extraFilters = document.querySelector('.extra-filters');
            if (extraFilters) {
                extraFilters.classList.toggle('d-none');
                this.textContent = extraFilters.classList.contains('d-none') ? 
                    'Show More Filters' : 'Show Fewer Filters';
            }
        });
    }
});

// Image preview for property forms
document.addEventListener('DOMContentLoaded', function() {
    // Function to preview images before upload
    function previewImage(input, previewId) {
        const preview = document.getElementById(previewId);
        const file = input.files[0];
        const reader = new FileReader();
        
        reader.onload = function(e) {
            preview.src = e.target.result;
            preview.style.display = 'block';
        }
        
        if (file) {
            reader.readAsDataURL(file);
        }
    }
    
    // Set up previews for all image inputs
    const imageInputs = document.querySelectorAll('input[type="file"][accept^="image/"]');
    imageInputs.forEach(input => {
        const previewId = input.id + '-preview';
        let preview = document.getElementById(previewId);
        
        if (!preview) {
            preview = document.createElement('img');
            preview.id = previewId;
            preview.className = 'image-preview';
            preview.style.display = 'none';
            input.parentNode.insertBefore(preview, input.nextSibling);
        }
        
        input.addEventListener('change', function() {
            previewImage(this, previewId);
        });
    });
});