$(function(){
    // 设置默认为“false”（没有错误）才能提交表单
    var error_name = false;
    var error_pwd = false;
    var error_cpwd = false;
    var error_email = false;
    var error_allow = false;
    // 设置失去焦点即光标离开的时候，进行表单验证
    $('#user_name').blur(function(){
        check_username();
    });
    // 设置获得焦点即有光标的时候，隐藏提示信息
    $('#user_name').focus(function(){
        $(this).next().hide();
    });
    $('#pwd').blur(function(){
        check_pwd();
    });
    $('#pwd').focus(function(){
        $(this).next().hide();
    });
    $('#cpwd').blur(function(){
        check_cpwd();
    });
    $('#cpwd').focus(function(){
        $(this).next().hide();
    });
    $('#email').blur(function(){
        check_email();
    });
    $('#email').focus(function(){
        $(this).next().hide();
    });
    // 设置勾选同意协议
    $('#allow').click(function(){
        // 如果勾选协议
        // 使用prop()方法（不能使用attr()方法）读取checkbox属性的状态是否是checked
        if($(this).prop('checked')==true){
            error_allow = false;
            $('.error_tip2').hide();
        }
        // 没有勾选协议
        else{
            error_allow = true;
            $('.error_tip2').html('请勾选同意！').show();
        }
    });
    function check_username(){
        var val = $('#user_name').val();
        // 定义一个正则的规则：忽略大小写，5~15位数字、字母或下划线
        var re = /^\w{5,15}$/i;
        // 如果输入为空，显示提示信息
        if(val==''){
            $('#user_name').next().html('用户名不能为空！');
            $('#user_name').next().show();
            // 设置为“true”（有错误），不能提交表单
            error_name = true;
            // 结束函数的运行
            return;
        }
        // 如果有返回值：符合正则
        if(re.test(val)){
            // 发送get请求：发送用户名过去。请求配置好的url（真正的网址是到“?”之前），从?开始是需要传的参数：$('#user_name').val()，data表示发送给服务器的数据
            $.get('/user/register_exist/?uname='+$('#user_name').val(),function(data){
                if(data.count==1){
                    $('#user_name').next().html('用户名已存在').show();
                    error_name = true;
                }
                else{
                    $('#user_name').next().hide();
                    // 设置为“false”（没有错误），可以提交表单
                    error_name = false;
                }
            });
        }
        // 不符合正则
        else{
            error_name = true;
            // 显示提示信息
            $('#user_name').next().html('用户名是包含数字、字母或下划线的5到15位字符！');
            $('#user_name').next().show();
        }
    }
    function check_pwd(){
        var val = $('#pwd').val();
        // 定义一个正则的规则：6~16位数字、字母或特殊符号（@不需要转义，$、*、.、!、?都需要转义）
        var re = /^[a-zA-Z0-9@\$\*\.\!\?]{6,16}$/;
        if(val==''){
            $('#pwd').next().html('密码不能为空！');
            $('#pwd').next().show();
            error_pwd = true;
            return;
        }
        if(re.test(val)){
            error_pwd = false;
        }
        else{
            error_pwd = true;
            $('#pwd').next().html('密码是包含数字,字母或@,$,*,.,!,?的6到16位数字！');
            $('#pwd').next().show();
        }
    }
    // 验证密码
    function check_cpwd(){
        var val = $('#pwd').val();
        var cval = $('#cpwd').val();
        if(val==cval){
            error_cpwd = false;
        }
        else{
            error_cpwd = true;
            $('#cpwd').next().html('两次输入的密码不一致！');
            $('#cpwd').next().show();
        }
    }
    function check_email(){
        var val = $('#email').val();
        // 定义一个正则的规则：
        var re = /^[a-zA-Z0-9][\w\.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$/;
        if(val==''){
            $('#email').next().html('邮箱不能为空！');
            $('#email').next().show();
            error_email = true;
            return;
        }
        if(re.test(val)){
            error_email = false;
        }
        else{
            error_email = true;
            $('#email').next().html('邮箱格式错误');
            $('#email').next().show();
        }
    }
    // 设置提交表单
    $('.regform_input').submit(function(){
        // 设置默认执行表单验证
        check_username();
        check_pwd();
        check_cpwd();
        check_email();
        // 如果它们的值全是false
        if(error_name == false && error_pwd == false && error_cpwd == false && error_email == false && error_allow == false){
            // 可以提交
            return true;
        }
        else{
            // 不能提交
            return false;
        }
        // 或
        // 如果它们的值不全是false：使用!取反？？？
        /* if(!(error_name == false && error_pwd == false && error_cpwd == false && error_email == false && error_allow == false)){
            return false;
        }
        else{
            return true;
        } */
    });
});