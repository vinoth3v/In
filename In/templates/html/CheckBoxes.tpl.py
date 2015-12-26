<div <%= attributes %>>
<py if _['title']: >
<label for="<%= id %>"><%= title %> </label>
</py>
<%= children %><div class="info field-info i-text-muted"><%= info %></div><%= error_message %></div>