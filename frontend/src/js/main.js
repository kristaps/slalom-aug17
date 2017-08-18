var foundation = require('../../node_modules/foundation-sites/dist/js/foundation.js');
var Rx = require('rxjs/Rx');

$(document).foundation();

// Airport search options
var airportSearchOptions = {

	url: function(phrase) {
		return `https://private-anon-eeaec2e728-locations10.apiary-mock.com/?term=${phrase}&locale=en-US&location_types=airport&limit=20&partner=picky`;
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
	listLocation: "locations",
	preparePostData: function(data) {
		data.phrase = $("#airport-search-input").val();
		return data;
	},
	list: {
		onChooseEvent: function() {
			console.log($("#airport-search-input").getSelectedItemData());
		}
	},
	requestDelay: 400,
	theme: "square"

};

// Medical service search options
var serviceSearchOptions = {

	url: function(phrase) {
		return `here_goes_python_api_search_url`;
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
			console.log($("#service-search-input").getSelectedItemData());
		}
	},
	requestDelay: 400,
	theme: "square"

};

// Initialize autocomplete plugn on search fields
$("#airport-search-input").easyAutocomplete(airportSearchOptions);
$("#service-search-input").easyAutocomplete(serviceSearchOptions);



