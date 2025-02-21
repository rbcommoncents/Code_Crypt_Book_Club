document.addEventListener("DOMContentLoaded", function () {
    console.log("rating_songs.js loaded successfully!");

    const stars = document.querySelectorAll(".star-rating input");
    const submitButtons = document.querySelectorAll(".submit-rating");

    // Handle star selection (but NOT submission)
    stars.forEach(star => {
        star.addEventListener("change", function () {
            const ratingSection = this.closest(".rating-section");
            if (!ratingSection) {
                console.error("ERROR: .rating-section not found! Check HTML structure.");
                return;
            }

            const songId = this.dataset.songId;
            const selectedValue = parseInt(this.value);

            console.log("Song ID Retrieved:", songId);
            console.log("Selected Rating Value:", selectedValue);

            if (!songId) {
                console.error("ERROR: songId is undefined or not set correctly.");
                return;
            }

            // Highlight all stars up to the selected one
            const labels = ratingSection.querySelectorAll(".star-label");
            labels.forEach(label => {
                label.classList.remove("selected");
                if (parseInt(label.dataset.value) <= selectedValue) {
                    label.classList.add("selected");
                }
            });

            // Enable submit button when a rating is selected
            const submitButton = ratingSection.querySelector(".submit-rating");
            if (submitButton) {
                submitButton.classList.add("active");
                submitButton.disabled = false;
                submitButton.dataset.selectedRating = selectedValue; // Store selected rating in the button
            }

            // Show the selected rating
            const ratingDisplay = document.getElementById(`selected-rating-${songId}`);
            if (ratingDisplay) {
                ratingDisplay.textContent = `Selected Rating: ${selectedValue} Stars`;
            }
        });
    });

    // Handle submit button click (Only submits when clicked)
    submitButtons.forEach(button => {
        button.addEventListener("click", function (event) {
            event.preventDefault();  // Prevents form submission (AJAX only)
            const ratingSection = this.closest(".rating-section");

            if (!ratingSection) {
                console.error("ERROR: .rating-section not found!");
                return;
            }

            const songId = ratingSection.querySelector("input[type='radio']:checked").dataset.songId;
            const selectedValue = parseInt(this.dataset.selectedRating);  // Get selected rating
            const commentField = ratingSection.querySelector("textarea[name='comment']");
            const comment = commentField ? commentField.value.trim() : "";

            console.log("Submitting Rating: ", selectedValue);
            console.log("Submitting Comment: ", comment);

            fetch(`/music/rate/${songId}/`, {
                method: "POST",
                headers: {
                    "X-CSRFToken": getCSRFToken(),
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    rating: selectedValue,
                    comment: comment
                })
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    console.log("Success: Rating updated on the server.");
                    location.reload();  // Reload the page to reflect the new rating
                } else {
                    console.error("Error Updating Rating:", data.error);
                    alert("Error updating rating: " + (data.error || "Unknown error"));
                }
            })
            .catch(error => {
                console.error("Fetch Request Failed:", error);
            });
        });
    });

    function getCSRFToken() {
        return document.querySelector('[name=csrfmiddlewaretoken]').value;
    }
});
