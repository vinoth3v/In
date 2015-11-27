UPDATE <%= itm.sql['tables'] %/>
<%= itm.sql['set_values'] %/>
<%= itm.sql['join'] %/>
<% if itm.has_condition(): >
WHERE
<%= itm.sql['condition'] %/>
</% >