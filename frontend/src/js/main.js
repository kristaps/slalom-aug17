let foundation = require('../../node_modules/foundation-sites/dist/js/foundation.js');

$(document).foundation();

// Medical service search options
let serviceSearchOptions = {

	url: function(phrase) {
		return `https://medincluded.com/api/services?term=${phrase}`;
	},
	getValue: function(element) {
		return element.name;
	},
	ajaxSettings: {
		dataType: "json",
		method: "GET",
		data: {
			dataType: "json"
		}
	},
	preparePostData: function(data) {
		data.phrase = $("#service-search-input").val();
		return data;
	},
	list: {
		onChooseEvent: function() {
			window.location.href = `${window.location.origin}/providers.html`;
		}
	},
	requestDelay: 400,
	theme: "square"

};

// Initialize autocomplete plugn on search fields
$("#service-search-input").easyAutocomplete(serviceSearchOptions);


//set click handler for hot-it-works button
$("#how-it-works-btn").click(() => {
	$('html, body').animate({
		scrollTop: $('#how-it-works').offset().top
	}, 500);
});



