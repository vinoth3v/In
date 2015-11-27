DELETE FROM <%= theme_output['tables'] %/>
<%= theme_output['joins'] %/>
<% if theme_output['condition']: >
WHERE 
<%= theme_output['condition'] %/></% >
<% if theme_output['groupby']: >
GROUP BY 
<%= theme_output['groupby'] %/></% >
<% if theme_output['having']: >
HAVING 
<%= theme_output['having'] %/></% >
<% if theme_output['orderby']: >
ORDER BY 
<%= theme_output['orderby'] %/></% >
<% if theme_output['limit']: >
LIMIT <%= theme_output['limit'] %/></% >