function user() {
    var user = $('input[name="username"]').val();
    return user;
}

function name() {
    var name = $('input[name="name"]').val();
    return name;
}

function pwd() {
    var pwd = $('input[name="password"]').val();
    return pwd;
}

function checkpwd() {
    var pwd = $('input[name="password"]').val();
    var c_pwd = $('input[name="confirm-password"]').val();
    if (c_pwd != "" && pwd != c_pwd) {
        alert("密碼不相同，請重新輸入");
    }
}

function email() {
    var email = $('input[name="email"]').val();
    return email;
}

function bday() {
    var bday = $('input[name="birthday"]').val();
    return bday;
}

function signup() {

    if (user() == null || user() == "") {
        alert("帳號漏填寫喔~");
    } else if (name() == null || name() == "") {
        alert("姓名漏填寫喔~");
    } else if (pwd() == null || pwd() == "") {
        alert("密碼漏填寫喔~");
    } else if ($('input[name="confirm-password"]').val() == null || $('input[name="confirm-password"]').val() == "") {
        alert("確認密碼漏填寫喔~");
    } else if (email() == null || email() == "") {
        alert("郵件漏填寫喔~");
    } else if (bday() == null || bday() == "") {
        alert("生日漏填寫喔~");
    } else {
        var r = confirm("使用帳號:" + user() + "\n姓名:" + name() + "\n密碼:" + pwd() + "\ne-mail:" + email() + "\n生日:" + bday());
    }


}