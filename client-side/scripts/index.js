const icons = [{
  htmlClass: '.likes',
  imgSrc: './assets/like.png'
},
{
  htmlClass: '.dislikes',
  imgSrc: './assets/dislike.png'
},
{
  htmlClass: '.add-to-cart',
  imgSrc: './assets/add-to-cart.png'
},
{
  htmlClass: '.comment',
  imgSrc: './assets/comment.png'
},
{
  htmlClass: '.ellipse',
  imgSrc: './assets/ellipse.png'
}
];

const menu = document.getElementById('nav-list');
const menuToggle = document.getElementById('menu-toggle');
const mobileSearchBar = document.getElementById('mobile-search-bar-input');
const mobileSearchIcon = document.getElementById('mobile-search-icon');

let menuDisplayed = false;
let searchBarDisplayed = false;

const displaySocialInteractions = (htmlClass, imgSrc) => {
  const htmlClassList = document.querySelectorAll(htmlClass);

  htmlClassList.forEach(htmlElement => {
    const img = document.createElement('img');
    img.src = imgSrc;
    htmlElement.appendChild(img);
  });
};

document.addEventListener('DOMContentLoaded', () => {
  icons.map((icon) => {
    displaySocialInteractions(icon.htmlClass, icon.imgSrc)
  })
});

menuToggle.addEventListener('click', () => {
  menu.style.display = !menuDisplayed ? 'block' : 'none';
  menuDisplayed = menuDisplayed === false ? true : false
});

mobileSearchIcon.addEventListener('click', () => {
  mobileSearchBar.style.display = !searchBarDisplayed ? 'block' : 'none';
  searchBarDisplayed = searchBarDisplayed === false ? true : false
});
