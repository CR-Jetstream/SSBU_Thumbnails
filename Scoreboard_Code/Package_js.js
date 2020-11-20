function elemHide(elem) {
    return function (next) {
        $(elem).addClass('hidden');
        next();
    }
}

function elemShow(elem) {
    return function (next) {
        $(elem).removeClass('hidden');
        next();
    }
}

function elemUpdate() {
    return function (next) {
        for (var prop in docData) {
            $('#'+prop).text(docData[prop]);
        }
        next();
    }
}

function elemUpdateSingle(elem) {
    return function (next) {   
		$('#'+elem).text(docData[elem]);
        next();
    }
}