document.addEventListener("DOMContentLoaded", function () {
    let selectedRatings = {};

    // Handle Star Selection
    document.querySelectorAll(".star").forEach(star => {
        star.addEventListener("click", function () {
            const drinkId = this.closest(".rating-section").querySelector(".submit-rating").dataset.drinkId;
            const ratingValue = parseInt(this.getAttribute("data-value"));
            selectedRatings[drinkId] = ratingValue;

            // Highlight all preceding stars including the selected one
            const stars = this.parentElement.querySelectorAll(".star");
            stars.forEach(s => {
                const starValue = parseInt(s.getAttribute("data-value"));
                if (starValue <= ratingValue) {
                    s.classList.add("selected");
                } else {
                    s.classList.remove("selected");
                }
            });
        });
    });

    // Submit Rating via AJAX
    document.querySelectorAll(".submit-rating").forEach(button => {
        button.addEventListener("click", function () {
            const drinkId = this.dataset.drinkId;
            const selectedRating = selectedRatings[drinkId] || 0;
            const comment = document.getElementById(`rating-comment-${drinkId}`).value;
            const csrftoken = getCSRFToken();  // Ensure CSRF token is retrieved

            if (selectedRating === 0) {
                alert("Please select a rating before submitting.");
                return;
            }

            fetch(`/drink/${drinkId}/rate/`, {
                method: "POST",
                headers: {
                    "X-CSRFToken": csrftoken,
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    rating: selectedRating,
                    comment: comment
                })
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    alert("Rating submitted successfully!");

                    // Update rating display
                    document.querySelector(`.badge[data-drink-id="${drinkId}"]`).innerText = `⭐ ${data.new_avg_rating}/5`;

                    // Hide rating form
                    document.querySelector(`.submit-rating[data-drink-id="${drinkId}"]`).parentElement.innerHTML =
                        `<p class="text-success">Thank you for your rating!</p>`;
                } else {
                    alert("Error submitting rating: " + data.error);
                }
            })
            .catch(error => {
                alert("Failed to submit rating. Please try again.");
                console.error("Error:", error);
            });
        });
    });

    // Function to retrieve CSRF token from hidden input field
    function getCSRFToken() {
        return document.querySelector('[name=csrfmiddlewaretoken]').value;
    }
});
