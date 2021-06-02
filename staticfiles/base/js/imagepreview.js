function handleFileSelectDecorator(parent_html, output_class) {
    function handleFileSelect(evt) {
    var file = evt.target.files;
    var f = file[0];

    if (!f.type.match('image.*')) {
        alert("Image only please....");
    }
    var reader = new FileReader();

    reader.onload = (function(theFile) {
        return function(e) {
            let image = parent_html.getElementsByClass(output_class)
            image.title = escape(theFile.name)
            image.stc = e.target.result
        };
    })(f);

    reader.readAsDataURL(f);
    }
    return handleFileSelect
}

function handleFileSelectSet(parent_html, input_class, output_class) {
    parent_html.getElementByClass(input_class)[0].addEventListener('change', handleFileSelectDecorator(parent_html, output_class), false);
}