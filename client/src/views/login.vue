<template>
    <div class="login-body">
        <div class="login-win">
            <div class="login-form">
                <Form ref="loginForm" :rules="rules" :model="loginForm" :label-width="90">
                    <FormItem>
                        <Input v-model="loginForm.userName" placeholder="请输入您的账号..."></Input>
                    </FormItem>
                    <FormItem style="margin-top: 45px;">
                        <Input type="password" v-model="loginForm.passWord" placeholder="请输入您的密码..."></Input>
                    </FormItem>
                    <FormItem style="margin-top: 50px;">
                        <Button style="width:410px;" 
                            @click="submitForm('loginForm')"  class="login-btn" type="primary">用户登陆</Button>
                    </FormItem>
                </Form>
            </div>
        </div>
    </div>
</template>

<style>
.login-body{
    background-color: #2d8cf0;
    position: fixed;
    left: 0;
    top: 0;
    bottom: 0;
    right: 0;
}
.login-win{
    position: absolute;
    top: 48%;
    left: 50%;
    transform: translate(-50%, -50%);
    width: 850px;
    height: 500px;
    padding: 15px;
    border-radius: 8px;
    border: 2px solid #dcdee2;
    background-image: url('../assets/1.jpg');
    background-size: cover;
}
.login-form{
    position: absolute;
    left: 17%;
    top: 50%;
    width: 500px;
}
</style>

<script>
import initMenu from "../utils/menus.js";
import { login } from '../api/index.js';
export default {
    data() {

        return {
            loginForm: {
                userName: '',
                passWord: '',
                type: 'client'
            },
            rules: {
                userName: [
                    { required: true, message: '用户账号必须输入', trigger: 'blur' }
                ],
                passWord: [
                    { required: true, message: '用户密码必须输入', trigger: 'blur' }
                ],
            }
        }
    },
    methods: {
        submitForm (formName) {
            this.$refs[formName].validate((valid) => {

                if (valid) {

                    console.log('开始登陆');

                    login(this.loginForm).then(res => {
                        
                        if(res.code == 0){

                            this.$store.commit('setToken', res.data.token);
                            sessionStorage.setItem("token", res.data.token);
                            initMenu(this.$router, this.$store);
                            this.$router.push('/welcome');
                        }else{

                            this.$Message.warning(res.msg);
                        }
                    });
                } else {

                    return false;
                }
            })
        }
    },
}
</script>
