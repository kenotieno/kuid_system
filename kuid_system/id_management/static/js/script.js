document.addEventListener("DOMContentLoaded", function() {
    const navbar = document.querySelector(".navbar");

    // Shrink navbar on scroll
    window.addEventListener("scroll", function() {
        if (window.scrollY > 50) {
            navbar.classList.add("shrink");
        } else {
            navbar.classList.remove("shrink");
        }
    });
});


