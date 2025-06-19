const slideContainer = document.querySelector('.slide');
const prev = document.getElementById('prev');
const next = document.getElementById('next');
const indicator = document.getElementById('indicator');
const slides = document.querySelectorAll('.slide > div');
const totalSlides = slides.length;
const slideWidth = 100 / totalSlides;
slideContainer.style.width = `${totalSlides * 100}%`;
slides.forEach((slide) => {
slide.style.width = `${slideWidth}%`;
});
let count = 0;
function updateSlidePosition() {
slideContainer.style.transform = `translateX(-${count * slideWidth}%)`;
}
function updateIndicatorColors() {
const lists = document.querySelectorAll('.list');
lists.forEach((list, i) => {
    list.style.backgroundColor = i === count % totalSlides ? '#000' : '#fff';
});
}
function nextClick() {
count++;
if (count >= totalSlides) {
    count = 0;
}
updateSlidePosition();
updateIndicatorColors();
}
function prevClick() {
count--;
if (count < 0) {
    count = totalSlides - 1;
}
updateSlidePosition();
updateIndicatorColors();
}
next.addEventListener('click', () => {
nextClick();
});
prev.addEventListener('click', () => {
prevClick();
});
indicator.addEventListener('click', (event) => {
if (event.target.classList.contains('list')) {
    const index = Array.from(indicator.children).indexOf(event.target);
    setActiveSlide(index);
}
});
function setActiveSlide(index) {
count = index;
updateSlidePosition();
updateIndicatorColors();
}
updateIndicatorColors();