let http = require("../../api/index");
let util = require("../../utils/util");
import Dialog from '@vant/weapp/dialog/dialog';
Page({


    data: {
        userInfo: {},
        notice: {},
        dateStr: "",
        timeStr: ""
    },

    onLoad(options) {

        this.getLoginUser();

        this.getDateInfo();
    },
    onShow(){

        setInterval(() =>{

            this.getDateInfo();
        }, 1000*60);
    },
    getLoginUser(){
        http.getUserInfo((resp) =>{
            this.setData({
                userInfo: resp.data
            });
        });
    },
    getDateInfo(){

        let temp = util.getDateInfo();
        this.setData({
            dateStr: temp.d,
            timeStr: temp.t
        });
    },
    showNotice(){

        http.getNotice(resp =>{

            Dialog.alert({
                title: resp.data.title,
                messageAlign: 'left',
                message: resp.data.detail,
                confirmButtonText: '知道了',
            })
        });
        
    },
    showMore(){
        Dialog.alert({
            messageAlign: 'left',
            message: '嗨，大家好，我是小胖，一名普通程序员，如果需要项目代码和设计文档关注我的微信公众号肥仔编程或者搜索小程序编程苑联系我付费获取，感谢您的支持和帮助',
            confirmButtonText: '知道了',
        })
    },
    toProjectPage(){

        wx.navigateTo({
          url: '../projects/projects?gradeId=' + this.data.userInfo.gradeId,
        })
    },
    toCheckPage(){

        wx.navigateTo({
          url: '../checks/checks?studentId=' + this.data.userInfo.id,
        })
    },
    toLeavePage(){

        wx.navigateTo({
          url: '../leaves/leaves?studentId=' + this.data.userInfo.id,
        })
    },
    toSettingPage(){

        wx.navigateTo({
          url: '../settings/settings?studentId=' + this.data.userInfo.id,
        })
    },
})