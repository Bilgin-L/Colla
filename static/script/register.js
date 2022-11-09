// # ///////////////////////////////////////////////////////////////////////////
// # @file: register.js
// # @time: 2022/10/19
// # @author: Yuheng Liu
// # @email: sc20yl2@leeds.ac.uk && i@bilgin.top
// # @organisation: University of Leeds
// # @url: colla.bilgin.top
// # ///////////////////////////////////////////////////////////////////////////

// get the captcha
function bindCaptchaBtnClick() {
    $("#captcha-btn").on("click", function (event) {
        var $this = $(this)
        var email = $("input[name='email']").val();
        var username = $("input[name='username']").val();
        if (!email) {
            alert("Colla: Please enter your e-mail first!");
            return;
        }
        // Send the request throw js：ajax：Async Javascript And XML
        $.ajax({
            url: "/captcha",
            method: "POST",
            data: {
                "email": email,
                "username": username
            },
            success: function (res) {
                var code = res['code']
                if (code === 200) {
                    // cancel the click event
                    $this.off("click")
                    // start the countdown
                    var countDown = 60;
                    var timer = setInterval(function () {
                        if (countDown > 0) {
                            $this.text(countDown + " s")
                        } else {
                            $this.text("Send");
                            // rebind the click event
                            bindCaptchaBtnClick();
                            // If the countdown is not needed, it needs to be cleared,
                            // otherwise it will continue to execute
                            clearInterval(timer)
                        }
                        countDown -= 1;
                    }, 1000)
                    alert("Captcha has been sent to your e-mail!");
                } else {
                    alert(res['message']);
                }
            }
        })
    })
}

// wait for the web page to load all elements
$(function () {
        bindCaptchaBtnClick();
    }
)