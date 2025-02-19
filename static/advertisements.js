document.addEventListener("DOMContentLoaded", function () {
  const advertisements = document.querySelectorAll(".advertisement");

  advertisements.forEach(function (advertisement) {
    let close_button = advertisement.querySelector(".close-button");
    close_button.addEventListener("click", function () {
      advertisement.classList.add("slideOut");
    });
  });
});