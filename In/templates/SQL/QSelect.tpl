SELECT <%= itm.sql['field_option'] %/>
<%= itm.sql['fields'] %/>
FROM <%= itm.sql['tables'] %/>
<%= itm.sql['join'] %/>
<% if itm.sql['condition']: >
WHERE 
<%= itm.sql['condition'] %/>
</% >
<% if itm.sql['groupby']: >
GROUP BY 
<%= itm.sql['groupby'] %/>
</% >
<% if itm.sql['having']: >
HAVING 
<%= itm.sql['having'] %/>
</% >
<% if itm.sql['orderby']: >
ORDER BY 
<%= itm.sql['orderby'] %/>
</% >
<% if itm.sql['limit']: >
LIMIT 
<%= itm.sql['limit'] %/>
</% >