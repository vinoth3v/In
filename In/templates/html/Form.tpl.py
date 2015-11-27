<form <%= attributes %>>
<py if _['title']: >
	<h2 class="form-title"><%= title %></h2>
</py>
<py if _['info']: >
	<div class="info form-info i-text-muted"><%= info %></div>
</py>
	<%= error_message %>
	<input type="hidden" name="form_id" value="<%= form_id %>" /><input type="hidden" name="form_type" value="<%= form_type %>" /><input type="hidden" name="form_token" value="<%= form_token %>" />
	<%= children %>
</form>
