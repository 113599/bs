<template>
	<div class="fater-body-show">
        <Card>
            <template #title>
				信息查询
			</template>
			<div>
				<Form :model="qryForm" inline>
					<FormItem v-if="userInfo.type == 0">
						<Input type="text" v-model="qryForm.teacherName" placeholder="教师姓名……"></Input>
					</FormItem>
                    <FormItem>
                        <Select style="width: 200px" v-model="qryForm.gradeId" placeholder="选择班级……">
                            <Option value="">查看全部</Option>
                            <Option v-for="(item, index) in grades" 
                                    :value="item.gradeId" :key="index">{{ item.gradeName }}</Option>
                        </Select>
					</FormItem>
					<FormItem>
						<Button type="primary" @click="getPageInfo(1, 10)">
							<Icon type="ios-search" />
						</Button>
					</FormItem>
				</Form>
			</div>
		</Card>

        <Card>
			<template #title>
				<Button @click="showAddWin()"  v-if="userInfo.type == 1" type="primary">
					<Icon type="md-add" />
				</Button>
			</template>
			<div>
				<Table border :columns="columns" :loading="loading" :data="pageInfos">
                    <template #status="{ row }">
						<Tag v-if="row.status==0" type="border" color="primary">考勤中</Tag>
						<Tag v-if="row.status==1" type="border" color="warning">已关闭</Tag>
					</template>
                    <template #detail="{ row }">
						<Button size="small" ghost type="info" @click="showDetailWin(row.no)">查看详情</Button>
					</template>
					<template #action="{ row }">
						<Button v-if="row.status==0"
                                size="small" type="info" @click="cancelCheck(row.no)">结束</Button>
						<Button v-else size="small" type="info" disabled>结束</Button>
					</template>
				</Table>
				<Page style="margin-top: 15px;" v-if="pageTotal > 1" :current="pageIndex"
					@on-change="handleCurrentChange" :total="totalInfo" show-total/>
			</div>
		</Card>

        <Modal v-model="showAddFlag"
			title="考勤设置" ok-text="提交" cancel-text="取消" @on-ok="addInfo()">
			<Form :label-width="80" :model="checkForm">
				<FormItem label="学院名称">
					<Select v-model="checkForm.gradeId" placeholder="选择考勤处理班级……">
                        <Option v-for="(item, index) in grades" 
                                :value="item.gradeId" :key="index">{{ item.gradeName }}</Option>
                    </Select>
				</FormItem>
			</Form>
		</Modal>

        
        <Modal v-model="showDetailFlag" fullscreen="true" footer-hide="true" title="考勤详情">
			<Table border :columns="checkCols" :data="checkLogs">
            </Table>
		</Modal>
    </div>
</template>

