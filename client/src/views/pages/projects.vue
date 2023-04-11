<template>
	<div class="fater-body-show">
        <Card>
            <template #title>
				信息查询
			</template>
			<div>
				<Form :model="qryForm" inline>
					<FormItem>
						<Input type="text" v-model="qryForm.name" placeholder="课程名称……"></Input>
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

        <Modal v-model="showAddFlag"
			title="信息编辑" ok-text="提交" cancel-text="取消" @on-ok="addInfo()">
			<Form :label-width="80" :model="projectForm">
				<FormItem label="课程名称">
					<Input v-model="projectForm.name" placeholder="请输入课程名称..."></Input>
				</FormItem>
			</Form>
		</Modal>

        <Modal v-model="showUpdFlag"
			title="信息编辑" ok-text="提交" cancel-text="取消" @on-ok="updInfo()">
			<Form :label-width="80" :model="projectForm">
				<FormItem label="课程名称">
					<Input v-model="projectForm.name" placeholder="请输入课程名称..."></Input>
				</FormItem>
			</Form>
		</Modal>
    </div>
</template>

<script>
import {
    getPageProjects,
    addProjects,
    updProjects,
    delProjects,
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
            },
            projectForm: {
                id: "",
                name: ""
            },
            columns: [
                {title: '序号', type: 'index', width: 70, align: 'center'},
                {title: '课程名称', key: 'name', align: 'center'},
                {title: '添加时间', key: 'createTime', align: 'center'},
                {title: '操作', slot: 'action', align: 'center'}
            ]
        }
    },
    methods: {

        getPageInfo(pageIndex, pageSize) {
			
            getPageProjects(pageIndex, pageSize, 
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
        showAddWin(){

            this.projectForm = {
                name: ""
            };
            this.showAddFlag = true;
        },
        showUpdWin(row) {
			
            this.projectForm = row;
            this.showUpdFlag = true;
        },
        addInfo() {
			
            addProjects(this.projectForm).then(resp => {
                
                this.$Notice.success({
                    duration: 3,
                    title: resp.msg
                });
                
                this.getPageInfo(1, this.pageSize);
                
                this.showAddFlag = false;
            });
        },
        updInfo() {
        
            updProjects(this.projectForm).then(resp => {
        
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
                    delProjects(id).then(resp =>{
                        
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