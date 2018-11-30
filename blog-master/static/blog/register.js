// 注册页面的主要js代码


    var per_error_arr = [];

    $(".ajax_signUp").click(function () {
        var form = new FormData();
        form.append("username",$("[name=username]").val());
        form.append("password",$("[name=password]").val());
        form.append("repassword",$("[name=repassword]").val());
        form.append("email",$("[name=email]").val());
        form.append("valid_code",$("[name=valid_code]").val());
        var fileobj =$("#preScan").next()[0].files[0];

        // console.log(fileobj);

        $.ajax({
            url: "/reg/",
            type: "POST",
            data: form,
            processData: false,
            contentType: false,
            headers: {"X-CSRFToken": $.cookie('csrftoken')},
            success: function (data) {

                data = JSON.parse(data);
                if (data["user"]) {
                    alert("OK");
                    location.href="/login/"
                }
                else if(data["errors"]){
                    var error_list = data["errors"];
                    console.log("per_error_arr",per_error_arr);
                    $(".Yuan").css("border","").next().remove();

                    for (var error in error_list){
                        $div=$("<div>").addClass("row");

                       $div_in=$("<div>").addClass("col-md-5").addClass("col-md-offset-9");

                       $div.append($div_in);

                       console.log($div);
                       if (error=="__all__"){
                            $div_in.text("密码不一致!");
                            $("#id_repeat_password").css("border","2px solid red").after($div);
                       }

                       $div_in.text(errors[error]);
                       $("#id_"+error).css("border","2px solid red").addClass("Yuan").after($div);
                    }
                    pre_error_arr=errors_list;
                   console.log("pre_error_arr",pre_error_arr)
                }
            }
        })

    });



    $(".validCode_img").click(function () {
        this.src+="?";
    });


    $("#avator").change(function () {
        console.log("OK");
        var first_file = $(this)[0].files[0];
        var reader = new FileReader();
        reader.readAsDataURL(first_file);
        reader.onload=function () {
            $("#preScan").attr("src",this.result)
        }
    })