const get_modal = (pk, name, url, csrf_token) => {
  for (let modal in document.querySelectorAll(".modal")) {
    delete modal;
  }

  let modal = document.createElement("div");
  modal.setAttribute("id", `modal-${pk}`);
  modal.setAttribute("tabindex", "-1");
  modal.setAttribute("role", "dialog");
  modal.setAttribute("aria-labelledby", "ModalLabel");
  modal.setAttribute("aria-hidden", "true");
  modal.classList.add("modal", "fade");

  modal.innerHTML = `
        <div class="modal-dialog">
          <div class="modal-content">
            <div class="modal-header">
              <h5 class="modal-title" id="ModalLabel">Are You Sure</h5>
              <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close">
              </button>
            </div>
            <div class="modal-body">
              <p>Are You sure to delete <strong>${name}</strong></p>
            </div>
            <div class="modal-footer">
              <form method="post" action="${url}">
                <input type="hidden" name="csrfmiddlewaretoken" value="${csrf_token}">
                <button type="button" class="btn btn-outline-secondary" data-bs-dismiss="modal">Close</button>
                <button type="submit" class="btn btn-outline-primary">Delete</button>
              </form>
            </div>
          </div>
        </div>
      `.trim();

  bsmodal = new bootstrap.Modal(modal);
  modal.addEventListener("hidden.bs.modal", (event) => {
    delete bsmodal;
  });
  bsmodal.show();
};
