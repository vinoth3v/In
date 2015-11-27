<fieldset <%= attributes %>>
<py if _['title']: >
<legend><%= title %></legend>
</py>
<%= value %> <%= children %></fieldset>
