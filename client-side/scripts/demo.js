let popedUp = false;

const closeBtn = document.getElementById('close');
const ellipseBtn = document.getElementById('demo');
const popUpContainer = document.getElementById('popup-container');

const showOrHidePopup = () => {
    if (!popedUp) {
        popUpContainer.style.display = 'block'
        popUpContainer.style.opacity = 1;
        popedUp = true;
    } else {
        popUpContainer.style.display = 'none';
        popUpContainer.style.opacity = 0.5;
        popedUp = false;
    }
}

ellipseBtn.addEventListener('click', showOrHidePopup);
closeBtn.addEventListener('click', showOrHidePopup);
