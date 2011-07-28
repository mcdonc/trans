<%
    from pyramid.url import static_url
    general_css = static_url('trans:static/css/general.css', request)
%>
<link rel="stylesheet" href="${general_css}" type="text/css" />