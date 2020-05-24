const get_modal = (pk, name, url, csrf_token) => {
      $('.modal').remove();

      const modal = document.createElement('div');
      modal.setAttribute('id', `modal-${pk}`);
      modal.setAttribute('tabindex', '-1');
      modal.setAttribute('role', 'dialog');
      modal.setAttribute('aria-labelledby', "ModalLabel");
      modal.setAttribute('aria-hidden', "true");
      modal.classList.add("modal", "fade");

      modal.innerHTML = `
        <div class="modal-dialog">
          <div class="modal-content">
            <div class="modal-header">
              <h5 class="modal-title" id="ModalLabel">Contiramtion</h5>
              <button type="button" class="close" data-dismiss="modal" aria-label="Close">
                <span aria-hidden="true">&times;</span>
              </button>
            </div>
            <div class="modal-body">
              <p>Are You sure to delete <strong>${name}</strong></p>
            </div>
            <div class="modal-footer">
              <form method="post" action="${url}">
                <input type="hidden" name="csrfmiddlewaretoken" value="${csrf_token}">
                <button type="button" class="btn btn-outline-secondary" data-dismiss="modal">Close</button>
                <button type="submit" class="btn btn-outline-primary">Delete</button>
              </form>
            </div>
          </div>
        </div>
      `.trim();

      $(modal).on('hidden.bs.modal', function () {
                $(this).remove();
            }).modal('show');
  };
