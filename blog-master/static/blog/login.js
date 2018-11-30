// // 登录页面的主要js代码
//
//
// // 点击注册按钮跳转
$("#register").click(function () {
        location.href="/reg/"
    });
//
//
//     var handlerPopup = function (captchaObj) {
//         // 成功的回调
//         captchaObj.onSuccess(function () {
//             var validate = captchaObj.getValidate();
//             $.ajax({
//                 url: "/pc-geetest/ajax_validate", // 进行二次验证
//                 type: "post",
//                 dataType: "json",
//                 data: {
//                     username: $('#username').val(),
//                     password: $('#password').val(),
//                     csrfmiddlewaretoken:$("[name='csrfmiddlewaretoken']").val(),
//                     geetest_challenge: validate.geetest_challenge,
//                     geetest_validate: validate.geetest_validate,
//                     geetest_seccode: validate.geetest_seccode
//                 },
//                 success: function (data) {
//
//                     var response = data;
//                     alert(response)
//                     if (response["is_login"]){
//                         if ($.cookie("next_path")){
//                         location.href=$.cookie("next_path")
//                         }
//                         else{
//                             location.href="/index/"
//                         }
//                     }else{
//                         $(".error").html(response["error_msg"]).css("color","red");
//                     }
//                 }
//             });
//         });
//         $("#subBtn").click(function () {
//             captchaObj.show();
//
//         });
//         // 将验证码加到id为captcha的元素里
//         captchaObj.appendTo("#popup-captcha");
//         // 更多接口参考：http://www.geetest.com/install/sections/idx-client-sdk.html
//     };
//     // 验证开始需要向网站主后台获取id，challenge，success（是否启用failback）
//     $.ajax({
//         url: "/pc-geetest/register?t=" + (new Date()).getTime(), // 加随机数防止缓存
//         type: "get",
//         dataType: "json",
//         success: function (data) {
//             // 使用initGeetest接口
//             // 参数1：配置参数
//             // 参数2：回调，回调的第一个参数验证码对象，之后可以使用它做appendTo之类的事件
//             initGeetest({
//                 gt: data.gt,
//                 challenge: data.challenge,
//                 product: "popup", // 产品形式，包括：float，embed，popup。注意只对PC版验证码有效
//                 offline: !data.success // 表示用户后台检测极验服务器是否宕机，一般不需要关注
//                 // 更多配置参数请参见：http://www.geetest.com/install/sections/idx-client-sdk.html#config
//             }, handlerPopup);
//         }
//     });
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
// // 点击提交按钮进行ajax校验；登录的时候只需要校验用户名密码：顺带校验验证码确定事认为操作
// //     $("#subBtn").click(function () {
// //         // alert($.session.get("urls"))
// //         $.ajax({
// //             url:"/login/",
// //             type:"POST",
// //             data:{
// //                 username:$("#username").val(),
// //                 password:$("#password").val(),
// //                 // valid_code:$("#validCode").val(),
// //                 csrfmiddlewaretoken:$("[name='csrfmiddlewaretoken']").val()
// //             },
// //             success:function (data) {
// //                 var response = JSON.parse(data);
// //                 if (response["is_login"]){        //如果校验通过，再次判断，如果获取到urls则跳转该url，否则条状到index页面
// //                     if ($.cookie("next_path")){
// //                         location.href=$.cookie("next_path")
// //                     }
// //                     else{
// //                         location.href="/index/"
// //                     }
//                 // }
// //                 else {
// //                     $(".error").html(response["error_msg"]).css("color","red");
// //                 }
// //             }
// //         })
// //     });
//
//
//
//     //url无刷新验证码
//     $(".validCode_img").click(function () {
//         this.src+="?";
//     });
//
//
//
//
//
//
//
//
