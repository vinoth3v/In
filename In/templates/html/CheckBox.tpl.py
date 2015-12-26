<py if _['title']: >
<label for="<%= id %>"><%= title %> </label>
</py>
<input <%= attributes %> />
<py if _['label']: >
<label for="<%= id %>"><%= label %></label>
</py>
<div class="info field-info i-text-muted"><%= info %></div><%= error_message %>