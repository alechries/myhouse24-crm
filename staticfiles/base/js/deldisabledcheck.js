function check() {
    const btns = document.getElementsByClassName('del-measure-form')

    for(let i = 0; i < btns.length; i++) {
        const [text] = document.getElementsByClassName('measure-pk')

        $.get("/api/service/?measure="+1, function(data) {
        console.log(data)
            if(data.length !== 0) {
                btns[i].classList.add('disabled')
            }
        });
    }
}

check()
//$.get("/api/service/?measure="+1, function(data) {
//    console.log(data);
//});



    // del buttons - .del-measure-form
    // del measure pk - .del-measure-form div -> .measure-pk