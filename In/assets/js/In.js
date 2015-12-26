window.IN = { config: {}, callbacks:{}, window_in_focus:true, audioElement : document.createElement('audio') };

define('In', ['jQuery', 'once', 'jQuery_form',  'uikit!notify' ], function() {
"use strict";

(function ($) {

  // element destroyed event
  $.event.special.destroyed = {
    remove: function(o) {
      if (o.handler) { //  && o.type !== 'destroyed'
        o.handler();
      }
    }
  }

  IN.on = function(e, m, n, f) {
    this.calls = this.calls || {};
    this.calls[e] = this.calls[e] || {};
    this.calls[e][m] = this.calls[e][m] || {};
    this.calls[e][m][n] = f;
    return this;
  };

  IN.trigger = function(e, onoff) {
    this.calls = this.calls || {};
    if (!e in this.calls) {
      return;
    }
    var args = [].slice.call(arguments, 2)
    for(var m in this.calls[e]) {
      for(var n in this.calls[e][m]) {
        var f = this.calls[e][m][n];
        try { (onoff)?f.bind.apply(args):f.unbind.apply(args); } catch(e1){} // console.log(e1); continue next on error
      }
    }
    return this;
  };

  IN.off = function(e, m, n) {
    var l = arguments.length;
    if (l == 3) {
      try { delete this.calls[e][m][n]; } catch(e1){}
    }
    if (l == 2) {
      try { delete this.calls[e][m]; } catch(e1){}
    }
    if (l == 1) {
      try { delete this.calls[e]; } catch(e1){}
    }
    if (l == 0) {
      this.calls = {};
    }
    return this;
  };

  IN.redirect = function(path, ajax_redirect) {
    if (window.history && ajax_redirect) { // ajax navigate
      IN.ajaxNavigate(path);
    } else {
      window.location = path;
    }
  };

  IN.runScript = function(scripts) {
    if (typeof scripts === 'string') {
      scripts = [scripts]
    }
    for(var script in scripts) {
      if (typeof script === 'string') { // just run once
        eval(script);
        continue;
      }
      var tag = document.createElement('script'); tag.type = 'text/javascript';
      if ('src' in script) { // file
        tag.src = script.path;
      } else if ('text' in script) { // inline
        tag.text = script.text;
      }
      document.body.appendChild(tag);
    }
  };

  IN.addStyle = function(styles) {
    if (typeof styles === 'string') {
      styles = [styles]
    }
    var head = document.getElementsByTagName('head')[0];
    for(var css in styles) {
      if (typeof css === 'string') { // inline
        var tag = document.createElement('style');
        tag.type = 'text/css';
        if (tag.styleSheet) {
          tag.styleSheet.cssText = css;
        } else {
          tag.appendChild(document.createTextNode(css));
        }
      }
      if ('href' in css) { // file
        var tag  = document.createElement('link');
        tag.rel  = css.rel?css.rel:'stylesheet';
        tag.type = css.rel?css.rel:'text/css';
        tag.href = css.href;
        tag.media = css.media?css.media:'all';
      }
      head.appendChild(tag);
    }
  };

	IN.setTitle = function(title) {
	  document.title = title;
	}

  /**
   * Ajax object.
   *
   * Thanks to Drupal7 Ajax
   *
   */
  IN.ajax = {};

  /**
   * Extends Error to provide handling for Errors in AJAX
   */
  IN.AjaxError = function (xmlhttp, uri) {

    var statusCode, statusText, pathText, responseText, readyStateText;
    if (xmlhttp.status) {
      statusCode = "\n" + "An AJAX HTTP error occurred." + "\n" + "HTTP Result Code: " + xmlhttp.status;

      if (xmlhttp.status == 413) {
        UIkit.notify({
            message : 'Error! Request is too large!',
            status  : 'danger',
            timeout : 5000,
            pos     : 'bottom-left'
        });
      } else if (xmlhttp.status == 503) {
        UIkit.notify({
            message : 'Error! Internal server error! Please try again later!',
            status  : 'danger',
            timeout : 5000,
            pos     : 'bottom-left'
        });
      }
    } else {
      statusCode = "\n" + "An AJAX HTTP request terminated abnormally.";
    }
    statusCode += "\n" + "Debugging information follows.";
    pathText = "\n" + "Path: " + uri;
    statusText = '';
    // In some cases, when statusCode === 0, xmlhttp.statusText may not be defined.
    // Unfortunately, testing for it with typeof, etc, doesn't seem to catch that
    // and the test causes an exception. So we need to catch the exception here.
    try {
      statusText = "\n" + "StatusText: " + $.trim(xmlhttp.statusText);
    } catch (e) {}

    responseText = '';
    // Again, we don't have a way to know for sure whether accessing
    // xmlhttp.responseText is going to throw an exception. So we'll catch it.
    try {
      responseText = "\n" + "ResponseText: " + $.trim(xmlhttp.responseText);
    } catch (e) {}

    // Make the responseText more readable by stripping HTML tags and newlines.
    responseText = responseText.replace(/<("[^"]*"|'[^']*'|[^'">])*>/gi, "");
    responseText = responseText.replace(/[\n]+\s+/g, "\n");

    // We don't need readyState except for status == 0.
    readyStateText = xmlhttp.status === 0 ? ("\n" + "ReadyState: " + xmlhttp.readyState) : "";

    this.message = statusCode + pathText + statusText + responseText + readyStateText;
    this.name = 'AjaxError';
  };

  IN.AjaxError.prototype = new Error();
  IN.AjaxError.prototype.constructor = IN.AjaxError;

  /**
   * Ajax object.
   *
   */
  IN.ajax = function (base, element, ajax_options) {

    this.commands = new IN.AjaxCommands();

    var defaults = {
      event: 'click', //'click', //mousedown
      form: null,
      keypress: true,
      setClick : true,
      selector: '#' + base,
      effect: 'none',
      speed: 'none',
      method: 'replaceWith',
      progress: {
        type: 'throbber',
        message: ''
      },
      submit: {
        'ajax': 1
      },
      type : 'POST',
      modal : false
    };

    //if (element.form) { // use the form instead of submit button
        //element = element.form;
    //}

    var $el = $(element);
	var n = $(element).attr('name');
	var i = $(element).attr('id');

    if (!ajax_options.event) {
        var ajax_event = $el.data('ajax_event');
        if (ajax_event) {
            ajax_options['event'] = ajax_event;
        } else {
            if ($el.is('form')) {
                ajax_options['event'] = 'submit';
            } else if ($el.is('select') ||
				$el.is(':file') ||
				$el.is(':checkbox') ||
				$el.is(':radio')) {
					ajax_options['event'] = 'change';
            }
            // use default
        }
    }

    // partial submit, rendering
    var partial = $el.data('ajax_partial');
    if (partial) {
        ajax_options['partial'] = 1;
    }



    $.extend(this, defaults, ajax_options);

    this.element = element;
    this.ajax_options = ajax_options;

    // get the ajax url
    if (!this.url) {
      if ($(element).is('a')) {
        this.url = $(element).attr('href');
        if (!ajax_options.type || ajax_options.type == 'GET') { // normal a navigation
            this.navigation = true;
            this.type = 'GET';
            //$('body').scrollTop(0);
        }
      } else if ($(element).is('form')) {
        this.url = $(element).attr('action');
      }
      if (!this.url) {
        this.url = $(element).data('href'); // use data-href
        if (!this.url) {
          this.url = window.location.href; // use current url
        }
      }
    }

    if (this.type == 'GET') {
      if ($el.hasClass('no-scroll')) {
        this.no_scroll = true;
	  }
    }

    // it is ajax request # XMLHttpRequest will be added by jquery
    //this.url = this.url + ((this.url.indexOf('?') == -1)? '?' : '&') + 'ajax=1';

    // Set the options for the ajaxSubmit function.
    // The 'this' variable will not persist inside of the options object.
    var ajax = this;
    ajax.options = {
      url: ajax.url,
      data: ajax.submit,
      beforeSerialize: function (ajax_options, options) {
        return ajax.beforeSerialize(ajax_options, options);
      },
      beforeSubmit: function (form_values, ajax_options, options) {
        ajax.ajaxing = true;
        return ajax.beforeSubmit(form_values, ajax_options, options);
      },
      beforeSend: function (xmlhttprequest, options) {
        ajax.ajaxing = true;
        return ajax.beforeSend(xmlhttprequest, options);
      },
      success: function (response, status) {
        // iFrame uploads returns string
        if (typeof response === 'string') {
          response = $.parseJSON(response);
        }
        return ajax.success(response, status);
      },
      complete: function (response, status) {
        ajax.ajaxing = false;
        if (status === 'error' || status === 'parsererror') {
          return ajax.error(response, ajax.url);
        }
      },
      dataType: 'json',
      accepts: {
        json: ajax_options.accepts || 'application/vnd.ajax'
      },
      type: ajax.type
    };

    if (ajax_options.dialog) {
      ajax.options.data.dialogOptions = ajax_options.dialog;
    }

    // bind it
    $(ajax.element).on(ajax.event, function (event) {
	  return ajax.eventResponse(this, event);
    });

    // If necessary, enable keyboard submission so that Ajax behaviors
    // can be triggered through keyboard input as well as e.g. a mousedown
    // action.
    if (ajax_options.keypress) {
      $(ajax.element).on('keypress', function (event) {
        return ajax.keypressResponse(this, event);
      });
    }

    // If necessary, prevent the browser default action of an additional event.
    // For example, prevent the browser default action of a click, even if the
    // AJAX behavior binds to mousedown.
    if (ajax_options.prevent) {
      $(ajax.element).on(ajax_options.prevent, false);
    }
  };

  /**
   * Handle a key press.
   *
   * The Ajax object will, if instructed, bind to a key press response. This
   * will test to see if the key press is valid to trigger this event and
   * if it is, trigger it for us and prevent other keypresses from triggering.
   * In this case we're handling RETURN and SPACEBAR keypresses (event codes 13
   * and 32. RETURN is often used to submit a form when in a textfield, and
   * SPACE is often used to activate an element without submitting.
   */
  IN.ajax.prototype.keypressResponse = function (element, event) {
    // Create a synonym for this to reduce code confusion.
    var ajax = this;

    // Detect enter key and space bar and allow the standard response for them,
    // except for form elements of type 'text', 'tel', 'number' and 'textarea',
    // where the spacebar activation causes inappropriate activation if
    // #ajax['keypress'] is TRUE. On a text-type widget a space should always be a
    // space.
    if (event.which === 13 || (event.which === 32 && element.type !== 'text' &&
      element.type !== 'textarea' && element.type !== 'tel' && element.type !== 'number')) {
      event.preventDefault();
      event.stopPropagation();
      $(ajax.ajax_options.element).trigger(ajax.ajax_options.event);
    }
  };

  /**
   * Handle an event that triggers an Ajax response.
   *
   * When an event that triggers an Ajax response happens, this method will
   * perform the actual Ajax call. It is bound to the event using
   * bind() in the constructor, and it uses the options specified on the
   * ajax object.
   */
  IN.ajax.prototype.eventResponse = function (element, event) {
    event.preventDefault(); event.stopPropagation();

    var ajax = this;

    // wait for the previous request to complete
    if (ajax.ajaxing) {
      return false;
    }

    try {
      ajax.clicked = element;

      if ($(ajax.element).is('form')) {
        $(ajax.element).ajaxSubmit(ajax.options);
      } else if (ajax.form) {
        $(ajax.form).ajaxSubmit(ajax.options);
      } else {
        ajax.beforeSerialize(ajax.element, ajax.options);
        $.ajax(ajax.options);
      }
    } catch (e) {
      ajax.ajaxing = false;
      UIkit.notify({
    		message : 'Error! ' + e.message,
    		status  : 'danger',
    		timeout : 5000,
    		pos     : 'bottom-left'
      });
    }

    if (ajax.type == 'GET' && !ajax.no_scroll) {
  	  // TODO: not for all gets
  	  scrollTo(0, 0);
  	}

    return false;
  };

  /**
   * Handler for the form serialization.
   *
   * Runs before the beforeSend() handler (see below), and unlike that one, runs
   * before field data is collected.
   */
  IN.ajax.prototype.beforeSerialize = function (element, options) {

    if (this.element_id) {
        options.data.element_id = this.element_id;
    }
    if (this.lazy) {
        options.data.lazy_load = this.lazy;
    }
    if (this.ajax_args) {
        options.data.ajax_args = this.ajax_args;
    }
    var value = $(this.element).attr('value')
    var id = $(this.element).attr('id')
    if (id && value && !(id in options.data)) {
        //options.data[id] = value; // v: checkbox value appears twice
    }

    if (this.clicked) {
        var clicked = this.clicked;
        var value = $(clicked).attr('value')
        var name = $(clicked).attr('name')
        if (name && value && !(name in options.data)) {
            //options.data[name] = value; // v: checkbox value appears twice
        }
    }

    // mark it is in modal
    if (this.modal) {
        options.data['modal'] = 1;
    }

    // partial
    if (this.partial) {
        options.data['partial'] = this.partial;
    }

  };

  /**
   * Modify form values prior to form submission.
   */
  IN.ajax.prototype.beforeSubmit = function (form_values, element, options) {
    // This function is left empty to make it simple to override for modules
    // that wish to add functionality here.
  };

  /**
   * Prepare the Ajax request before it is sent.
   */
  IN.ajax.prototype.beforeSend = function (xmlhttprequest, options) {
    // For forms without file inputs, the jQuery Form plugin serializes the form
    // values, and then calls jQuery's $.ajax() function, which invokes this
    // handler. In this circumstance, options.extraData is never used. For forms
    // with file inputs, the jQuery Form plugin uses the browser's normal form
    // submission mechanism, but captures the response in a hidden IFRAME. In this
    // circumstance, it calls this handler first, and then appends hidden fields
    // to the form to submit the values in options.extraData. There is no simple
    // way to know which submission mechanism will be used, so we add to extraData
    // regardless, and allow it to be ignored in the former case.
    if ($(this.element).is('form')) {
      options.extraData = options.extraData || {};

      // Let the server know when the IFRAME submission mechanism is used. The
      // server can use this information to wrap the JSON response in a TEXTAREA,
      // as per http://jquery.malsup.com/form/#file-upload.
      options.extraData.ajax_iframe_upload = '1';

      // The triggering element is about to be disabled (see below), but if it
      // contains a value (e.g., a checkbox, textfield, select, etc.), ensure that
      // value is included in the submission. As per above, submissions that use
      // $.ajax() are already serialized prior to the element being disabled, so
      // this is only needed for IFRAME submissions.

      var v = $.fieldValue(this.element);
      if (v !== null) {
        options.extraData[this.element.name] = v;
      }
    }

    // Disable the element that received the change to prevent user interface
    // interaction while the Ajax request is in progress. ajax.ajaxing prevents
    // the element from triggering a new request, but does not prevent the nabar
    // from changing its value.
    $(this.element).prop('disabled', true);

    // Insert progressbar or throbber.
    if (this.progress.type === 'bar') {
      var progressBar = new IN.ProgressBar('ajax-progress-' + this.element.id, $.noop, this.progress.method, $.noop);
      if (this.progress.message) {
        progressBar.setProgress(-1, this.progress.message);
      }
      if (this.progress.url) {
        progressBar.startMonitoring(this.progress.url, this.progress.interval || 1500);
      }
      this.progress.element = $(progressBar.element).addClass('ajax-progress ajax-progress-bar');
      this.progress.object = progressBar;
      $(this.element).after(this.progress.element);
    }
    else if (this.progress.type === 'throbber') {
        this.progress.element = $('<div class="ajax-progress ajax-progress-throbber"></div>');

      if ($(this.element).is('a')) {
        if ($(this.element).find('img').length == 0) {
          $(this.element).append(this.progress.element);
        }
      } else {
        $(this.element).after(this.progress.element);
      }
    }
    else if (this.progress.type === 'fullscreen') {
      this.progress.element = $('<div class="ajax-progress ajax-progress-fullscreen">&nbsp;</div>');
      $('body').after(this.progress.element);
    }
  };

  /**
   * Handler for the form redirection completion.
   */
  IN.ajax.prototype.success = function (response, status) {

    // Remove the progress element.
    if (this.progress.element) {
      $(this.progress.element).remove();
    }
    if (this.progress.object) {
      this.progress.object.stopMonitoring();
    }
    $(this.element).prop('disabled', false);

    for (var i in response) {
      if (response.hasOwnProperty(i)) {
          var value = response[i];
          if (i == 'redirect') {
              IN.redirect(value, true);
          }
          if (i == 'script') { IN.runScript(value); }
          if (i == 'style') { IN.addStyle(value); }
          if (i == 'title') { IN.setTitle(value); }

          if (i == 'commands') {
			  for(var c in value) {
				  if (value[c].method in this.commands) {
					try {
					  this.commands[value[c].method].apply(this, value[c].args);
					} catch (e) {} // console.log(e);
                  }
              }
          }
      }
    }

    this.ajaxing = false;

    // dom may changed
    IN.trigger('dom', true);
    UIkit.init();

    // change url
    if(window.history && this.type == 'GET' && this.url != window.location.pathname) {
        window.history.pushState({path:this.url},'', this.url);
    }
    //this.ajax_options = null;

  };

  /**
   * Handler for the form redirection error.
   */
  IN.ajax.prototype.error = function (response, uri) {
    // Remove the progress element.
    if (this.progress.element) {
      //$(this.progress.element).remove();
    }
    if (this.progress.object) {
      this.progress.object.stopMonitoring();
    }
    // Undo hide.
    $(this.wrapper).show();
    // Re-enable the element.
    $(this.element).prop('disabled', false);

    //IN.trigger('dom', true);
    this.ajaxing = false;
    throw new IN.AjaxError(response, uri);
  };

    IN.AjaxCommands = function () {};
    IN.AjaxCommands.prototype = {

        replace: function (element, value) {
          $(value).hide().trigger('remove');
          $(element).replaceWith(value);
          $(value).fadeIn('slow');
          //$(value).slideDown('slow');
          //$(element).replaceWith(value);
        },
        html: function (element, value) {
    		  $(element).children().trigger('remove');
    		  $(element).empty();
    		  $(value)
      			.hide()
      			.appendTo($(element))
      			.fadeIn('slow'); // slideDown('slow');
        },
        append: function (element, value) {
          value = $(value).hide();
          $(element).append(value);
          value.fadeIn();
          //value.slideDown();
        },
        prepend: function (element, value) {
          value = $(value).hide();
          $(element).prepend(value);
          value.fadeIn();
          //value.slideDown();
        },
        remove: function (element) {
		      $(element).slideUp('slow').trigger('remove').remove();
        },
        notify: function (options) {
            UIkit.notify(options);
        },
        closeAjaxModal: function () {
            var id = 'i-ajax-modal';
            var modal = UIkit.modal('#' + id);
            modal.hide();
        },
        focus: function (element) {
          $(element).focus();
        },
        /**
         * todo: alert in dialog
         */
        alert: function (message, title) {
          window.alert(message, title);
        },

        /**
         * calls the In redirect
         */
        redirect: function (path, ajax_redirect) {
          IN.redirect(path, ajax_redirect);
        },

        /**
         * Command to set the options that will be used for other commands in this response.
         */
        config: function (config) {
          $.extend(true, IN.config, config);
        },

        title : function (title) {
          document.title = title;
        }
    };

    IN.lazy_load = function(lazy, delay) {
        if (delay) {
          setTimeout(function () { IN.lazy_load(lazy, 0); }, delay);
          return;
        }
        var id = 'i-ajax-lazi-load-trigger';
        var $a = $('<a id="'+id+'"></a>');
        IN.ajax[id] = new IN.ajax(id, $a[0], {element_id : id, event : 'click', lazy : lazy, url : window.location.pathname});
        $a.click(); // trigger
    };

    IN.lazy_reload = function(id) {
      var lazys = {};
      var added = 0
      $(id).each(function() {
        var $el = $(this);
        lazys[added] = {
          args : $el.data('args')
        };
        added++;
      });
      if (added != 0) {
        IN.lazy_load(lazys);
      }
    };

    IN.historyPopState = function() {
        var url = window.location.pathname;
        IN.ajaxNavigate(url);
    };

    IN.ajaxNavigate = function(url) {
        var id = 'i-ajax-navigator-trigger';
        var $a = $('<a id="'+id+'" href="'+url+'"></a>');
        IN.ajax[id] = new IN.ajax(id, $a[0], {element_id : id, event : 'click', url : url, type : 'GET'});
        $a.click(); // trigger
    };

    IN.playSound = function(url) {
      IN.audioElement.setAttribute('src', url);
      IN.audioElement.load();
      IN.audioElement.addEventListener("canplay", function() {
        IN.audioElement.play();
      });
    }

    // only once


    IN.on('dom', 'In.ajax', 'a-ajax', {
        bind : function() {

            if (window.history) { // only if html5
                $('a').once('ajax', function(){
                    var href = $(this).attr('href');
                    if (href
                        && href.substr(0, 1) == '/'
                        && href.substr(0, 2) != '//'
                        && (!$(this).attr('target'))
                        && (!$(this).hasClass('no-ajax'))
                        && (!$(this).hasClass('ajax-modal'))) {
                        var id = $(this).attr('id');
                        var options = {element_id : id};
                        var ajax_args = $(this).data('ajax_args');
                        if (ajax_args) {
                            options['ajax_args'] = ajax_args;
                        }
                        var ajax_type = $(this).data('ajax_type');
                        if (ajax_type) {
                            options['type'] = ajax_type;
                        }
                        IN.ajax[id] = new IN.ajax(id, this, options);
                    }
                });
            }
            $('form.ajax input[type="submit"]').once('ajax', function(){
                var id = $(this).attr('id');
                var form = $(this).closest('form');
                if (form) {
                    var options = {element_id : id, form :  form};
                    var ajax_args = $(this).data('ajax_args');
                    if (ajax_args) {
                        options['ajax_args'] = ajax_args;
                    }
                    IN.ajax[id] = new IN.ajax(id, this, options);
                }
            });
            $('form.ajax button[type="submit"]').once('ajax', function(){
                var id = $(this).attr('id');
                var form = $(this).closest('form');
                if (form) {
                    var options = {element_id : id, form :  form};
                    var ajax_args = $(this).data('ajax_args');
                    if (ajax_args) {
                        options['ajax_args'] = ajax_args;
                    }
                    IN.ajax[id] = new IN.ajax(id, this, options);
                }
            });
            $('form.ajax').once('ajax', function(){
                var id = $(this).attr('id');
                var options = {element_id : id, event : 'submit'};
                IN.ajax[id] = new IN.ajax(id, this, options);
            });
            $('.ajax').once('ajax', function(){
                var id = $(this).attr('id');
                var form = $(this).closest('form');
                if (form.length) { // if form
                    var options = {element_id : id, form :  form};
                    var ajax_args = $(this).data('ajax_args');
                    if (ajax_args) {
                        options['ajax_args'] = ajax_args;
                    }
                    IN.ajax[id] = new IN.ajax(id, this, options);
                } else {
                    var options = {element_id : id, 'ajax_args' : {}};
                    var ajax_args = $(this).data('ajax_args');
                    if (ajax_args) {
                        options['ajax_args'] = ajax_args;
                    }
                    IN.ajax[id] = new IN.ajax(id, this, options);
                }
            });
            var lazys = {};
            var added = 0;
            $('.ajax-lazy').once('ajax-lazy', function(){
                var $el = $(this);
                lazys[added] = {
                    args : $el.data('args')
                };
                added++;
            });
            if (added) {
                IN.lazy_load(lazys, 2000); // TODO: dynamic delay
            }


            $('.ajax-modal').once('ajax-modal', function(){
                var $el = $(this);
                $el.click(function(event){
                    event.preventDefault(); event.stopPropagation();

                    var id = 'i-ajax-modal';
                    $('#' + id).remove(); // delete old modal, content not updating
                    $('<div id="'+id+'" class="i-modal"><div class="i-modal-dialog"><a class="i-modal-close i-close"></a><div class="modal-content i-modal-spinner"></div></div></div>').appendTo('body');
                    var trigger = 'i-ajax-modal-trigger';
                    var $a = $('<a id="'+trigger+'"></a>');
                    var url = $el.attr('href'); if (!url) { url = $el.data('href'); } if (!url) { url = $el.data('url'); }
                    IN.ajax[trigger] = new IN.ajax(trigger, $a[0], {element_id : trigger, event : 'click', url : url, 'type' : 'POST', modal : true});
                    var modal = UIkit.modal('#' + id);
                    modal.show();
                    $a.click(); // ajax load trigger
                });
            });

            require(['selectize'], function(selectize) {
                $('.autocomplete').once('autocomplete', function(){
                    var $el = $(this);

                    $el.selectize({
                        theme: 'links',
                        //plugins: ['restore_on_backspace'],
                        delimiter: ',',
                        maxItems: $el.data('autocomplete_max_items'),
                        valueField: 'id',
                        searchField: 'text',
                        hideSelected: true,
                        options: $el.data('autocomplete_options'),
                        create: $el.data('autocomplete_create'),
                        render: {
                          option: function(item, escape) {
                            return '<div data-value="'+item.id+'">' + item.text + '</div>';
                          },
                          item: function(item, escape) {
                            return '<div data-value="'+item.id+'">' + (item.item?item.item:item.text) + '</div>';
                          },
                        },
                        load: function(query, callback) {
                          if (!query.length) {
                            return callback();
                          }
                          $.ajax({
                              url: $el.data('autocomplete_url') + '/!' + encodeURIComponent(query),
                              type: 'GET',
                              data : $el.data('autocomplete_url_data'),
                              error: function() {
                                callback();
                              },
                              success: function(data) {
                                callback(data);
                              }
                          });
                        }
                      });
                });
            });

            $('.auto-scrollspy-click').once('auto-scrollspy-click', function() {
              var $el = $(this);

              $el.on('inview.uk.scrollspy', function() {
                $el.find('a').click();
              });
            });

        },
        unbind : function() {}
    });


	/*UIkit.ready(function() {
	   //recursive
	});*/
	$(document).ready(function() {
      IN.trigger('dom', true);
      if (window.history) { // html5 only ajax
        $(window).bind('popstate', IN.historyPopState);
      }
      $(window).bind('focus', function() {IN.window_in_focus = true;});
      $(window).bind('blur', function() {IN.window_in_focus = false;});
    });


})(jQuery);

return window.IN;

});
