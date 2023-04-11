<template>
	<Header class="fater-header-user">
		<Dropdown @on-click="handleUser">
			<a href="javascript:void(0)">
				个人中心
				<Icon type="ios-arrow-down"></Icon>
			</a>
			<template #list>
				<DropdownMenu>
					<DropdownItem name="info">个人中心</DropdownItem>
					<DropdownItem name="pwd">修改密码</DropdownItem>
					<DropdownItem name="exit" divided>退出系统</DropdownItem>
				</DropdownMenu>
			</template>
		</Dropdown>

		<Modal v-model="showInfoFlag"
			title="信息编辑" ok-text="提交" cancel-text="取消" @on-ok="updInfo()">
			<Form :label-width="80" :model="infoForm">
				<FormItem label="用户账号">
					<Input v-model="infoForm.userName" placeholder="请输入用户账号..."></Input>
				</FormItem>
				<FormItem label="用户姓名">
					<Input v-model="infoForm.name" placeholder="请输入用户姓名..."></Input>
				</FormItem>
				<FormItem label="用户年龄">
					<Input v-model="infoForm.age" placeholder="请输入用户年龄..."></Input>
				</FormItem>
				<FormItem label="用户性别">
					<RadioGroup v-model="infoForm.gender">
						<Radio label="男">男</Radio>
						<Radio label="女">女</Radio>
					</RadioGroup>
				</FormItem>
			</Form>
		</Modal>

		<Modal v-model="showPwdFlag"
			title="信息编辑" ok-text="提交" cancel-text="取消" @on-ok="updPwd()">
			<Form :label-width="80" :model="pwdForm">
				<FormItem label="原始密码">
					<Input v-model="pwdForm.oldPwd" type="password" placeholder="请输入原始密码..."></Input>
				</FormItem>
				<FormItem label="修改密码">
					<Input v-model="pwdForm.newPwd" type="password" placeholder="请输入修改密码..."></Input>
				</FormItem>
				<FormItem label="确认密码">
					<Input v-model="pwdForm.rePwd" type="password" placeholder="请输入确认密码..."></Input>
				</FormItem>
			</Form>
		</Modal>
	</Header>
</template>

<style>
</style>

<script>
import {
	exit,
	getLoginUser,
	updSessionInfo,
	updSessionPwd,
} from "../api";

export default {

	data() {
		return {
			showInfoFlag: false,
			showPwdFlag: false,
			pwdForm: {
				token: this.$store.state.token,
				newPwd: "",
				rePwd: "",
				oldPwd: ""
			},
			infoForm: {
				token: this.$store.state.token,
				userName: "",
				name: "",
				gender: "",
				age: "",
			},
		}
	},
	methods: {
		showInfoWin(){

			getLoginUser(this.$store.state.token).then(resp =>{

				this.infoForm.id = resp.data.id;
				this.infoForm.userName = resp.data.userName;
				this.infoForm.name = resp.data.name;
				this.infoForm.gender = resp.data.gender;
				this.infoForm.age = resp.data.age;

				this.showInfoFlag = true;
			});
		},
		showPwdWin(){

			this.pwdForm = {
				token: this.$store.state.token,
				newPwd: "",
				rePwd: "",
				oldPwd: ""
			};
			this.showPwdFlag = true;
		},
		handleUser(name) {

			if (name == "info") {
					
				this.showInfoWin();
			} else if (name == "pwd") {
				
				this.showPwdWin();
			} else if (name == "exit") {
				
				this.$Modal.confirm({
					title: '系统提示',
					content: '即将退出系统, 是否继续?',
					onOk: () => {

						exit(this.$store.state.token).then(() => {
							this.$store.commit("clearToken");
							this.$store.commit("clearMenus");
							sessionStorage.clear();
							window.location.href="/";
						});
					},
            	});
			}
		},
		updInfo(){

			updSessionInfo(this.infoForm).then(resp =>{

				if(resp.code == 0){

					this.$Message.success({
						background: true,
						content: '用户信息修改完成'
					});
					this.showInfoFlag = false;
				}else{
					
					this.$Message.warning({
						background: true,
						content: resp.msg
					});
					this.showInfoFlag = true;
				}
			});
		},
		updPwd(){

			updSessionPwd(this.pwdForm).then(resp =>{

				if(resp.code == 0){

					this.$Message.success({
						background: true,
						content: '用户密码修改完成'
					});
					this.showPwdFlag = false;
				}else{
					
					this.$Message.warning({
						background: true,
						content: resp.msg
					});
					this.showPwdFlag = true;
				}
			});
		},
	},
}
</script>
