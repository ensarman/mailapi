//let th;
//let close_button;
let search_buttons = document.querySelectorAll(".search-button");

function replace_search() {
  let close_buttons = [];
  for (const search_button of search_buttons) {
    const th = search_button.closest("th");
    //th.onclick = () => { };
    search_button.onclick = (event) => {
      event.preventDefault();

      //const previous_content = replace_th_with_search(th);

      //const previous_content = th.children;

      for (let element of th.querySelectorAll("*")) {
        element.classList.add("d-none");
      }

      //th.innerHTML = "";

      //console.log(previous_content);
      const input = document.createElement("input");
      input.setAttribute(
        "type",
        search_button.classList.contains("search-button-date") ? "date" : "text"
      );
      input.setAttribute("name", th.id);
      input.setAttribute("placeholder", th.innerText.trim());
      input.setAttribute("class", "form-control");

      const close_button = document.createElement("a");
      close_button.setAttribute("href", "#");
      close_button.setAttribute("class", "input-group-text");
      close_button.innerHTML = "<strong>&times;</strong>";

      const input_group = document.createElement("div");
      input_group.setAttribute("class", "input-group mb-3");

      const input_group_append = document.createElement("div");
      input_group.setAttribute("class", "input-group-append");
      input_group.appendChild(close_button);

      input_group.appendChild(input);
      input_group.appendChild(input_group_append);

      th.appendChild(input_group);

      input.onkeyup = (event) => {
        if (event.code === "Enter") {
          //console.log(event.code);
          event.target.closest("form").submit();
        }
      };

      close_button.onclick = (event) => {
        th.removeChild(input_group);
        for (let element of th.querySelectorAll("*")) {
          element.classList.remove("d-none");
        }
      };

      close_buttons.push(close_button);
    };
  }

  return close_buttons;
}

replace_search();
