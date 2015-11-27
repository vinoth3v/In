Hi, <%= to_name %><br>
<br>
Thank you for registering into our site <%= app_name %>.<br>To complete registration please click the following link.<br>
<a href="<%= app_url %>/token/verify/!register/!<%str= mail_verify_token %>">Click here to complete registration!</a><br>
<%= value %><br>
<%= body_html %><br>
<%= children %><br>
<br>
<hr>
Thank you,<br>
<b><%= app_title %></b>