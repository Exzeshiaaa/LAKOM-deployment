const hamburger = document.querySelector('.hamburger');
const navLink = document.querySelector('.nav__link');

hamburger.addEventListener('click', () => {
  navLink.classList.toggle('hide');
});

function addBreak() {
  var screenWidth = window.innerWidth || document.documentElement.clientWidth || document.body.clientWidth;

  var headingElement = document.getElementById('main-desc-h2');

  if (screenWidth < 661) {
    headingElement.innerHTML = 'Want to archive a fake news post? <br /> Submit it to our website!';
  } else {
    headingElement.innerHTML = 'Want to archive a fake news post? Submit it to our website!';
  }
}

// Call the function when the page loads and on resize
window.onload = addBreak;
window.onresize = addBreak;