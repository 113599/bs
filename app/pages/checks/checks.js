var http = require("../../api/index");
Page({

    /**
     * 页面的初始数据
     */
    data: {
        isBack: true,
        isRound: true,
        showAddFlag: false,
        stuId: "",
        pageIndex: 1,
        pageSize: 20,
        total: 0,
        checks: [],
        checkForm: {
            checkNo: "",
            studentId: ""
        }
    },

    /**
     * 生命周期函数--监听页面加载
     */
    onLoad(options) {

        this.setData({
            studentId: options.studentId
        });
        this.getPageCheckInfos(1, this.data.pageSize);
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
            checkForm: {
                checkNo: "",
                studentId: this.data.stuId
            }
        });
    },
    hideAddWin(){
        this.setData({
            showAddFlag: false,
            checkForm: {
                checkNo: "",
                studentId: ""
            }
        });
    },
    getPageCheckInfos(pageIndex, pageSize){

        http.getPageCheckLogs({

            pageIndex: pageIndex, 
            pageSize: pageSize, 
            studentId: this.data.studentId
        }, resp =>{

            if(resp.data.data.length > 0){

                resp.data.data.forEach(item =>{

                    let temp = item.createTime.split(" ");
                    item['checkDate']=temp[0];
                    item['checkTime']=temp[1];
                });
                
                if(pageIndex==1){

                    this.setData({
                        total: resp.data.count,
                        pageIndex: pageIndex,
                        checks: resp.data.data
                    });
                }else{
                    let temp = this.data.checks;
                    resp.data.data.forEach(item =>{

                        temp.push(item);
                    });
                    this.setData({
                        total: resp.data.count,
                        pageIndex: pageIndex,
                        checks: temp
                    });
                }
            } else{

                if(pageIndex==1){

                    this.setData({
                        total: resp.data.count,
                        pageIndex: pageIndex,
                        checks: []
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

        http.addCheck({
            studentId: this.data.studentId,
            checkNo: e.detail.value.checkNo
        }, resp =>{

            if(resp.code == 0){
                
                wx.showToast({
                    title: resp.msg,
                    icon: 'success'
                });
                this.hideAddWin();
                this.getPageCheckInfos(1, this.data.pageSize);
            }else{

                wx.showToast({
                  title: resp.msg,
                  icon: 'none'
                })
            }
        })
    }
    
})