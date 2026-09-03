// Toggle navbar menu
function toggleMenu() {
  document.getElementById("navLinks").classList.toggle("active");
}

// Handle booking form submission
document.addEventListener("DOMContentLoaded", () => {
  const form = document.querySelector(".booking-form");
  form.addEventListener("submit", (e) => {
    e.preventDefault();
    alert("Thank you for booking with The Kumbh Travels! We will contact you soon.");
    form.reset();
  });
});
