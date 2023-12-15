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


// document.addEventListener('DOMContentLoaded', function () {
//   const mobileMenuToggle = document.getElementById('mobile-menu');
//   const navList = document.querySelector('.nav-list');

//   mobileMenuToggle.addEventListener('click', function () {
//     navList.classList.toggle('show');
//   });
// });
