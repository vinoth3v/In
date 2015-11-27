Hi, <%= to_name %><br>
<br>
Someone asked to recover this account on <%= app_name %>.<br>If you want to recover this account, Please click the following link and set new password! Otherwise please ignore this e-mail.<br>
<a href="<%= app_url %>/token/verify/!recovery/!<%str= mail_verify_token %>">Click here to set new password!</a><br>
<%= value %><br>
<%= body_html %><br>
<%= children %><br>
<br>
<hr>
Thank you,<br>
<b><%= app_title %></b>
