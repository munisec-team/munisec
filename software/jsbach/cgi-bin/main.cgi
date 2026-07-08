#!/bin/bash

source /usr/local/JSBach/conf/variables.conf

/bin/cat << EOM

<!DOCTYPE html>
<html lang="ca" class="main-layout">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Administració de $HOSTNAME</title>
EOM
cat $DIR/$DIR_PROJECTE/$DIR_CGI/$CSS_CGI_BIN
/bin/cat << EOM
</head> 
<body>
    <div class="container">
        <iframe src="/cgi-bin/index-admin.cgi" name="menu-general" class="header"></iframe>
        <div class="main-content">
            <iframe src="/cgi-bin/model.cgi" name="menu" class="sidebar"></iframe>
            <iframe src="/cgi-bin/estat.cgi" name="body" class="body-content"></iframe>
        </div>
    </div>
</body>
</html>

EOM
