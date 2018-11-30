//         var nb = parseInt($(".nb:last").text()) + 1;     // {# 建楼层用的 #}
//
//         // {# 格式化时间 #}
//         Date.prototype.Format = function (fmt) { //author: meizz
//             var o = {
//                 "M+": this.getMonth() + 1, //月份
//                 "d+": this.getDate(), //日
//                 "h+": this.getHours(), //小时
//                 "m+": this.getMinutes(), //分
//                 "s+": this.getSeconds(), //秒
//                 "q+": Math.floor((this.getMonth() + 3) / 3), //季度
//                 "S": this.getMilliseconds() //毫秒
//             };
//             if (/(y+)/.test(fmt)) fmt = fmt.replace(RegExp.$1, (this.getFullYear() + "").substr(4 - RegExp.$1.length));
//             for (var k in o)
//                 if (new RegExp("(" + k + ")").test(fmt)) fmt = fmt.replace(RegExp.$1, (RegExp.$1.length == 1) ? (o[k]) : (("00" + o[k]).substr(("" + o[k]).length)));
//             return fmt;
//         };
//
//         var createTime = new Date().Format("yyyy年MM月dd日 hh:mm");
//
//
//         // {#        提交评论#}
//         $(".submit").click(function () {
//             var cont = $(".text").val();
//             // {#   当前输入的内容   #}
//
//             $.ajax({
//                 url: "/blog/{{ current_user }}/com/",
//                 type: "POST",
//                 data: {
//                     csrfmiddlewaretoken: $("[name='csrfmiddlewaretoken']").val(),
//                     article_id:{{ article_obj.nid }},
//                     text: $(".text").val()
//                 },
//                 success: function (data) {
//                     data = JSON.parse(data);
//                     if (data["success"]) {
//
//                         var tr = '\
// <div class="row pl">\
//                         <div class="col-md-12">\
//                             <div class="row">\
//                                 <div class="pull-left">\
//                                     <a href="" style="white-space:pre;">#&nbsp;' +  nb  + '&nbsp;楼</a>&nbsp;&nbsp;\
//                                      ' + createTime + ' &nbsp;&nbsp;<a href="">{{ user_obj }}</a>\
//                                 </div>\
//                                 <a href="" class="sendMsg2This"></a>\
//                                 <div class="pull-right"><a href="">回复</a>&nbsp;&nbsp;&nbsp;&nbsp;<a href="">引用</a></div>\
//                             </div>\
//                             <div></div>\
//                             <div class="cont">' + cont + '</div>\
//                             <br>\
//                         </div>\
//                     </div>\
// '
//                         $(".contcont").append(tr);
//
//
//                         $(".text").val("");
//
//                     } else {
//                         alert($.session.get("urls"));
//                         location.href = "/login/"
//                     }
//                 }
//             })
//         });
//
//
//         function foo() {
//             $(".diggnum_error").html("")
//         }
//
//
//         // {#        正常用户#}
//         $(".diggit").click(function () {
//             $.ajax({
//                 url: "/blog/up_count/",
//                 type: "POST",
//                 data: {
//                     csrfmiddlewaretoken: $("[name='csrfmiddlewaretoken']").val(),
//                     article_id:{{ article_obj.nid }}
//                 },
//                 success: function (data) {
//                     data = JSON.parse(data);
//                     if (data["state"]) {
//                         var val = parseInt($("#digg_count").html()) + 1;
//                         $("#digg_count").html(val)
//
//                     } else {
//                         $(".diggnum_error").html("请不要重复点赞").css("color", "red");
//                         setTimeout(foo, 3000)
//
//                     }
//
//                 }
//             })
//         });
//
//
//         $(".buryit").click(function () {
//             $.ajax({
//                 url: "/blog/down_count/",
//                 type: "POST",
//                 data: {
//                     csrfmiddlewaretoken: $("[name='csrfmiddlewaretoken']").val(),
//                     article_id:{{ article_obj.nid }}
//                 },
//                 success: function (data) {
//                     data = JSON.parse(data);
//                     console.log(data);
//                     if (data["state"]) {
//                         var val = parseInt($("#bury_count").html()) + 1;
//                         $("#bury_count").html(val)
//
//                     } else {
//
//                         $(".diggnum_error").html("去你大爷的，").css("color", "red")
//                         setTimeout(foo, 3000)
//
//                     }
//
//                 }
//             })
//         });
//
//
//
//
//         // {#        游客进来之后吧当前的url写到session中，跳转到login页面#}
//         $("#wu_diggnum").click(function () {
//             $.session.set("urls", window.location.href);
//             location.href = "/login/"
//         });
//
//
//         $(".reply").click(function () {
//             alert("没有资格评论")
//         })