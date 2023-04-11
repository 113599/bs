<template>
	<div class="fater-body-show">
        <Card>
            <template #title>
				信息查询
			</template>
			<div>
				<Form :model="qryForm" inline>
					<FormItem>
						<Input type="text" v-model="qryForm.name" placeholder="班级名称……"></Input>
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
				<Button @click="showAddWin()" type="primary">
					<Icon type="md-add" />
				</Button>
			</template>
			<div>
				<Table border :columns="columns" :loading="loading" :data="pageInfos">
					<template #action="{ row }">
						<Button style="margin-right: 5px;" 
                                size="small" type="info" icon="md-create" @click="showUpdWin(row)"></Button>
						<Button size="small" type="warning" icon="ios-trash" @click="delInfo(row.id)"></Button>
					</template>
                    <template #work="{ row }">
                        <Button size="small" type="info" @click="showWorkWin(row.id)">工作设置</Button>
                    </template>
				</Table>
				<Page style="margin-top: 15px;" v-if="pageTotal > 1" :current="pageIndex"
					@on-change="handleCurrentChange" :total="totalInfo" show-total/>
			</div>
		</Card>

        <Modal v-model="showAddFlag"
			title="信息编辑" ok-text="提交" cancel-text="取消" @on-ok="addInfo()">
			<Form :label-width="80" :model="gradeForm">
				<FormItem label="班级名称" prop="reord">
					<Input v-model="gradeForm.name" placeholder="请输入班级名称..."></Input>
				</FormItem>
			</Form>
		</Modal>

        <Modal v-model="showUpdFlag"
			title="信息编辑" ok-text="提交" cancel-text="取消" @on-ok="updInfo()">
			<Form :label-width="80" :model="gradeForm">
				<FormItem label="班级名称" prop="reord">
					<Input v-model="gradeForm.name" placeholder="请输入班级名称..."></Input>
				</FormItem>
			</Form>
		</Modal>

        <Modal v-model="showWorkFlag" fullscreen="true" footer-hide="true" title="班级工作安排">
			<Table border :columns="workCols" :data="works">
				<template #teacherInfo="{ row }">
                    <span v-if="row.teacherName">{{ row.teacherName }}</span>
                    <span v-else>暂未设置</span>
                </template>
                <template #jobInfo="{ row }">
                    <span v-if="row.job==0">授课教师</span>
                    <span v-else-if="row.job==1">班主任</span>
                    <span v-else>暂未设置</span>
                </template>
                <template #workBtn="{ row }">
                    <Button size="small" type="info" @click="showSetWorkWin(row)">授课安排</Button>
                </template>	
			</Table>
		</Modal>

        <Modal v-model="showSetWorkFlag"
			title="信息编辑" ok-text="提交" cancel-text="取消" @on-ok="settingWork()">
			<Form :label-width="80" :model="workForm">
				<FormItem label="教师工号">
					<Input v-model="workForm.teacherId" placeholder="请输入授课教师工号..."></Input>
				</FormItem>
				<FormItem label="教师职责">
					<RadioGroup v-model="workForm.job">
                        <Radio label="0">授课教师</Radio>
                        <Radio label="1">班主任</Radio>
                    </RadioGroup>
				</FormItem>
			</Form>
		</Modal>
    </div>
</template>

<style></style>

<script>import {
    getSetWorks,
    setWork,
    getPageGrades,
    addGrades,
    updGrades,
    delGrades,
} from '../../api/index.js';

export default{
		
    data(){
        return {
            works: [],
            pageInfos: [],
            pageIndex: 1,
            pageSize: 10,
            pageTotal: 0,
            totalInfo: 0,
            loading: true,
            showAddFlag: false,
            showUpdFlag: false,
            showWorkFlag: false,
            showSetWorkFlag: false,
            qryForm: {
                name: "",
            },
            workForm: {
                id: "",
                gradeId: "",
                projectId: "",
                teacherId: "",
                job: 0,
            },
            gradeForm: {
                id: "",
                name: ""
            },
            columns: [
                {title: '序号', type: 'index', width: 70, align: 'center'},
                {title: '班级名称', key: 'name', align: 'center'},
                {title: '添加时间', key: 'createTime', align: 'center'},
                {title: '工作安排', slot: 'work', align: 'center'},
                {title: '操作', slot: 'action', align: 'center'}
            ],
            workCols: [
                {title: '序号', type: 'index', width: 70, align: 'center'},
                {title: '课程名称', key: 'projectName', align: 'center'},
                {title: '授课教师', slot: 'teacherInfo', align: 'center'},
                {title: '工作职责', slot: 'jobInfo', align: 'center'},
                {title: '授课安排', slot: 'workBtn', align: 'center'}
            ]
        }
    },
    methods:{
			
		getPageInfo(pageIndex, pageSize) {
			
            getPageGrades(pageIndex, pageSize, 
                    this.qryForm.name).then(resp => {
                
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
        showWorkWin(id){

            getSetWorks(id).then(resp =>{

                this.works = resp.data;

                this.workForm.gradeId = id;
                this.showWorkFlag = true;
            });
        },	
        showAddWin(){

            this.gradeForm = {
                name: ""
            };
            this.showAddFlag = true;
        },
        showUpdWin(row) {
			
            this.gradeForm = row;
            this.showUpdFlag = true;
        },
        addInfo() {
			
            addGrades(this.gradeForm).then(resp => {
                
                this.$Notice.success({
                    duration: 3,
                    title: resp.msg
                });
                
                this.getPageInfo(1, this.pageSize);
                
                this.showAddFlag = false;
            });
        },
        updInfo() {
        
            updGrades(this.gradeForm).then(resp => {
        
                this.$Notice.success({
                    duration: 3,
                    title: resp.msg
                });
        
                this.getPageInfo(1, this.pageSize);
        
                this.showUpdFlag = false;
            });
        },
        delInfo(id){

            this.$Modal.confirm({
                title: '系统提示',
                content: '即将删除相关信息, 是否继续?',
                onOk: () => {
                    delGrades(id).then(resp =>{
                        
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
        },
        showSetWorkWin(row){

            this.workForm.projectId = row.projectId;
            this.workForm.teacherId = row.teacherId;
            this.workForm.job = row.job.toString();
            this.showSetWorkFlag = true;

            console.log(row, this.workForm);
        },
        settingWork(){

            setWork(this.workForm).then(resp =>{

                this.$Message.success({
                    content: resp.msg
                });
                getSetWorks(this.workForm.gradeId).then(resp =>{

                    this.works = resp.data;
                    this.showSetWorkFlag = false;
                });
                
            });
        }
    },
    mounted(){

        this.getPageInfo(1, this.pageSize);
    }
}
</script>