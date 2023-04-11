<template>
	<div class="fater-body-show">
        <Card>
            <template #title>
				信息查询
			</template>
			<div>
				<Form :model="qryForm" inline>
					<FormItem v-if="userInfo.type == 0">
						<Input type="text" v-model="qryForm.studentName" placeholder="学生姓名……"></Input>
					</FormItem>
                    <FormItem>
                        <Select style="width: 200px" v-model="qryForm.collegeId" placeholder="选择学院……">
                            <Option value="">查看全部</Option>
                            <Option v-for="(item, index) in colleges" 
                                    :value="item.gradeId" :key="index">{{ item.gradeName }}</Option>
                        </Select>
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
			<div>
				<Table border :columns="columns" :loading="loading" :data="pageInfos">
                    <template #status="{ row }">
						<Tag v-if="row.status==0" type="border" color="primary">待审核</Tag>
						<Tag v-if="row.status==1" type="border" color="warning">已同意</Tag>
						<Tag v-if="row.status==2" type="border" color="warning">已拒绝</Tag>
						<Tag v-if="row.status==3" type="border" color="warning">已销假</Tag>
					</template>
                    <template #teacher="{ row }">
                        <Button v-if="row.status==0" disabled size="small" ghost type="info">查看详情</Button>
                        <Poptip v-else placement="top-start"
                            transfer="true"
                            word-wrap="true" trigger="hover" width="280">
                            <Button size="small" ghost type="info">信息查看</Button>
                            <template #content>
                                <table class="fater-detail-panle">
                                    <tr>
                                        <td>教师工号</td>
                                        <td>{{row.teacherId}}</td>
                                    </tr>
                                    <tr>
                                        <td>教师姓名</td>
                                        <td>{{row.teacherName}}</td>
                                    </tr>
                                    <tr>
                                        <td>联系方式</td>
                                        <td>{{row.teacherPhone}}</td>
                                    </tr>
                                </table>
                            </template>
                        </Poptip>
					</template>
                    <template #reason="{ row }">
                        <Poptip placement="top-start"
                            transfer="true"
                            word-wrap="true" trigger="hover" width="280">
                            <Button size="small" ghost type="info">查看详情</Button>
                            <template #content>
                                <div style="padding: 10px 15px;">{{ row.reason }}</div>
                            </template>
                        </Poptip>
					</template>
                    <template #reply="{ row }">
                        <Button v-if="row.status==0" disabled size="small" ghost type="info">查看详情</Button>
                        <Poptip v-if="row.status==1" placement="top-start"
                            transfer="true"
                            word-wrap="true" trigger="hover" width="280">
                            <Button size="small" ghost type="info">查看详情</Button>
                            <template #content>
                                <div style="padding: 10px 15px;">班级主任已同意, 学生休假中</div>
                            </template>
                        </Poptip>
                        <Poptip v-if="row.status==2" placement="top-start"
                            transfer="true"
                            word-wrap="true" trigger="hover" width="280">
                            <Button size="small" ghost type="info">查看详情</Button>
                            <template #content>
                                <div style="padding: 10px 15px;">请假申请被班级主任拒绝, 拒绝原因是 {{ row.replyComm }}</div>
                            </template>
                        </Poptip>
                        <Poptip v-if="row.status==3" placement="top-start"
                            transfer="true"
                            word-wrap="true" trigger="hover" width="280">
                            <Button size="small" ghost type="info">查看详情</Button>
                            <template #content>
                                <div style="padding: 10px 15px;">请假处理完毕, 学生已返校上课</div>
                            </template>
                        </Poptip>
					</template>
					<template #action="{ row }">
						<Button v-if="row.isAdmin && row.status==0"
                                size="small" type="info" @click="showUpdWin(row)">请假处理</Button>
						<Button v-else size="small" type="info" disabled>请假处理</Button>
					</template>
				</Table>
				<Page style="margin-top: 15px;" v-if="pageTotal > 1" :current="pageIndex"
					@on-change="handleCurrentChange" :total="totalInfo" show-total/>
			</div>
		</Card>

        <Modal v-model="showUpdFlag"
			title="请假处理" ok-text="提交" cancel-text="取消" @on-ok="updInfo()">
			<Form :label-width="80" :model="leaveForm">
				<FormItem label="处理结果">
                    <RadioGroup v-model="leaveForm.status">
                        <Radio label="1">同意</Radio>
                        <Radio label="2">拒绝</Radio>
                    </RadioGroup>
				</FormItem>
				<FormItem label="处理说明">
					<Input v-model="leaveForm.replyComm" type="textarea" rows="5" placeholder="请输入请假处理说明..."></Input>
				</FormItem>
			</Form>
		</Modal>
    </div>
