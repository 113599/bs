var http = require("../../api/index");
Page({

    /**
     * 页面的初始数据
     */
    data: {
        isBack: true,
        isRound: true,
        pageHight: 0,
        showInfoFlag: false,
        showPwdFlag: false,
        showProjectFlag: false,
        showExitFlag: false,
        showConfirmBtn: true,
        gender: "",
        userInfo: {},
        infoForm: {
            token: "",
            userName: "",
            name: "",
            gender: "",
            age: ""
        },
        pwdForm: {
            token: "",
            newPwd: "",
            rePwd: "",
            oldPwd: "",
        },
    },

    /**
     * 生命周期函数--监听页面加载
     */
    onLoad(options) {

        this.getPageHeight();
        this.getLoginUser();
    },

    showInfoWin(){

        console.log(this.data.userInfo);
        this.setData({

            showInfoFlag: true
        });
    },
    hideInfoWin(){

        this.setData({
            
            showInfoFlag: false
        });
    },
    showPwdWin(){

        this.setData({

            pwdForm: {
                newPwd: "",
                rePwd: "",
                oldPwd: "",
            },
            showPwdFlag: true
        });
    },
    hidePwdWin(){

        this.setData({

            pwdForm: {
                newPwd: "",
                rePwd: "",
                oldPwd: "",
            },
            showPwdFlag: false
        });
    },
    showExitWin(){

        this.setData({

            showExitFlag: true
        });
    },
    hideExitWin(){

        this.setData({
            
            showExitFlag: false
        });
    },
    showProjectWin(){

        this.setData({

            showProjectFlag: true
        });
    },
    hideProjectWin(){

        this.setData({
            
            showProjectFlag: false
        });
    },
    getPageHeight(){

        wx.getSystemInfo({
            success: resp =>{

                this.setData({
                    pageHight: resp.screenHeight
                });
            }
        })
    },
    getLoginUser(){
        http.getUserInfo((resp) =>{
            this.setData({
                userInfo: resp.data,
                gender: resp.data.gender
            });
        });
    },
    changeGender(e){
        
        this.setData({
            gender: e.detail
        });
    },
    updInfo(e){

        http.updUserInfo({
            token: wx.getStorageSync('token'),
            userName:  e.detail.value.userName,
            name: e.detail.value.name,
            gender: this.data.gender,
            age: e.detail.value.age,
        }, resp =>{
            
            if(resp.code == 0){
                
                wx.showToast({
                    title: resp.msg,
                    icon: 'success'
                });
                this.hideInfoWin();
                this.getLoginUser();
            }else{

                wx.showToast({
                  title: resp.msg,
                  icon: 'none'
                })
            }
        });
    },
    updPwd(e){

        http.updUserPwd({
            token: wx.getStorageSync('token'),
            newPwd:  e.detail.value.newPwd,
            rePwd: e.detail.value.rePwd,
            oldPwd: e.detail.value.oldPwd,
        }, resp =>{
            
            if(resp.code == 0){
                
                wx.showToast({
                    title: resp.msg,
                    icon: 'success'
                });
                this.hidePwdWin();
            }else{

                wx.showToast({
                  title: resp.msg,
                  icon: 'none'
                })
            }
        });
    },
    exit(){

        http.exit(resp =>{

            wx.clearStorage();
            wx.navigateTo({
                url: '../login/login',
            });

        });
        
    }
})