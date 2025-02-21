document.addEventListener("DOMContentLoaded", function () {
    const stars = document.querySelectorAll(".star-rating input");
    const submitButtons = document.querySelectorAll(".submit-rating");

    stars.forEach(star => {
        star.addEventListener("change", function () {
            const ratingSection = this.closest(".rating-section");
            const drinkId = this.dataset.drinkId;
            const selectedValue = parseInt(this.value);

            // Highlight all stars up to the selected one
            ratingSection.querySelectorAll(".star-label").forEach(label => {
                label.classList.remove("selected");
                if (parseInt(label.dataset.value) <= selectedValue) {
                    label.classList.add("selected");
                }
            });

            // Show the selected rating
            const ratingDisplay = document.getElementById(`selected-rating-${drinkId}`);
            if (ratingDisplay) {
                ratingDisplay.textContent = `Selected Rating: ${selectedValue} Stars`;
            }

            // Enable submit button when a rating is selected
            const submitButton = ratingSection.querySelector(".submit-rating");
            if (submitButton) {
                submitButton.classList.add("active");
                submitButton.disabled = false;
            }
        });
    });

    // Ensure submit buttons are initially disabled
    submitButtons.forEach(button => {
        button.disabled = true;
    });
});
