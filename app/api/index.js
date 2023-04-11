const server = "http://localhost:8000/api";

function request(url, method, param, callback){
    wx.request({
        url: server + url,
        header: {
            "content-type": "application/x-www-form-urlencoded"
        },
        method: method,
        data: param,
        success: function(res) {

            if(res.data.code == 0){

                callback(res.data);
            }else if(res.data.code == 1){

                callback(res.data);
            }else{
                wx.showToast({
                    title: res.data.msg,
                    icon: 'error'
                })
            }
        },
        fail: function(){
            wx.showToast({
                title: '系统异常',
                icon: 'error',
                duration: 2000
            })
        }
    });
}

/** 系统请求处理 */
export function login(param, callback){
    
    request("/login/", "POST", param, callback);
}
export function exit(callback){
    
    let token = wx.getStorageSync('token');
    request("/exit/", "POST", {token: token}, callback);
}
export function getUserInfo(callback){
    
    let token = wx.getStorageSync('token');
    request("/info/", "GET", {token: token}, callback);
}
export function updUserInfo(param, callback){
    
    request("/info/", "POST", param, callback);
}
export function updUserPwd(param, callback){
    
    request("/pwd/", "POST", param, callback);
}

/** 校园公告获取 */
export function getNotice(callback){

    request("/notices/show/", "GET", null, callback);
}

/** 课程安排查看 */
export function getProjects(gradeId, callback){

    request("/works/stuworklist/", "GET", {gradeId: gradeId}, callback);
}

/** 考勤打卡处理 */
export function getPageCheckLogs(param, callback){
    
    request("/checklogs/referstu/", "GET", param, callback);
}
export function addCheck(param, callback){

    request("/checklogs/add/", "POST", param, callback);
}

/** 学生请假处理 */
export function getPageLeavel(param, callback){
    
    request("/leaves/page/", "GET", param, callback);
}
export function addLeavel(param, callback){

    request("/leaves/add/", "POST", param, callback);
}
export function updLeavel(param, callback){

    request("/leaves/upd/", "POST", param, callback);
}
