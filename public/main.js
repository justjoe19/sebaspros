const year = document.getElementById('year');
if (year) year.textContent = new Date().getFullYear();

// Hide the mobile quick-contact bar while the form is on screen so it never covers it.
const dock = document.querySelector('.dock');

// Messages shown by this script, matched to the page language.
const text = document.documentElement.lang === 'es'
  ? {
      captcha: 'Marque la casilla "No soy un robot".',
      sending: 'Enviando…',
      failed: 'Lo sentimos, no se pudo enviar. Llame o envíe un mensaje al 574-360-5040.',
    }
  : {
      captcha: 'Please check the "I\'m not a robot" box.',
      sending: 'Sending…',
      failed: 'Sorry, that did not send. Please call or text 574-360-5040.',
    };

// Switching language keeps the visitor in the same section of the page.
document.querySelectorAll('.lang a').forEach((link) => {
  link.addEventListener('click', (event) => {
    if (link.classList.contains('active')) event.preventDefault();
    else link.hash = location.hash;
  });
});
const form = document.querySelector('form[name="estimate"]');
if (dock && form) {
  new IntersectionObserver(([entry]) => dock.classList.toggle('hide', entry.isIntersecting)).observe(form.parentElement);
}

// Format phone numbers as 574-555-0123 while they are typed, pasted or autofilled.
const phone = form?.elements.phone;
if (phone) {
  // US area codes never start with 1, so a leading 1 is the country code.
  const digitsOf = (text) => text.replace(/\D/g, '').replace(/^1/, '');
  const format = (d) => [d.slice(0, 3), d.slice(3, 6), d.slice(6, 10)].filter(Boolean).join('-');
  let previous = '';
  phone.addEventListener('input', (event) => {
    const caret = phone.selectionStart ?? phone.value.length;
    let digits = digitsOf(phone.value);
    let before = digitsOf(phone.value.slice(0, caret)).length;
    // Backspacing over a dash should remove the digit in front of it.
    if (event.inputType === 'deleteContentBackward' && digits === previous && before > 0) {
      digits = digits.slice(0, before - 1) + digits.slice(before);
      before -= 1;
    }
    previous = digits.slice(0, 10);
    phone.value = format(previous);
    if (document.activeElement === phone) {
      let position = 0;
      for (let seen = 0; position < phone.value.length && seen < before; position += 1) {
        if (phone.value[position] !== '-') seen += 1;
      }
      phone.setSelectionRange(position, position);
    }
  });
  form.addEventListener('reset', () => { previous = ''; });
}

if (form) {
  const sent = form.parentElement.querySelector('.sent');
  sent.querySelector('.reset').addEventListener('click', () => {
    sent.hidden = true;
    form.hidden = false;
    form.elements['name'].focus();
  });
  const status = form.querySelector('.status');
  const button = form.querySelector('button[type="submit"]');
  form.addEventListener('submit', async (event) => {
    event.preventDefault();
    // Netlify adds the reCAPTCHA widget at deploy time; its answer travels in this field.
    const captcha = form.querySelector('[name="g-recaptcha-response"]');
    if (captcha && !captcha.value) {
      status.classList.add('error');
      status.textContent = text.captcha;
      return;
    }
    button.disabled = true;
    status.classList.remove('error');
    status.textContent = text.sending;
    try {
      const response = await fetch('/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
        body: new URLSearchParams(new FormData(form)).toString(),
      });
      if (!response.ok) throw new Error(response.status);
      form.reset();
      status.textContent = '';
      form.hidden = true;
      sent.hidden = false;
      sent.focus({ preventScroll: true });
      sent.scrollIntoView({ block: 'center' });
    } catch {
      status.classList.add('error');
      status.textContent = text.failed;
    } finally {
      button.disabled = false;
      window.grecaptcha?.reset(); // each answer can only be used once
    }
  });
}
