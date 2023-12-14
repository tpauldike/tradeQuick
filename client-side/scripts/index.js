

document.addEventListener('DOMContentLoaded', function () {
    const mobileMenuToggle = document.getElementById('mobile-menu');
    const navList = document.querySelector('.nav-list');
  
    mobileMenuToggle.addEventListener('click', function () {
      navList.classList.toggle('show');
    });
  });