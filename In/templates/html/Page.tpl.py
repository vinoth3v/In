<%= doctype %>
<html <%= html_attributes %>>
<head>
	<title><%= title %></title>
	<%= head_tags %>

	<%= header_css %>
	<%= header_js %>

</head>
<body <%= attributes %>>
	<div class='page' >
		<%= header %>
		<%= ajax_page_replaceable %>
		<div id="off-sidebar3" class="i-offcanvas"><%= sidebar3 %></div>
		<div id="off-sidebar4" class="i-offcanvas"><%= sidebar4 %></div>
		<%= footer %>
	</div>
	<div class="footer-assets">
	<%= footer_css %>
	<%= footer_js %>
	</div>
</body>
</html>
