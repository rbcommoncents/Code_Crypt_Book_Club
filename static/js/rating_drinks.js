document.addEventListener("DOMContentLoaded", function () {
    const stars = document.querySelectorAll(".star-rating input");
    const submitButtons = document.querySelectorAll(".submit-rating");

    stars.forEach(star => {
        star.addEventListener("change", function () {
            const ratingSection = this.closest(".rating-section");

            if (!ratingSection) {
                console.error("ERROR: .rating-section not found! Check HTML structure.");
                return;  // Exit function to prevent further errors
            }

            const drinkId = this.dataset.drinkId;
            const selectedValue = parseInt(this.value);

            console.log("Drink ID Retrieved:", drinkId);
            console.log("Selected Rating Value:", selectedValue);

            if (!drinkId) {
                console.error("ERROR: drinkId is undefined or not set correctly.");
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

            // Retrieve comment value
            const commentField = ratingSection.querySelector("textarea[name='comment']");
            const comment = commentField ? commentField.value.trim() : "";

            console.log("Comment Submitted:", comment);

            // Send rating update to server
            fetch(`/drinks/rate/${drinkId}/`, {
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
                    ratingDisplay.textContent = `Confirmed: ${selectedValue} Stars`;
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
