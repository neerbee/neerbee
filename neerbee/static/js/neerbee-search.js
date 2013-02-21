$(function() {

	var Neerbee = {};
	window.Neerbee = Neerbee;

	var template = function(name) { return Mustache.compile($('#'+name+'-template').html()); };

	Neerbee.Router = Backbone.Router.extend({
		initialize: function(options) {
			this.el = options.el;
		},
		routes: {
			"": "search"
		},
		search: function() {
			var view = new Neerbee.Search();
			this.el.empty();
			this.el.append(view.render().el);
		}
	});

	Neerbee.boot = function(container) {
		container = $(container);
		var router = new Neerbee.Router({ el: container });
		Backbone.history.start();
	}

	Neerbee.Result = Backbone.Model.extend({
		name: function() { return this.get('name'); }
	});

	Neerbee.Results = Backbone.Collection.extend({
		model: Neerbee.Result,
		url: "/api/v1/spot/search/"
	});

	Neerbee.Search = Backbone.View.extend({
		initialize: function() {
			this.results = new Neerbee.Results();
			this.results.on('all', this.showResults, this);
		},
		render: function() {
			var resultsView = new Neerbee.Search.Results({ collection: this.results });
			var thisElement = this.$el;
			$("#input-search-query").keyup(function() {
				if (jQuery.trim($("#input-search-query").val()) != '') {
					$('#loading-image').remove();
					thisElement.prepend('<img id="loading-image" src="/static/img/loading.gif" />');
					resultsView.results().fetch({
						data:{"q":jQuery.trim($("#input-search-query").val())},
						error: function () {
							$('#loading-image').remove();
							//alert('Connection error. Maybe you are disconnected.');
						}
					});
				}
				else {
					$(".results-list").empty();
				}
			});
			this.$el.append(resultsView.render().el);
			return this;
		},
		showResults: function() {
			var resultsView = new Neerbee.Search.Results({ collection: this.results });
			this.$el.empty();
			this.$el.append(resultsView.render().el);
		},
		count: function() {
			return this.results.models[0].attributes.models.length;
		}
	});

	Neerbee.Search.Results = Backbone.View.extend({
		tagName: 'ul',
		className: 'nav nav-tabs nav-stacked results-list',
		render: function() {
			if (this.collection.models.length > 0) {
				var thisCollection = this.collection.models[0].attributes.models;
				for (var i = 0; i < thisCollection.length; i++) {
					var thisModel = thisCollection[i];
					this.renderItem(thisModel);
				}
			}
			return this;
		},
		renderItem: function (model) {
			var item = new Neerbee.Search.Result({
				"model": model
			});
			item.render().$el.appendTo(this.$el);
		},
		results: function() {
			return this.collection;
		}
	});

	Neerbee.Search.Result = Backbone.View.extend({
		tagName: "li",
		className: "result",
		template: template('result'),
		render: function () {
			this.$el.html(this.template(this));
			return this;
		},
		name: function() { 
			var thisName = highlightString(this.model.name, jQuery.trim($("#input-search-query").val()));
			return thisName; 
		},
		address: function() { return this.model.address; },
		neighbourhood: function() { return this.model.neighbourhood; },
		spot_url: function() { return this.model.spot_url; }
	});

});

function highlightString(inputString, highlightString) {
	inputString = inputString.replace(highlightString, '<span style="background-color: PaleTurquoise;">' + highlightString + '</span>');
	return inputString;
}
