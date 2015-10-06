// An example Backbone application contributed by
// [Jérôme Gravel-Niquet](http://jgn.me/). This demo uses a simple
// [LocalStorage adapter](backbone-localstorage.html)
// to persist Backbone models within your browser.

// Load the application once the DOM is ready, using `jQuery.ready`:
$(function(){

  // Todo Model
  // ----------

  // Our basic **Todo** model has `title`, `order`, and `done` attributes.
  var Todo = Backbone.Model.extend({

    // Default attributes for the todo item.
    defaults: function() {
      return {
        username: "empty username",
        email: "empty email",
        order: Todos.nextOrder()
      };
    },

    // Ensure that each todo created has `title`.
    initialize: function() {
      
      if (!this.get("username")) {
        this.set({"username": this.defaults().username});
      }
      
      if (!this.get("email")) {
        this.set({"email": this.defaults().email});
      }
      
      this.on("error", function(model, error){
			console.log(error);
		});
		
    }

  });

	//get the collection url
	function get_collection_url()
	{
		var loc = String(window.location);
		if(loc.charAt(loc.length-1) == '/')
		{
			return loc + 'api/users';
		}else
		{
			return loc + '/api/users';
		}
	}

  // Todo Collection
  // ---------------

  // The collection of todos is backed by *localStorage* instead of a remote
  // server.
  var TodoList = Backbone.Collection.extend({

    // Reference to this collection's model.
    model: Todo,

    // Save all of the todo items under the `"todos-backbone"` namespace.
    //localStorage: new Backbone.LocalStorage("todos-backbone"),
    
    // Flask API server
    url:  get_collection_url(),

    // We keep the Todos in sequential order, despite being saved by unordered
    // GUID in the database. This generates the next order number for new items.
    nextOrder: function() {
      if (!this.length) return 1;
      return this.last().get('order') + 1;
    },

    // Todos are sorted by their original insertion order.
    comparator: function(todo) {
      return todo.get('order');
    }

  });

  // Create our global collection of **Todos**.
  var Todos = new TodoList;

  // Todo Item View
  // --------------

  // The DOM element for a todo item...
  var TodoView = Backbone.View.extend({

    //... is a list tag.
    tagName:  "tr",

    // Cache the template function for a single item.
    template: _.template($('#item-template').html()),

    // The DOM events specific to an item.
    events: {
      "dblclick .view"  : "edit",
      "click a.destroy" : "clear",
      "keypress input"  : "updateOnEnter",
      "blur input"      : "close"
    },

    // The TodoView listens for changes to its model, re-rendering. Since there's
    // a one-to-one correspondence between a **Todo** and a **TodoView** in this
    // app, we set a direct reference on the model for convenience.
    initialize: function() {
      this.listenTo(this.model, 'change', this.render);
      this.listenTo(this.model, 'destroy', this.remove);
    },

    // Re-render the titles of the todo item.
    render: function() {
      this.$el.html(this.template(this.model.toJSON()));
      this.input_username = this.$('.input_username');
      this.input_email = this.$('.input_email');
      
      $("#users-table").prepend(this.el);

      return this;
    },

    // Switch this view into `"editing"` mode, displaying the input field.
    edit: function(ev) {
      this.$el.addClass("editing");
      ev.target.nextSibling.nextSibling.focus();
    },

    // Close the `"editing"` mode, saving changes to the todo.
    close: function() {
      var i_user = this.input_username.val();
      var i_eml = this.input_email.val();
      
      if (!i_user && !i_eml) {
        this.clear();
      } else {
        this.model.save({username: i_user, email: i_eml});
        this.$el.removeClass("editing");
      }
    },

    // If you hit `enter`, we're through editing the item.
    updateOnEnter: function(e) {
      if (e.keyCode == 13) this.close();
    },

    // Remove the item, destroy the model.
    clear: function() {
      this.model.destroy();
    }

  });

  // The Application
  // ---------------

  // Our overall **AppView** is the top-level piece of UI.
  var AppView = Backbone.View.extend({

    // Instead of generating a new element, bind to the existing skeleton of
    // the App already present in the HTML.
    el: $("#main-app"),

    // Delegated events for creating new items, and clearing completed ones.
    events: {
      "keypress #new-user":  "createOnEnter",
      "keypress #new-email":  "createOnEnter"
    },

    // At initialization we bind to the relevant events on the `Todos`
    // collection, when items are added or changed. Kick things off by
    // loading any preexisting todos that might be saved in *localStorage*.
    initialize: function() {

      this.input_user = this.$("#new-user");
      this.input_email = this.$("#new-email");

      this.listenTo(Todos, 'add', this.addOne);
      this.listenTo(Todos, 'reset', this.addAll);
      this.listenTo(Todos, 'all', this.render);

      Todos.fetch();
    },

    // Re-rendering the App just means refreshing the statistics -- the rest
    // of the app doesn't change.
    render: function() {
    },

    // Add a single todo item to the list by creating a view for it, and
    // appending its element to the table.
    addOne: function(todo) {
      var view = new TodoView({model: todo});
      view.render();
    },

    // Add all items in the **Todos** collection at once.
    addAll: function() {
      Todos.each(this.addOne);
    },

    // If you hit return in the main input field, create new **Todo** model,
    // persisting it to *localStorage*.
    createOnEnter: function(e) {
      if (e.keyCode != 13) return;
      if (!this.input_user.val() || !this.input_email.val() ) return;

      Todos.create( {username: this.input_user.val(), email: this.input_email.val()} );
      
      this.input_user.val('');
      this.input_email.val('');
    },

    // Clear all done todo items, destroying their models.
    clearCompleted: function() {
      _.invoke(Todos.done(), 'destroy');
      return false;
    }

  });

  // Finally, we kick things off by creating the **App**.
  var App = new AppView;

});
