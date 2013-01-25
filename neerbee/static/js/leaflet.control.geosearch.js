/*
 * L.Control.GeoSearch - search for an address and zoom to it's location
 * https://github.com/smeijer/leaflet.control.geosearch
 */

L.GeoSearch = {};
L.GeoSearch.Provider = {};

L.GeoSearch.Result = function (x, y, label, postal_code, neighborhood, formatted_address) {
    this.X = x;
    this.Y = y;
    this.Label = label;
    this.postal_code = postal_code;
    this.neighborhood = neighborhood;
    this.formatted_address = formatted_address;
};

L.Control.GeoSearch = L.Control.extend({
    options: {
        position: 'topright'
    },

    initialize: function (options) {
        this._config = {};
        this.setConfig(options);
    },

    setConfig: function (options) {
        this._config = {
            'country': options.country || '',
            'provider': options.provider,
            
            'notFoundMessage' : options.notFoundMessage || 'Sorry, that address could not be found.',
            'messageHideDelay': options.messageHideDelay || 3000,
            'zoomLevel': options.zoomLevel || 18
        };
    },

    onAdd: function (map) {
        var $controlContainer = $(map._controlContainer);

        if ($controlContainer.children('.leaflet-top.leaflet-center').length == 0) {
            $controlContainer.append('<div class="leaflet-top leaflet-center"></div>');
            map._controlCorners.topcenter = $controlContainer.children('.leaflet-top.leaflet-center').first()[0];
        }

        this._map = map;
        this._container = L.DomUtil.create('div', 'leaflet-control-geosearch');

        var msgbox = document.createElement('div');
        msgbox.id = 'leaflet-control-geosearch-msg';
        msgbox.className = 'leaflet-control-geosearch-msg';
        this._msgbox = msgbox;

        var resultslist = document.createElement('ul');
        resultslist.id = 'leaflet-control-geosearch-results';
        this._resultslist = resultslist;

        $(this._msgbox).append(this._resultslist);
        $(this._container).append(this._searchbox, this._msgbox);

        L.DomEvent.addListener(this._container, 'click', L.DomEvent.stop);

        L.DomEvent.disableClickPropagation(this._container);

        return this._container;
    },
    
    geosearch: function (qry) {
        try {
            var provider = this._config.provider;
            var url = provider.GetServiceUrl(qry);

            $.getJSON(url, function (data) {
                try {
                    var results = provider.ParseJSON(data);
                    if (results.length == 0)
                        throw this._config.notFoundMessage;
                    this._showLocation(results[0].X, results[0].Y);
                    geoResults = results;

                    i = 0;
                    $('#id_address_results').append('<ul>');
                    while(results[i].formatted_address) {
                        $('#id_address_results').append('<li><a onClick="geoResultShow(\'' + i + '\');" href="#">' +  results[i].formatted_address + '</a></li>');
                        i++;
                    }
                    $('#id_address_results').append('</ul>');

                }
                catch (error) {
                    this._printError(error);
                }
            }.bind(this));
        }
        catch (error) {
            this._printError(error);
        }
    },
    
    _showLocation: function (x, y) {
        if (typeof this._positionMarker === 'undefined')
            this._positionMarker = L.marker([y, x]).addTo(this._map);
        else
            this._positionMarker.setLatLng([y, x]);

        this._map.setView([y, x], this._config.zoomLevel, false);
    },

    _printError: function(message) {
        $(this._resultslist)
            .html('<li>'+message+'</li>')
            .fadeIn('slow').delay(this._config.messageHideDelay).fadeOut('slow',
                    function () { $(this).html(''); });
    },
    
});