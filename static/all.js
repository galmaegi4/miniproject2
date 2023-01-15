
function go_login_page(){
  location.href='http://192.168.0.128:5000/login'
}

function join_member() {
  let user_id = $('#id').val()
  let user_password = $('#password').val()
  let user_name = $('#name').val()
  let user_nickname = $('#nickname').val()

    let user_image = $('#uproad_img').val()
    user_image = user_image.split("\\")
    let user_img = user_image[user_image.length -1]


  $.ajax({
    type: "POST",
    url: "member/join",
    data: {
      'user_id': user_id, 'user_password': user_password, 'user_name': user_name,
      'user_nickname': user_nickname, 'user_image':user_img
    },
    success: function (response) {
      alert(response['msg'])
      window.location.reload()
      location.href = 'http://192.168.0.128:5000/login'
    }
  });


}





function go_member_page(){
      location.href = 'http://192.168.0.128:5000/member'
}

function log_in(){
    let login_id = $('#login_id').val()
    let login_password = $('#login_password').val()
    let state = false
    $.ajax({
        type: "POST",
        url: `/login/checkid`,
        data: {'login_id':login_id, 'login_password':login_password},
        success: function (response) {
            console.log(response)
          let rows = response['login_permission']
            if (rows) {
                state = true
            }
            if (state){
                sessionStorage.setItem("session_login_id", login_id )
                location.href = 'http://192.168.0.128:5000/'

            }else {
                alert("아이디 비밀번호가 일치하지 않습니다.")
            }
        }
    });

}

function go_mypage() {
    location.href = 'http://192.168.0.128:5000/mypage'
}

function logout() {
    sessionStorage.clear()
    location.href = 'http://192.168.0.128:5000/'
}

function go_myblog(){
    let id = sessionStorage.getItem('session_id')
    if (id != null) {
        location.href = `http://192.168.0.128:5000/blog/${id}`
    } else {
        location.href = 'http://192.168.0.128:5000/'
    }

}



