/**
 * Created by Dasate on 2017/9/14.
 * QQ361899429
 */
var simpleAlert = function (opts) {
    //设置默认参数
    var opt = {
        "closeAll": false,
        "content": "",
        "buttons": {},
    };
    //合并参数
    var option = $.extend(opt, opts);
    //事件
    var dialog = {};
    var $simpleAlert = $('<div class="simpleAlert">');
    var $shelter = $('<div class="simpleAlertShelter">');
    var $simpleAlertBody = $('<div class="simpleAlertBody">');
    //var $simpleAlertBodyClose = $('<img class="simpleAlertBodyClose" src="img/close.png" height="14" width="14"/>');
    var $simpleAlertBodyContent_ = $('<p class="simpleAlertBodyContent onlyOne" style="color: #1ab394">' + option.content + '</p>');
    var $simpleAlertBodyContent = $('<img  src="/static/img/loading.gif"/>');
    //var $simpleAlertBodyContent = $('<div class="panel-body onlyOne"><div class="progress "><div id="task_progress" style="width: 0%;color: red" class="progress-bar progress-bar-info" >0%</div></div></div>');
    dialog.init = function () {
        //.append($simpleAlertBodyClose)
        //$simpleAlertBodyContent.children().css('width',opt.width+'%').html(opt.width+"%");
        $simpleAlertBody.append($simpleAlertBodyContent_).append($simpleAlertBodyContent);
        var num = 0;
        var only = false;
        var onlyArr = [];
        for (var i = 0; i < 2; i++) {
            for (var key in option.buttons) {
                switch (i) {
                    case 0:
                        onlyArr.push(key);
                        break;
                    case 1:
                        if (onlyArr.length <= 1) {
                            only = true;
                        } else {
                            only = false;
                        }
                        num++;
                        var $btn = $('<button class="simpleAlertBtn simpleAlertBtn' + num + '">' + key + '</button>');
                        $btn.bind("click", option.buttons[key]);
                        if (only) {
                            $btn.addClass("onlyOne")
                        }
                        //$simpleAlertBody.append($btn);
                        break;
                }

            }
        }
        $simpleAlert.append($shelter).append($simpleAlertBody);
        $("body").append($simpleAlert);
        $simpleAlertBody.show().animate({"marginTop":"-128px","opacity":"1"},300);
    }
    //右上角关闭按键事件
    // $simpleAlertBodyClose.bind("click", function () {
    //     option.closeAll=false;
    //     dialog.close();
    // })
    dialog.close = function () {
        if(option.closeAll){
            $(".simpleAlert").remove()
        }else {
            $simpleAlertBody.animate({"marginTop": "-188px", "opacity": "0"}, 200, function () {
                $(".simpleAlert").last().remove()
            });
        }
    };
    dialog.init();
    return dialog;
};