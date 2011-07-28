<%
    from pyramid.security import authenticated_userid
%>

<div id="header">
    <h1>WebTranslator for Autostore v2.2</h1>
    % if authenticated_userid(request) != None:
    <span><a href="/logout">Logout</a></span>
    % endif
</div>
