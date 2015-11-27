<article <%= attributes %>><%= value %>
	<header class="i-clearfix">
		<%= nabar_picture %>
		<div>
			<div><a href="/nabar/<%str= nabar_id %>"><%= nabar_name %></a> <%= featured %></div>
			<div class="i-text-muted"><%= created %></div>			
		</div>
	</header>
	<%= children %>
	<footer class="i-margin i-clearfix"><%= entity_context_links %></footer>
</article>