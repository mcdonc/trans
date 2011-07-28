<!DOCTYPE html>
<html lang="en">
    <head>
        <%!
            #from pyramid.url import resource_url
            from pyramid.url import static_url
            
            def cleanid(text):
                return text.replace(' ', '_').replace('(', '_').replace(')', '_')
        %>
        <%
            jquery_js = static_url('trans:static/js/jquery-1.6.min.js', request)
            general_js = static_url('trans:static/js/general.js', request)
        %>
        
        <meta charset="utf-8" />
        
        <title>WebTranslator for Autostore v2.2</title>
        
<%include file="css_files.mak"/>
        
        <script type="text/javascript" language="javascript" src="${jquery_js}"></script>
        <script type="text/javascript" language="javascript" src="${general_js}"></script>
    </head>
    
    <body>
<%include file="header.mak"/>
        <div id="subheader">
            <h3>Editing language "${_context.contain['lang_code']}"</h3>
        </div>
        <div id="breadcrumbs">
            <a href="/">&lt;&lt; Back to overview</a>
        </div>
        <div id="content">
            <form action="" method="post">
                <input type="hidden" name="form.submitted" value=""/>
                
                % if len(request.session.peek_flash()) > 0:
                <span class="flashmessage">
                    ${request.session.pop_flash()[0]}
                </span>
                % endif
                
                <div class="row">
                    <input type="submit" value="Save"/>
                </div>
                % for key,value in _context.map.items():
                <%
                    if value == None:
                        value = ''
                %>
                <div class="row">
                    <label for="${key|cleanid}">${key}</label>
                    <input class="toupdate" type="text" name="${key}" id="${key|cleanid}" value="${value}"/>
                    <span class="updatestatus"></span>
                </div>
                % endfor
                <div class="row">
                    <input type="submit" value="Save"/>
                </div>
            </form>
            % if saved:
            <div id="saved">Language saved correctly</div>
            % endif
        </div>
<%include file="footer.mak"/>
    </body>
</html>