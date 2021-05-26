function handleFileSelectDecorator(output_id) {
    function handleFileSelect(evt) {
    var file = evt.target.files;
    var f = file[0];

    if (!f.type.match('image.*')) {
        alert("Image only please....");
    }
    var reader = new FileReader();

    reader.onload = (function(theFile) {
        return function(e) {
            var span = document.createElement('span');
            span.innerHTML = ['<img class="card-img-top" alt="image" style="padding-top: 7px;" title="', escape(theFile.name), '" src="', e.target.result, '" />'].join('');
            var elem = document.getElementById(output_id);

            if (elem.childNodes[0]) {
                elem.replaceChild(span, elem.childNodes[0]);
            }
            else {
                elem.insertBefore(span, null);
            }

        };
    })(f);

    reader.readAsDataURL(f);
    }
    return handleFileSelect
}

function handleFileSelectSet(input_id, output_id) {
    document.getElementById(input_id).addEventListener('change', handleFileSelectDecorator(output_id), false);
}