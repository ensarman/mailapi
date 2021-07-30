

// restrict all imputs with class restrict-numbers to only numbers
const restrict_to_numbers = () => {
    inputs = document.querySelectorAll("input.restrict-numbers");

    for (let input of inputs){
        input.onkeydown = (e) => {
            const AllowedKeys = [
                'Backspace',
                'Delete' ,
                'Control',
                'Alt',
                'Insert',
                'Home',
                'End',
                'Enter',
                'ArrowUp',
                'ArrowDown',
                'ArrowLeft',
                'ArrowRight',
                'Shift'

            ];
            re = /^[0-9]$/;
            if (AllowedKeys.includes(e.key) || re.test(e.key) ){
                return;
            }
            else{
                e.preventDefault();
            }
        }
    }
}

// fixes the email putting the corresponding domain
const fix_domain = (input, domain) => {
    // input must be an input form  DOM element
    input.onchange = (e) => {
        //const domain = domain;
        const re = /^(([^<>()\[\]\.,;:\s@\"]+(\.[^<>()\[\]\.,;:\s@\"]+)*)|(\".+\"))@(([^<>()[\]\.,;:\s@\"]+\.)+[^<>()[\]\.,;:\s@\"]{2,})$/i;
        if (e.target.value == `@${domain}`){
          e.target.value = `@${domain}`;
        }
        else if (!e.target.value.match(re))
          e.target.value = `${e.target.value}@${domain}`;
        else{
          const address = e.target.value.split('@')[0];
          e.target.value = `${address}@${domain}`;
        }
      };
}
