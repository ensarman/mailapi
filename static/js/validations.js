

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

