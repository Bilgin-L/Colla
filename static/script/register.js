function bindCaptchaBtnClick(){
    $("#captcha-btn").on("click", function (event){
        var $this = $(this)
        var email = $("input[name='email']").val();
        var username = $("input[name='username']").val();
        if(!email){
            alert("Colla: Please enter your e-mail first!");
            return;
        }
        // 通过js发送网络请求：ajax：Async Javascript And XML
        $.ajax({
            url: "/captcha",
            method: "POST",
            data: {
                "email": email,
                "username": username
            },
            success: function (res){
                var code = res['code']
                if (code === 200){
                    //取消点击事件
                    $this.off("click")
                    //开始倒计时
                    var countDown = 60;
                    var timer = setInterval(function (){
                        if(countDown > 0){
                            $this.text(countDown+"秒后重新发送")
                        }else {
                            $this.text("获取验证码");
                            // 重新绑定点击事件
                            bindCaptchaBtnClick();
                            // 如果不需要倒计时了，那么就需要记得清除，否则会一直执行下去
                            clearInterval(timer)
                        }
                        countDown -= 1;
                    }, 1000)
                    alert("验证码发送成功！");
                }else {
                    alert(res['message']);
                }
            }
        })
    })
}

// 等网页文档所有元素都加载完成后再执行
$(function (){
    bindCaptchaBtnClick();
}
)