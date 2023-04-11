var http = require("../../api/index");
import Dialog from '@vant/weapp/dialog/dialog';
Page({

    /**
     * 页面的初始数据
     */
    data: {
        isBack: true,
        isRound: true,
        showConfirmBtn: true,
        showAddFlag: false,
        showInfoFlag: false,
        showCancleFlag: false,
        infoMsg: "",
        studentId: "",
        pageIndex: 1,
        pageSize: 20,
        total: 0,
        leaves: [],
        leavelForm: {
            id: "",
            reason: "",
            status: ""
        },
    },

    /**
     * 生命周期函数--监听页面加载
     */
    onLoad(options) {

        this.setData({
            studentId: options.studentId
        });
        this.getPageLeaveInfos(1, this.data.pageSize);
    },
    
    onReachBottom(){

        let index = this.data.pageIndex;
        this.setData({
            pageIndex: index+1
        });
        this.getPageLeaveInfos(this.data.pageIndex, this.data.pageSize);
    },

    showAddWin(){

        this.setData({
            showAddFlag: true,
            leavelForm: {
                id: "",
                reason: "",
                status: 0
            }
        });
    },
    hiddenAddWin(){

        this.setData({
            showAddFlag: false,
            leavelForm: {
                id: "",
                reason: "",
                status: 0
            }
        });
    },
    showCancleWin(e){

        this.setData({
            showCancleFlag: true,
            leavelForm: {
                id: e.currentTarget.dataset.id,
                status: 3,
                stuId: this.data.studentId
            }
        });
    },
    hideCancleWin(){

        this.setData({
            showCancleFlag: false,
            leavelForm: {
                id: "",
                status: ""
            }
        });
    },

    showInfoWin(e){

        let temp = "";

        if (e.currentTarget.dataset.status == 2){

            temp = "您的请假申请于 " +  e.currentTarget.dataset.replytime + 
                    " 被 " + e.currentTarget.dataset.teaname + " 老师拒绝, 具体原因是 "
                    + e.currentTarget.dataset.replycomm;
        }else if (e.currentTarget.dataset.status == 3){

            temp = "处理流程已完结，请尽量减少请假，好好学习, 避免影响学习质量!"
        }

        this.setData({
            infoMsg: temp,
            showInfoFlag: true
        });
    },
    hideInfoWin(){

        this.setData({
            infoMsg: "",
            showInfoFlag: false
        });
    },
    getPageLeaveInfos(pageIndex, pageSize){

        http.getPageLeavel({
            pageIndex: pageIndex, 
            pageSize: pageSize, 
            studentId: this.data.studentId
        }, resp =>{

            if(resp.data.data.length > 0){
                
                if(pageIndex==1){

                    this.setData({
                        total: resp.data.count,
                        pageIndex: pageIndex,
                        leaves: resp.data.data
                    });
                }else{
                    let temp = this.data.leaves;
                    resp.data.data.forEach(item =>{

                        temp.push(item);
                    });
                    this.setData({
                        total: resp.data.count,
                        pageIndex: pageIndex,
                        leaves: temp
                    });
                }
                
            } else{

                if(pageIndex==1){

                    this.setData({
                        total: resp.data.count,
                        pageIndex: pageIndex,
                        leaves: []
                    });
                }else{
                    this.setData({
                        pageIndex: pageIndex-1
                    });
                }
            }           
        });
    },
    addInfo(e){

        http.addLeavel({
            studentId: this.data.studentId,
            reason: e.detail.value.reason
        }, resp =>{

            if(resp.code == 0){
                
                wx.showToast({
                    title: resp.msg,
                    icon: 'success'
                });
                this.hiddenAddWin();
                this.getPageLeaveInfos(1, this.data.pageSize);
            }else{

                wx.showToast({
                  title: resp.msg,
                  icon: 'none'
                })
            }
        })
    },
    updInfo(e){

        http.updLeavel(this.data.leavelForm, resp =>{

            if(resp.code == 0){
                
                wx.showToast({
                    title: '销假处理成功',
                    icon: 'success'
                });
                this.hideCancleWin();
                this.getPageLeaveInfos(1, this.data.pageSize);
            }else{

                wx.showToast({
                  title: resp.msg,
                  icon: 'none'
                })
            }
        });
    }

})
