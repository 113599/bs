let http = require("../../api/index");
Page({

    data: {
        isBack: true,
        gradeId: "",
        projects: []
    },

    onLoad(options) {

        this.getProjectInfos(options.gradeId);
    },

    
    getProjectInfos(gradeId){

        http.getProjects(gradeId, resp =>{

            this.setData({
                projects: resp.data
            });
        });
    }
})