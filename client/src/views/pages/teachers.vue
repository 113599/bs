<template>
	<div class="fater-body-show">
        <Card>
            <template #title>
				信息查询
			</template>
			<div>
				<Form :model="qryForm" inline>
					<FormItem>
						<Input type="text" v-model="qryForm.name" placeholder="教师姓名……"></Input>
					</FormItem>
					<FormItem>
                        <Select style="width: 200px" v-model="qryForm.record" placeholder="教师学历……">
                            <Option value="">查看全部</Option>
                            <Option v-for="(item, index) in records" 
                                    :value="item" :key="index">{{ item }}</Option>
                        </Select>
					</FormItem>
					<FormItem>
						<Input type="text" v-model="qryForm.phone" placeholder="联系电话……"></Input>
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
				</Table>
				<Page style="margin-top: 15px;" v-if="pageTotal > 1" :current="pageIndex"
					@on-change="handleCurrentChange" :total="totalInfo" show-total/>
			</div>
		</Card>

        <Modal width="800" v-model="showAddFlag"
			title="信息编辑" ok-text="提交" cancel-text="取消" @on-ok="addInfo()">
			<Form :label-width="80" :model="teacherForm">
                <FormItem label="教师工号">
                    <Input v-model="teacherForm.id" placeholder="请输入教师工号..."></Input>
                </FormItem>
				<Row :gutter="15">
					<Col :span="12">
                        <FormItem label="系统账号">
                            <Input v-model="teacherForm.userName" placeholder="请输入系统账号..."></Input>
                        </FormItem>
					</Col>
					<Col :span="12">
						<FormItem label="教师姓名">
							<Input v-model="teacherForm.name" placeholder="请输入教师姓名..."></Input>
						</FormItem>
					</Col>
				</Row>
			    <Row :gutter="15">
					<Col :span="12">
						<FormItem label="教师年龄">
							<Input v-model="teacherForm.age" placeholder="请输入教师年龄..."></Input>
						</FormItem>
					</Col>
					<Col :span="12">
						<FormItem label="教师性别">
							<RadioGroup v-model="teacherForm.gender">
								<Radio label="男">男</Radio>
								<Radio label="女">女</Radio>
							</RadioGroup>
						</FormItem>
					</Col>
				</Row>
                <Row :gutter="15">
					<Col :span="12">
						<FormItem label="教师学历">
                            <Select v-model="teacherForm.record" placeholder="选择教师学历……">
                                <Option v-for="(item, index) in records" 
                                    :value="item" :key="index">{{ item }}</Option>
                            </Select>
                        </FormItem>
					</Col>
					<Col :span="12">
						<FormItem label="联系电话">
							<Input v-model="teacherForm.phone" placeholder="请输入教师联系电话..."></Input>
						</FormItem>
					</Col>
				</Row>
			</Form>
		</Modal>

        <Modal v-model="showUpdFlag"
			title="信息编辑" ok-text="提交" cancel-text="取消" @on-ok="updInfo()">
			<Form :label-width="80" :model="teacherForm">
				<FormItem label="教师学历">
                    <Select v-model="teacherForm.record" placeholder="选择教师学历……">
                        <Option v-for="(item, index) in records" 
                            :value="item" :key="index">{{ item }}</Option>
                    </Select>
                </FormItem>
				<FormItem label="联系电话">
                    <Input v-model="teacherForm.phone" placeholder="请输入教师联系电话..."></Input>
                </FormItem>
			</Form>
		</Modal>
    </div>
</template>

<script>

import {
    getPageTeachers,
    addTeachers,
    updTeachers,
    delTeachers
} from '../../api/index.js';

export default{
		
    data(){
        return {
            pageInfos: [],
            pageIndex: 1,
            pageSize: 10,
            pageTotal: 0,
            totalInfo: 0,
            loading: true,
            showAddFlag: false,
            showUpdFlag: false,
            qryForm: {
                name: "", 
				record: "", 
				phone: ""
            },
            teacherForm: {
                id: "",
                userName: "",
				name: "",
				age: "",
				gender: "",
				record: "",
				phone: "",
            },
            records: ['专科', '本科', '研究生', '其他'],
            columns: [
                {title: '序号', type: 'index', width: 70, align: 'center'},
                {title: '教师工号', key: 'id', align: 'center'},
                {title: '系统账号', key: 'userName', align: 'center'},
                {title: '教师姓名', key: 'name', align: 'center'},
                {title: '教师性别', key: 'gender', align: 'center'},
                {title: '教师年龄', key: 'age', align: 'center'},
                {title: '联系电话', key: 'phone', align: 'center'},
                {title: '教师学历', key: 'record', align: 'center'},
                {title: '操作', slot: 'action', align: 'center'}
            ]
        }
    },
    methods: {

        getPageInfo(pageIndex, pageSize) {
			
            getPageTeachers(pageIndex, pageSize, 
                    this.qryForm.name, this.qryForm.record, this.qryForm.phone).then(resp => {
                
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

            this.teacherForm = {
                id: "",
                userName: "",
				name: "",
				age: "",
				gender: "",
				record: "",
				phone: "",
            };
            this.showAddFlag = true;
        },
        showUpdWin(row) {
			
            this.teacherForm = row;
            this.showUpdFlag = true;
        },
        addInfo() {
			
            addTeachers(this.teacherForm).then(resp => {
                
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
        
            updTeachers(this.teacherForm).then(resp => {
        
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
                    delTeachers(id).then(resp =>{
                        
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

        this.getPageInfo(1, this.pageSize);
    }
}
</script>