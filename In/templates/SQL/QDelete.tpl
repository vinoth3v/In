DELETE FROM <%= tbl %/> 
<% if itm.has_conditions(): >
WHERE
<%= itm.sql['conditions'] %/>
</% >