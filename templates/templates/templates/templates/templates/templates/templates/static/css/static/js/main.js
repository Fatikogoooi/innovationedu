function toggleMenu() {
  document.getElementById('mobileMenu').classList.toggle('open');
}

document.querySelectorAll('.nav-link').forEach(link => {
  if (link.href === window.location.href) {
    link.style.background = 'var(--surface-2)';
    link.style.color = 'var(--ink)';
  }
});
