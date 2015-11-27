UPDATE <%= itm.sql['tables'] %/>
SET <%= itm.sql['fields'] %/>
<% if itm.sql['condition']: >
WHERE 
<%= itm.sql['condition'] %/></% >
<% if itm.sql['orderby']: >
ORDER BY 
<%= itm.sql['orderby'] %/></% >
<% if itm.sql['limit']: >
LIMIT
<%= itm.sql['limit'] %/></% >