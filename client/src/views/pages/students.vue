<template>
	<div class="fater-body-show">
        <Card>
            <template #title>
				信息查询
			</template>
			<div>
				<Form :model="qryForm" inline>
					<FormItem>
						<Input type="text" v-model="qryForm.stuName" placeholder="学生姓名……"></Input>
					</FormItem>
					<FormItem>
                        <Select style="width: 200px" v-model="qryForm.collegeId" placeholder="选择学院……">
                            <Option value="">查看全部</Option>
                            <Option v-for="(item, index) in colleges" 
                                    :value="item.id" :key="index">{{ item.name }}</Option>
                        </Select>
					</FormItem>
					<FormItem>
                        <Select style="width: 200px" v-model="qryForm.gradeId" placeholder="选择班级……">
                            <Option value="">查看全部</Option>
                            <Option v-for="(item, index) in grades" 
                                    :value="item.id" :key="index">{{ item.name }}</Option>
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
					<template #status="{ row }">
                        <span v-if="row.status == 0">正常</span>
                        <span v-else>休假</span>
					</template>
				</Table>
				<Page style="margin-top: 15px;" v-if="pageTotal > 1" :current="pageIndex"
					@on-change="handleCurrentChange" :total="totalInfo" show-total/>
			</div>
		</Card>

        <Modal width="800" v-model="showAddFlag"
			title="信息编辑" ok-text="提交" cancel-text="取消" @on-ok="addInfo()">
			<Form :label-width="80" :model="studentForm">
                <FormItem label="学生学号">
                    <Input v-model="studentForm.id" placeholder="请输入学生学号..."></Input>
                </FormItem>
				<Row :gutter="15">
					<Col :span="12">
                        <FormItem label="系统账号">
                            <Input v-model="studentForm.userName" placeholder="请输入系统账号..."></Input>
                        </FormItem>
					</Col>
					<Col :span="12">
						<FormItem label="学生姓名">
							<Input v-model="studentForm.name" placeholder="请输入管理员姓名..."></Input>
						</FormItem>
					</Col>
				</Row>
			    <Row :gutter="15">
					<Col :span="12">
						<FormItem label="学生年龄">
							<Input v-model="studentForm.age" placeholder="请输入管理员年龄..."></Input>
						</FormItem>
					</Col>
					<Col :span="12">
						<FormItem label="学生性别">
							<RadioGroup v-model="studentForm.gender">
								<Radio label="男">男</Radio>
								<Radio label="女">女</Radio>
							</RadioGroup>
						</FormItem>
					</Col>
				</Row>
                <Row :gutter="15">
					<Col :span="12">
						<FormItem label="所属学院">
                            <Select v-model="studentForm.collegeId" placeholder="选择学院……">
                                <Option v-for="(item, index) in colleges" 
                                        :value="item.id" :key="index">{{ item.name }}</Option>
                            </Select>
                        </FormItem>
					</Col>
					<Col :span="12">
						<FormItem label="所属班级">
                            <Select v-model="studentForm.gradeId" placeholder="选择班级……">
                                <Option v-for="(item, index) in grades" 
                                        :value="item.id" :key="index">{{ item.name }}</Option>
                            </Select>
                        </FormItem>
					</Col>
				</Row>
			</Form>
		</Modal>

		<Modal v-model="showUpdFlag"
			title="信息编辑" ok-text="提交" cancel-text="取消" @on-ok="updInfo()">
			<Form :label-width="80" :model="studentForm">
				<FormItem label="所属学院">
					<Select v-model="studentForm.collegeId" placeholder="选择学院……">
                        <Option v-for="(item, index) in colleges" 
                                :value="item.id" :key="index">{{ item.name }}</Option>
                    </Select>
				</FormItem>
				<FormItem label="所属班级">
					<Select v-model="studentForm.gradeId" placeholder="选择班级……">
                        <Option v-for="(item, index) in grades" 
                                :value="item.id" :key="index">{{ item.name }}</Option>
                    </Select>
				</FormItem>
			</Form>
		</Modal>
    </div>
</template>

<script>
import {
    getAllColleges,
    getAllGrades,
    getPageStudents,
    addStudents,
    updStudents,
    delStudents,
} from '../../api/index.js';
export default{
		
    data(){
        return {
            colleges: [],
            grades: [],
            pageInfos: [],
            pageIndex: 1,
            pageSize: 10,
            pageTotal: 0,
            totalInfo: 0,
            loading: true,
            showAddFlag: false,
            showUpdFlag: false,
            qryForm: {
                stuName: "", 
				collegeId: "", 
				gradeId: ""
            },
            studentForm: {
                id: "",
                userName: "",
				name: "",
				age: "",
				gender: "",
				collegeId: "",
				gradeId: "",
            },
            columns: [
                {title: '序号', type: 'index', width: 70, align: 'center'},
                {title: '学生学号', key: 'id', align: 'center'},
                {title: '系统账号', key: 'userName', align: 'center'},
                {title: '姓名', key: 'name', align: 'center'},
                {title: '性别', key: 'gender', align: 'center'},
                {title: '年龄', key: 'age', align: 'center'},
                {title: '所属学院', key: 'collegeName', align: 'center'},
                {title: '所属班级', key: 'gradeName', align: 'center'},
                {title: '学生状态', slot: 'status', align: 'center'},
                {title: '操作', slot: 'action', align: 'center'}
            ]
        }
    },
    methods: {
        getPageInfo(pageIndex, pageSize) {
			
            getPageStudents(pageIndex, pageSize, 
                    this.qryForm.stuName, this.qryForm.collegeId, this.qryForm.gradeId).then(resp => {
                
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
        showAddWin(){

            this.studentForm = {
                id: "",
                userName: "",
				name: "",
				age: "",
				gender: "",
				collegeId: "",
				gradeId: "",
            };
            this.showAddFlag = true;
        },
        showUpdWin(row) {
			
            this.studentForm = row;
            this.showUpdFlag = true;
        },
        addInfo() {
			
            addStudents(this.studentForm).then(resp => {
                
                if(resp.code == 0){
					this.$Notice.success({
						duration: 3,
						title: resp.msg
					});
					
					this.getPageInfo(1, this.pageSize);
					this.showAddFlag = false;
				}else{
					
					this.$Notice.warning({
						duration: 3,
						title: resp.msg
					});
					this.showAddFlag = true;
				}
            });
        },
        updInfo() {
        
            updStudents(this.studentForm).then(resp => {
        
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
                    delStudents(id).then(resp =>{
                        
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
        
        getAllColleges().then(resp =>{

            this.colleges = resp.data;
        });
        getAllGrades().then(resp =>{

            this.grades = resp.data;
        });
        this.getPageInfo(1, this.pageSize);
    }
}
</script>