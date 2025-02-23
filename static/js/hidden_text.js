document.addEventListener("DOMContentLoaded", function () {
    const tokenElement = document.getElementById("api-token");
    const toggleButton = document.getElementById("toggle-token");
    const toggleIcon = document.getElementById("toggle-icon");

    toggleButton.addEventListener("click", function () {
        if (tokenElement.style.display === "none") {
            tokenElement.style.display = "inline";
            toggleIcon.classList.remove("fa-eye");
            toggleIcon.classList.add("fa-eye-slash");
        } else {
            tokenElement.style.display = "none";
            toggleIcon.classList.remove("fa-eye-slash");
            toggleIcon.classList.add("fa-eye");
        }
    });
});
