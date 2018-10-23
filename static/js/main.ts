const $ = function(selector) {
    let selectorType = 'querySelectorAll';

    if (selector.indexOf('#') === 0) {
        selectorType = 'getElementById';
        selector = selector.substr(1, selector.length);
    }

    return document[selectorType](selector);
};



document.addEventListener('DOMContentLoaded', function() {

});
