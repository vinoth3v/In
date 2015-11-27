UPDATE <%= theme_output['tables'] %/>
SET <%= theme_output['values'] %/>
<% if theme_output['condition']: >
WHERE 
<%= theme_output['condition'] %/></% >
<% if theme_output['orderby']: >
ORDER BY 
<%= theme_output['orderby'] %/></% >
<% if theme_output['limit']: >
LIMIT
<%= theme_output['limit'] %/></% >