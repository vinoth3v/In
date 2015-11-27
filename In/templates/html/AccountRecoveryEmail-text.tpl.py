Hi, <%= to_name %>

Someone asked to recover this account on <%= app_name %>.
If you want to recover this account, Please click the following link and set new password! Otherwise please ignore this e-mail.<br>

<%= app_url %>/token/verify/!recovery/!<%str= mail_verify_token %>

<%= value %> <%= body_text %>
<%= children %>

--
Thank you
<%= app_title %>
