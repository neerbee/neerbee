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

	Neerbee.Search = Backbone.View.extend({ //
		initialize: function() {
			this.results = new Neerbee.Results();
			this.results.on('all', this.showResults, this);
		},
		render: function() {

			var resultsView = new Neerbee.Search.Results({ collection: this.results });

			$("#input-search-query").keyup(function() {
				resultsView.results().fetch({data:{"q":$("#input-search-query").val()}});
			});

			this.$el.append(resultsView.render().el);
			return this;

		},
		showResults: function() {

			var resultsView = new Neerbee.Search.Results({ collection: this.results });

			this.$el.empty();
			this.$el.append(resultsView.render().el);

		}
	});

	Neerbee.Search.Results = Backbone.View.extend({
		tagName: 'ul',
		className: 'nav nav-tabs nav-stacked results-list',
		render: function() {
			for (var i = 0; i < this.collection.length; i++) {
				var thisModel = this.collection.models[i];
				if (thisModel.attributes.models[0]) {
					this.renderItem(thisModel);
				}
			};
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
			var thisName = this.model.attributes.models[0].name;
			thisName = thisName.replace($("#input-search-query").val(), '<span style="background-color: PaleTurquoise;">' + $("#input-search-query").val() + '</span>');
			return thisName; 
		},
		address: function() { return this.model.attributes.models[0].address; },
		neighbourhood: function() { return this.model.attributes.models[0].neighbourhood; },
		slug: function() { return this.model.attributes.models[0].slug; }
	});

});