<script>
import {
    getCheckListByNo,
    getPageChecks,
    addCheck,
    updCheck,
    getTeacherWork,
    getAllGrades,
    getLoginUser,
} from '../../api/index.js';
export default{
		
    data(){
        return {
            userInfo: {},
            checkLogs: [],
            grades: [],
            pageInfos: [],
            pageIndex: 1,
            pageSize: 10,
            pageTotal: 0,
            totalInfo: 0,
            loading: true,
            showAddFlag: false,
            showDetailFlag: false,
            qryForm: {
                gradeId: "",
                teacherId: "",
                teacherName: "",
            },
            checkForm: {
                id: "",
                gradeId: "",
                teacherId: "",
                status: 0
            },
            columns: [],
            checkCols: [
                {title: '序号', type: 'index', width: 70, align: 'center'},
                {title: '学生学号', key: 'studentId', align: 'center'},
                {title: '学生姓名', key: 'studentName', align: 'center'},
                {title: '所属班级', key: 'gradeName', align: 'center'},
                {title: '签到时间', key: 'createTime', align: 'center'},
            ]
        }
    },
    methods: {

        getPageInfo(pageIndex, pageSize) {
			
            getPageChecks(pageIndex, pageSize, 
                    this.qryForm.gradeId, this.qryForm.teacherId, this.qryForm.teacherName).then(resp => {
                
                this.pageInfos = resp.data.data;
                this.pageIndex = resp.data.pageIndex;
                this.pageSize = resp.data.pageSize;
                this.pageTotal = resp.data.pageTotal;
                this.totalInfo = resp.data.count;
        
                this.loading = false;
            });
        },
        handleCurrentChange(pageIndex) {
        
            this.getPageInfo(pageIndex, this.pageSize);
        },
        showDetailWin(checkNo){

            getCheckListByNo(checkNo).then(resp =>{
                
                this.checkLogs = resp.data;
                this.showDetailFlag = true;
            });
        },
        showAddWin(){

            this.checkForm = {
                id: "",
                gradeId: "",
                teacherId: this.userInfo.id,
                status: 0
            };
            this.showAddFlag = true;
        },	
        addInfo(){

            addCheck(this.checkForm).then(resp =>{

                if(resp.code == 0){

                    this.$Notice.success({
                        duration: 3,
                        title: resp.msg
                    });
                    this.showAddFlag = false;
                    this.getPageInfo(1, this.pageSize);
                }else{
                    
                    this.$Notice.warning({
                        duration: 3,
                        title: resp.msg
                    });
                    this.showAddFlag = true;
                }
            });
        },
        cancelCheck(no){

            this.$Modal.confirm({
                title: '系统提示',
                content: '即将关闭考勤, 是否继续?',
                onOk: () => {
                    updCheck({
                        no: no
                    }).then(resp =>{
                        
                        if(resp.code == 0){
                            this.$Notice.success({
                                duration: 3,
                                title: resp.msg
                            });
                            
                            this.getPageInfo(1, this.pageSize);
                        }else{
                            
                            this.$Notice.warning({
                                duration: 3,
                                title: resp.msg
                            });
                        }
                    });
                },
            });
        }
    },
    mounted(){
        
        getLoginUser(this.$store.state.token).then(resp =>{

            this.userInfo = resp.data;

            if(resp.data.type == 0){
                
                getAllGrades().then(res =>{

                    res.data.forEach(item =>{

                        this.grades.push({
                            gradeId: item.id,
                            gradeName: item.name,
                        });
                    });
                });

                this.columns = [
                    {title: '序号', type: 'index', width: 70, align: 'center'},
                    {title: '考勤码', key: 'no', align: 'center'},
                    {title: '教师工号', key: 'teacherId', align: 'center'},
                    {title: '处理教师', key: 'teacherName', align: 'center'},
                    {title: '考核班级', key: 'gradeName', align: 'center'},
                    {title: '发布时间', key: 'createTime', align: 'center'},
                    {title: '签到人数', key: 'total', align: 'center'},
                    {title: '考勤记录', slot: 'detail', align: 'center'},
                    {title: '考勤状态', slot: 'status', align: 'center'}
                ];
            }else{

                getTeacherWork(resp.data.id).then(res =>{

                    res.data.forEach(item =>{
                        
                        let flag = false;

                        for(let i = 0; i < this.grades.length; i++){

                            if ((this.grades[i]).gradeId == item.gradeId){
                                
                                flag = true;
                                break;
                            }
                        }

                        if(!flag){
                            
                            this.grades.push({

                                gradeId: item.gradeId,
                                gradeName: item.gradeName,
                            });
                        }
                    });
                });
                this.qryForm.teacherId = resp.data.id;
                this.columns = [
                    {title: '序号', type: 'index', width: 70, align: 'center'},
                    {title: '考勤码', key: 'no', align: 'center'},
                    {title: '考核班级', key: 'gradeName', align: 'center'},
                    {title: '发布时间', key: 'createTime', align: 'center'},
                    {title: '签到人数', key: 'total', align: 'center'},
                    {title: '考勤记录', slot: 'detail', align: 'center'},
                    {title: '考勤状态', slot: 'status', align: 'center'},
                    {title: '考勤处理', slot: 'action', align: 'center'}
                ];
            }

            this.getPageInfo(1, this.pageSize);
        });
    }
}
</script>