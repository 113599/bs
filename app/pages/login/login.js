let http = require("../../api/index");
Page({

    /**
     * 页面的初始数据
     */
    data: {
        hideBorder: false,
        loginForm: {
            userName: "",
            passWord: "",
            type: "app"
        },
    },

    /**
     * 生命周期函数--监听页面加载
     */
    onLoad(options) {

    },

    login(e){

        if(e.type=='submit'){

            http.login({
                userName: e.detail.value.userName,
                passWord: e.detail.value.passWord,
                type: 'app'
            },
            (resp) =>{
                if(resp.code == 0){
                    // wx.setStorageSync('token', resp.data.token);

                    wx.setStorage({
                        key: "token",
                        data: resp.data.token
                    });

                    wx.redirectTo({
                        url: "../index/index"
                    });
                }else{

                    wx.showToast({
                      title: resp.msg,
                      icon: 'none'
                    })
                }
            });
        }
    }
})