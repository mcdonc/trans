<!DOCTYPE html>
<html lang="en">
    <head>
        <meta charset="utf-8" />
        
        <title>WebTranslator for Autostore v2.2</title>
<%include file="css_files.mak"/>
    </head>
    
    <body>
<%include file="header.mak"/>
        <div id="createnew">
            <p>
                Create new language:
            </p>
            <form action="." method="post">
                <input type="hidden" name="form.submitted" value="True"/>
                <input type="text" name="lang" title="Language code"/>
                <input type="submit" value="Create"/>
            </form>
        </div>
        <div id="editavailable">
            % if langs == None:
            <p>No available languages to edit.</p>
            % else:
            <p>Edit one of the currently available items:</p>
            <ul>
                % for lang in langs:
                <%
                    from pyramid.url import resource_url
                    url = resource_url(_context, request, lang)
                %>
                <li><a href="${url}">${lang}</a></li>
                % endfor
            </ul>
            % endif
        </div>
<%include file="footer.mak"/>
    </body>
</html>