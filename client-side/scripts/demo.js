const newPasswordForm = document.querySelector('#new-password-form');
const otpForm = document.querySelector('#otp-submission-form');
const resetPasswordForm = document.querySelector('#password-reset-form');
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

const displayOTPForm = () => {
    newPasswordForm.style.display = 'none'
    otpForm.style.display = 'block';
}

const displayNewPasswordForm = () => {
    newPasswordForm.style.display = 'none'
    otpForm.style.display = 'none'
    newPasswordForm.style.display = 'block';
}