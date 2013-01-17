/**
 * L.Control.GeoSearch - search for an address and zoom to it's location
 * L.GeoSearch.Provider.Google uses google geocoding service
 * https://github.com/smeijer/leaflet.control.geosearch
 */

L.GeoSearch.Provider.Google = L.Class.extend({
    options: {

    },

    initialize: function(options) {
        options = L.Util.setOptions(this, options);
    },

    GetServiceUrl: function (qry) {
        var parameters = L.Util.extend({
            address: qry,
            sensor: false
        }, this.options);

        return 'http://maps.googleapis.com/maps/api/geocode/json'
            + L.Util.getParamString(parameters);
    },

    ParseJSON: function (data) {
        if (data.results.length == 0)
            return [];

        var results = [];

        for (var i = 0; i < data.results.length; i++) {

            var neighborhood = null;
            var postalcode = null;
            var address = null;

            for (var x = 0; x < data.results[i].address_components.length; x++) {
                if (data.results[i].address_components[x].types[0] == 'neighborhood') {
                    neighborhood = data.results[i].address_components[x].long_name;
                }
                else if (data.results[i].address_components[x].types[0] == 'locality' && neighborhood == null) {
                    neighborhood = data.results[i].address_components[x].long_name;
                }
                else if (data.results[i].address_components[x].types[0] == 'administrative_area_level_1' && neighborhood == null) {
                    neighborhood = data.results[i].address_components[x].long_name;
                }
                else if (data.results[i].address_components[x].types[0] == 'administrative_area_level_2' && neighborhood == null) {
                    neighborhood = data.results[i].address_components[x].long_name;
                }
                else if (data.results[i].address_components[x].types[0] == 'administrative_area_level_3' && neighborhood == null) {
                    neighborhood = data.results[i].address_components[x].long_name;
                }
                else if (data.results[i].address_components[x].types[0] == 'postal_code') {
                    postalcode = data.results[i].address_components[x].long_name;
                }
            }

            results.push(new L.GeoSearch.Result(
                data.results[i].geometry.location.lng, 
                data.results[i].geometry.location.lat, 
                data.results[i].formatted_address,
                postalcode,
                neighborhood
            ));

        }

        return results;
    }
});