</template>

<script>
import {
    getLoginUser,
    getAllColleges,
    getAllGrades,
    getPageLeaves,
    updLeave,
} from '../../api/index.js';
export default{
		
    data(){
        return {
            userInfo: {},
            colleges: [],
            grades: [],
            pageInfos: [],
            pageIndex: 1,
            pageSize: 10,
            pageTotal: 0,
            totalInfo: 0,
            loading: true,
            showUpdFlag: false,
            qryForm: {
                collegeId: "", 
                gradeId: "", 
                teacherId: "", 
                studentId: "", 
                studentName: ""
            },
            leaveForm: {
                id: "",
                teacherId: "",
				stuId: "",
				replyComm: "",
				status: "",
            },
            columns: []
        }
    },
    methods: {

        getPageInfo(pageIndex, pageSize) {
			
            getPageLeaves(pageIndex, pageSize, 
                    this.qryForm.collegeId, this.qryForm.gradeId, 
                    this.qryForm.teacherId, this.qryForm.studentId, this.qryForm.studentName).then(resp => {
                
                this.pageInfos = resp.data.data;
                this.pageIndex = resp.data.pageIndex;
                this.pageSize = resp.data.pageSize;
                this.pageTotal = resp.data.pageTotal;
                this.totalInfo = resp.data.count;
        
                this.loading = false;
            });
        },
        showUpdWin(row) {
			
            this.leaveForm.id = row.id;
            this.leaveForm.stuId = row.studentId;
            this.leaveForm.replyComm = "";
            this.leaveForm.status = "1";
            this.showUpdFlag = true;
        },
        handleCurrentChange(pageIndex) {
        
            this.getPageInfo(pageIndex, this.pageSize);
        },	
        updInfo() {

            console.log(this.leaveForm);
        
            updLeave(this.leaveForm).then(resp => {
        
                this.$Notice.success({
					duration: 3,
					title: resp.msg
				});
				
				this.getPageInfo(1, this.pageSize);
				this.showUpdFlag = false;
            });
        },
    },
    mounted(){
        
        getLoginUser(this.$store.state.token).then(resp =>{

            this.userInfo = resp.data;

            if(resp.data.type == 0){

                this.columns = [
                    {title: '序号', type: 'index', width: 70, align: 'center'},
                    {title: '学生学号', key: 'studentId', align: 'center'},
                    {title: '学生姓名', key: 'studentName', align: 'center'},
                    {title: '所属学院', key: 'collegeName', align: 'center'},
                    {title: '所属班级', key: 'gradeName', align: 'center'},
                    {title: '请假时间', key: 'createTime', align: 'center'},
                    {title: '处理教师', slot: 'teacher', align: 'center'},
                    {title: '请假理由', slot: 'reason', align: 'center'},
                    {title: '处理结果', slot: 'reply', align: 'center'},
                    {title: '处理状态', slot: 'status', align: 'center'},
                ];
            }else if(resp.data.type == 1){

                this.qryForm.teacherId = resp.data.id;
                this.leaveForm.teacherId = resp.data.id;
                this.columns = [
                    {title: '序号', type: 'index', width: 70, align: 'center'},
                    {title: '学生学号', key: 'studentId', align: 'center'},
                    {title: '学生姓名', key: 'studentName', align: 'center'},
                    {title: '所属学院', key: 'collegeName', align: 'center'},
                    {title: '所属班级', key: 'gradeName', align: 'center'},
                    {title: '请假时间', key: 'createTime', align: 'center'},
                    {title: '请假理由', slot: 'reason', align: 'center'},
                    {title: '处理结果', slot: 'reply', align: 'center'},
                    {title: '处理状态', slot: 'status', align: 'center'},
                    {title: '请假处理', slot: 'action', align: 'center'},
                ];
            }

            getAllColleges().then(res =>{

                this.colleges = res.data;
            });
            getAllGrades().then(res =>{

                this.grades = res.data;
            });

            this.getPageInfo(1, this.pageSize);
        });
    }
}
</script>