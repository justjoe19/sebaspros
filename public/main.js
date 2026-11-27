const year = document.getElementById('year');
if (year) year.textContent = new Date().getFullYear();

// Hide the mobile quick-contact bar while the form is on screen so it never covers it.
const dock = document.querySelector('.dock');
const form = document.querySelector('form[name="estimate"]');
if (dock && form) {
  new IntersectionObserver(([entry]) => dock.classList.toggle('hide', entry.isIntersecting)).observe(form);
}

if (form) {
  const status = form.querySelector('.status');
  const button = form.querySelector('button[type="submit"]');
  form.addEventListener('submit', async (event) => {
    event.preventDefault();
    button.disabled = true;
    status.classList.remove('error');
    status.textContent = 'Sending…';
    try {
      const response = await fetch('/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
        body: new URLSearchParams(new FormData(form)).toString(),
      });
      if (!response.ok) throw new Error(response.status);
      form.reset();
      status.textContent = 'Thanks! Your request was sent. Sebastian will be in touch soon.';
    } catch {
      status.classList.add('error');
      status.textContent = 'Sorry, that did not send. Please call or text 574-360-5040.';
    } finally {
      button.disabled = false;
    }
  });
}
