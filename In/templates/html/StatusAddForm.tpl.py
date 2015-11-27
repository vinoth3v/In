<form <%= attributes %>><%= error_message %>
	<div class="i-clearfix">
		<%= nabar_picture %>
		<div class="i-nbfc">
			<div>		
				<input type="hidden" name="form_id" value="<%= form_id %>" /><input type="hidden" name="form_type" value="<%= form_type %>" /><input type="hidden" name="form_token" value="<%= form_token %>" />
				<%= children %>		
			</div>
		</div>
	</div>
</form>
