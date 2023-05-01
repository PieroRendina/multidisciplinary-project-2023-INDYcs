var button = document.querySelector('.play-pause-button');

button.addEventListener('click', function() {
  button.classList.toggle('paused');
});