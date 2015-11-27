<article <%= attributes %>>
	<div class="i-clearfix">
		<%= nabar_picture %>
		<div class="i-nbfc">
			<div>
				<div class="i-text-muted"><a href="/nabar/<%str= nabar_id %>"><%= nabar_name %></a> 	<time pubdate><%= created %></time></div>
				<div id="comment-<%str= id %>-children"><%= children %></div>
				<footer class="i-margin-small i-clearfix"><%= entity_context_links %></footer>
				<%= sub_comment_list %>
				<div id="Comment_<%str= id %>-ajax-comment-form"></div>
			</div>
		</div>
	</div>
</article>
