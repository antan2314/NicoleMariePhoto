/* ============================================================
   Nicole Marie Photo — site scripts
   ============================================================ */

/* ------------------------------------------------------------
   FORM ENDPOINT

   This is the only line that changes when you swap the hosted
   form handler for your own FastAPI service.

   Now:   Web3Forms (hosted, needs ACCESS_KEY below)
   Later: "https://nicolemariephoto.com/api/inquiries"
          — then set USE_WEB3FORMS to false so the access_key
            stops being sent.
   ------------------------------------------------------------ */
const FORM_ENDPOINT = "https://api.web3forms.com/submit";
const USE_WEB3FORMS = true;
const ACCESS_KEY = "PASTE_YOUR_WEB3FORMS_ACCESS_KEY_HERE";

/* ---------- Scroll reveal ---------------------------------- */
(function reveal() {
  const targets = document.querySelectorAll(".rise");
  if (!targets.length) return;

  const reduced = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  if (reduced || !("IntersectionObserver" in window)) {
    targets.forEach((el) => el.classList.add("is-in"));
    return;
  }

  const io = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (!entry.isIntersecting) return;
        entry.target.classList.add("is-in");
        io.unobserve(entry.target);
      });
    },
    { rootMargin: "0px 0px -8% 0px", threshold: 0.05 }
  );

  targets.forEach((el) => io.observe(el));
})();

/* ---------- Portfolio category filter ---------------------- */
(function filters() {
  const bar = document.querySelector("[data-filters]");
  if (!bar) return;

  const plates = document.querySelectorAll("[data-category]");

  bar.addEventListener("click", (event) => {
    const button = event.target.closest("button[data-filter]");
    if (!button) return;

    const want = button.dataset.filter;

    bar.querySelectorAll("button").forEach((b) => {
      b.setAttribute("aria-pressed", String(b === button));
    });

    plates.forEach((plate) => {
      const show = want === "all" || plate.dataset.category === want;
      plate.hidden = !show;
    });
  });
})();

/* ---------- Inquiry form ----------------------------------- */
(function inquiryForm() {
  const form = document.querySelector("[data-inquiry-form]");
  if (!form) return;

  const status = form.querySelector("[data-status]");
  const submit = form.querySelector("[type=submit]");
  const openedAt = Date.now();

  function say(message, tone) {
    status.textContent = message;
    status.hidden = false;
    status.style.borderLeftColor =
      tone === "error" ? "#a4453d" : "var(--brick)";
  }

  form.addEventListener("submit", async (event) => {
    event.preventDefault();
    status.hidden = true;

    const data = Object.fromEntries(new FormData(form).entries());

    /* Two cheap spam checks before anything leaves the browser.
       Neither replaces server-side validation — they just cut
       the volume of obvious junk. */
    if (data.botcheck) return;
    if (Date.now() - openedAt < 3000) {
      say("Give that another moment, then send.", "error");
      return;
    }
    delete data.botcheck;

    if (USE_WEB3FORMS) {
      data.access_key = ACCESS_KEY;
      data.subject = `New inquiry — ${data.name || "website"}`;
      data.from_name = "Nicole Marie Photo";
    }

    submit.disabled = true;
    submit.textContent = "Sending…";

    try {
      const response = await fetch(FORM_ENDPOINT, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Accept: "application/json",
        },
        body: JSON.stringify(data),
      });

      if (!response.ok) throw new Error(String(response.status));

      form.reset();
      say("Thanks — your note is on its way. Nicole usually replies within two days.");
      submit.textContent = "Sent";
    } catch (error) {
      say(
        "That didn't send. Email nicole_lovall@icloud.com directly and it'll get through.",
        "error"
      );
      submit.disabled = false;
      submit.textContent = "Send inquiry";
    }
  });
})();
