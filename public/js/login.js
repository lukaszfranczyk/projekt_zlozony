'use strict';

var LOGIN = LOGIN || {
    catchFormEvent: function($form) {
        var $buttons = $form.find("button");
        if ($buttons.length > 0) {
            $buttons.click(function(e) {
                var $requiredInput = $("input[required]"),
                    allowPost = true;
                $.each($requiredInput, function() {
                    if (!$(this).val()) {
                        $requiredInput.parent().show();
                        allowPost = false;
                        return;
                    }
                });
                if (allowPost) {
                    var $password = $form.find("input#password");
                    $password.val(md5($password.val()));
                    $form.attr("action", $(this).data("action"));
                    $form.submit();
                }
            });
        }
    },
    run: function() {
        if ($("form#login-signup").length > 0) {
            this.catchFormEvent($("form#login-signup"));
        }
    }
}