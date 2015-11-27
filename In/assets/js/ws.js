
define('In_ws', ['In'], function() {
	"use strict";

(function ($) {

	IN.socket_heart_beat_pointer = null;
	IN.socket_connect_retry_interval = null;

	IN.Socket = function() {
		this.socket = null;
		this.isopen = false;
	};


	if (!('WebSocket' in window)) {
  	UIkit.notify({
			message : 'This browser is very old, Some of the site features will not work in this browser!',
			status  : 'danger',
			timeout : 30000,
			pos     : 'bottom-left'
	  });
  }

  IN.WSCommands = function () {};
	IN.WSCommands.prototype = {};

	IN.Socket.prototype.init = function(url) {
		this.socket_url = url;
		IN.socket_connect_url = url; // retry
		this.commands = new IN.WSCommands();

		try {
			this.socket = new WebSocket(url);
		} catch(e1) {
			return;
		}

		var sock = this.socket;
		sock.binaryType = "arraybuffer";

		var ws = this;

		// on open
		sock.onopen = function() {
		   IN.WS.isopen = true;
		   IN.WS.socket.setMaxIdleTime = 9000;

		   clearInterval(IN.socket_connect_retry_interval);

		   var msg = {
				'ws_action' : 'me'
		   };
		   ws.send(msg);


		  clearInterval(IN.socket_heart_beat_pointer);
		  IN.socket_heart_beat_pointer = setInterval(function(){
				IN.WS.send({'ws_action' : 'me'}); // update me
      }, 1000 * 50);

		  setTimeout(function() {
		    IN.trigger('In.ws.onopen', true);
		  }, 1000);

		}

		sock.onmessage = function(e) {
		   if (typeof e.data == "string") {

			  var message = JSON.parse(e.data);
			  if ('ws_command' in message) {
				  var command = message['ws_command'];
				  if (command in IN.WS.commands) {
					//IN.WS.commands[command].apply(this, message, message);
					IN.WS.commands[command](message);
				  }
			  }
		   }
		}

		sock.onclose = function(e) {
		   
		   IN.WS.socket = null;
		   IN.WS.isopen = false;

		   // retry

		   clearInterval(IN.socket_connect_retry_interval);
		   IN.socket_connect_retry_interval = setInterval(function(){
				IN.WS.init(IN.socket_connect_url);
		   }, 1000 * 10);

		}

	}

	IN.Socket.prototype.send = function(message) {
	  if (!this.socket) {
	    this.init(this.socket_url);
	  }
	  if (this.socket) {
	    message = JSON.stringify(message);
	    this.socket.send(message);
	  }
	}

	IN.WSCommands.prototype.me = function(message) {
	  IN.nabar = message.nabar;
	}
	IN.WS = new IN.Socket();

	IN.WSCommands.prototype.ajax_command = function(message) {
      var command = message.command;
      var commands = new IN.AjaxCommands();
      if (command in commands) {
	    	commands[command].apply(commands, message.args);
	  	}
    };

})(jQuery);

	return IN.Socket;

});
