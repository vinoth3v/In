CREATE <%= theme_output['create_type'] %/> <%= theme_output['table'] %/>
(
<%= theme_output['fields'] %/>
<% if theme_output['keys']: >
,
<%= theme_output['keys'] %/></% > 
)
<%= theme_output['tbl_options'] %/>