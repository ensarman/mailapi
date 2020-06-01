let th;
let close_button;
let search_button = $('.search-button');

function replace_search() {
    th = search_button.closest('th');
    th.on('click', 'a',function(event) {
        event.preventDefault();
        th = $(this).closest('th');
        const contenido = th.html();
        const input = $('<input>');
        close_button = $('<a href="#" class="input-group-text"><strong>&times;</strong></a>');

        input.attr({
            'type': (($(this).hasClass('search-button-date')) ? 'date' : 'text'),
            'name': th.attr('id'),
            'placeholder': th.text().trim(),
            'class': 'form-control',
        });

        const input_group = $(`<div class="input-group mb-3"></div>`);
        const input_group_append = $('<div class="input-group-append"></div>');
        input_group_append.append(close_button);

        input_group.append(input, input_group_append);

        th.empty();
        th.append(input_group);

        input.unbind();
        input.keyup(function (event) {

            if (event.keyCode === 13) {
                console.log(event.keyCode);
                $(this).closest('form').submit();
            }
        });
        close_button.click(function () {
            th.empty();
            th.html(contenido);
        });
        input.focus()
    });
    return close_button;
}

close_button = replace_search();


