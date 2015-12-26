<article <%= attributes %>>
	<div class="i-clearfix">
		<%= nabar_picture %>
		<div class="i-nbfc">
			<div>
				<div class="i-text-muted"><a href="/nabar/<%str= nabar_id %>"><%= nabar_name %> <%= to_entity %> </a> 	<time pubdate><%= created %></time></div>
				<div id="status-<%str= id %>-children"><%= children %></div>
				<footer class="i-margin-small i-clearfix"><%= entity_context_links %></footer>
				<div class="ajax_boxes i-clearfix i-nbfc">
					<%= box_comments %>
					<%= box_comments_form %>
				</div>
			</div>
		</div>
	</div>
</article>
