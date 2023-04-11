// components/fater-nav/fater-nav.js
Component({
    /**
     * 组件的属性列表
     */
    properties: {
        title: {
            type: String,
            default: ''
        },
        isHideBorder: {
            type: [Boolean, String],
            default: false
        },
        isBack: {
            type: [Boolean, String],
            default: false
        }
    },

    /**
     * 组件的初始数据
     */
    data: {

    },

    /**
     * 组件的方法列表
     */
    methods: {
        toHome(){
            wx.reLaunch({
                url: '/pages/index/index',
            })
        }
    }
})
