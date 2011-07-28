<!DOCTYPE html>
<html lang="en">
    <head>
        <meta charset="utf-8" />
        
        <title>Login: WebTranslator for Autostore v2.2</title>
<%include file="css_files.mak"/>
    </head>
    
    <body>
<%include file="header.mak"/>
        <div id="subheader">
            <p>
                Login:
            </p>
        </div>
        <div id="content">
            % if len(request.session.peek_flash()) > 0:
            <div id="error" class="error flashmessage">
                <p>${request.session.pop_flash()[0]}</p>
            </div>
            % endif
            <form action="." method="post">
                <input type="hidden" name="login.submitted" value="True"/>
                <div class="row">
                    <label for="username">Username: </label>
                    <input type="text" name="username" id="username" value="${username}"/>
                </div>
                <div class="row">
                    <label for="password">Password</label>
                    <input type="password" name="password" id="password" value=""/>
                </div>
                <input type="submit" value="Login"/>
            </form>
        </div>
<%include file="footer.mak"/>
    </body>
</html>