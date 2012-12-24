$(function() {

	var NeerbeeSearch = {};
	window.NeerbeeSearch = NeerbeeSearch;

	var template = function(name) {
		return Mustache.compile($('#'+name+'-template').html());
	};

	NeerbeeSearch.Result = Backbone.Model.extend({
		name: function() { return this.get('name'); },
		location: function() { return this.get('location'); }
	});

	NeerbeeSearch.Results = Backbone.Collection.extend({
		model: NeerbeeSearch.Result,
		url: "/api/v1/spot/search/?format=json"
	});

	NeerbeeSearch.Index = Backbone.View.extend({
		template: template('index'),
		initialize: function() {
			this.results = new NeerbeeSearch.Results();
			this.results.fetch({ "q": $("#input-search-query").val() });
		},
		render: function() {
			this.$el.html(this.template(this));
			var resultsView = new NeerbeeSearch.Index.Results({ collection: this.results });
			var form = new NeerbeeSearch.Index.Form({ collection: this.results });
			this.$('.results').append(form.render().el);
			this.$('.results').append(resultsView.render().el);
			return this;
		},
		count: function() {
			return this.results.length;
		}
	});

	NeerbeeSearch.Index.Form = Backbone.View.extend({
		tagName: 'form',
		className: 'form',
		template: template('index-form'),
		events: {
			'keypress #input-search-query': 'displaySearch'
		},
		render: function() {
			this.$el.html(this.template(this));
			return this;
		},
		displaySearch: function(event) {
			this.collection.fetch({ "q": $("#input-search-query").val() });
		}
	});

	NeerbeeSearch.Index.Result = Backbone.View.extend({
		tagName: 'li',
		template: template('index-result'),
		events: {
			// TODO: click on result
		},
		render: function() {
			this.$el.html(this.template(this));
			return this;
		},
		name: function() { return this.model.get('name'); },
		//location: function() { return this.model.get('location'); }
		// TODO: click function
	});

	NeerbeeSearch.Index.Results = Backbone.View.extend({
		tagName: 'ul',
		render: function() {
			this.collection.each(
				function(result) {
					var view = new NeerbeeSearch.Index.Result({ model: result });
					this.$el.append(view.render().el);
				},
				this
			);
			return this;
		}
	});

	NeerbeeSearch.Router = Backbone.Router.extend({
		initialize: function(options) {
			this.el = options.el;
		},
		routes: {
			"": "index"
		},
		index: function() {
			var view = new NeerbeeSearch.Index();
			this.el.empty();
			this.el.append(view.render().el);
		}
	});

	NeerbeeSearch.boot = function(container) {
		container = $(container);
		var router = new NeerbeeSearch.Router({ el: container });
		Backbone.history.start();
	}

});
