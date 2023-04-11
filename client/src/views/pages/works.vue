<template>
	<div class="fater-body-show">
        <Card>
			<template #title>
				工作安排
			</template>
			<div>
				<Table border :columns="columns" :data="works">
                    <template #job="{ row }">
						<Tag v-if="row.job==0" type="border" color="primary">授课教师</Tag>
						<Tag v-if="row.job==1" type="border" color="warning">班主任</Tag>
					</template>
                </Table>
            </div>
        </Card>
    </div>
</template>

<script>
import {
    getTeacherWork,
    getLoginUser
} from '../../api/index.js';
export default{
		
    data(){
        return {
            userInfo: {},
            works: [],
            columns: [
                {title: '序号', type: 'index', width: 70, align: 'center'},
                {title: '上课班级', key: 'gradeName', align: 'center'},
                {title: '负责课程', key: 'projectName', align: 'center'},
                {title: '工作职责', slot: 'job', align: 'center'}
            ]
        }
    },
    methods: {

    },
    mounted(){
        
        getLoginUser(this.$store.state.token).then(resp =>{

            this.userInfo = resp.data;

            getTeacherWork(resp.data.id).then(res =>{

                this.works = res.data;
            })
        });
    }
}
</script>