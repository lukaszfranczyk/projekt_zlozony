'use strict';

$(document).ready(function() {
    LOGIN.run();
    if(location.pathname != '/auth/login')
        CHAT.run();
});