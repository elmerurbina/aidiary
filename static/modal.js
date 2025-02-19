const openModalButton = document.querySelector('.show-profile');
const modal = document.querySelector('.modal');
const closeModalButton = document.querySelector('.modal-close');
const content = document.querySelector('.modal-content');
const profileForm = document.querySelector('#profile-form');
const tabs = document.querySelectorAll('.tab');
const profileTab = document.querySelector('.profile-tab');
const settingsTab = document.querySelector('.settings-tab');

openModalButton.addEventListener('click', function () {
  modal.classList.add('show');
  content.classList.remove('slideOut');
  content.classList.add('slideIn');
});

closeModalButton.addEventListener('click', function () {
  content.classList.add('slideOut');
  content.classList.remove('slideIn');
  modal.classList.remove('show');
});

profileForm.addEventListener('submit', function submitProfileForm(event) {
  event.preventDefault();

  const form = event.target;
  const formData = new FormData(form);

  fetch(form.action, {
    method: 'POST',
    body: formData,
  })
    .then(response => response.json())
    .then(data => {
      if (data.message) {
        alert(data.message);
      }
      content.classList.remove('slideIn');
      content.classList.add('slideOut');
      setTimeout(() => {
        modal.classList.remove('show');
      }, 500);
    })
    .catch(error => {
      console.error('Error:', error);
    });
});

tabs.forEach(tab => {
  tab.addEventListener('click', function () {
    document.querySelector('.tab.selected').classList.remove('selected');
    tab.classList.add('selected');

    if (tab.textContent.includes('Cuenta')) {
      profileTab.classList.add('selected-tab');
      settingsTab.classList.remove('selected-tab');
    } else {
      settingsTab.classList.add('selected-tab');
      profileTab.classList.remove('selected-tab');
    }
  });
});
