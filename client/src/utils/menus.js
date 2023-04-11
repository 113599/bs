import {getLoginUser} from "../api";

export const adminMenus = {
    path: '/home',
    name: 'home',
    component: require("../views/home.vue").default,
    children: [
        {
            path: '/welcome',
            name: '系统首页',
            icon: "fa fa-home",
            component: require("../views/pages/welcome.vue").default
        },
        {
            path: '/notices',
            name: '系统公告管理',
            icon: "fa fa-bullhorn",
            component: require("../views/pages/notices.vue").default
        },
        {
            path: '/colleges',
            name: '学院信息管理',
            icon: "fa fa-building",
            component: require("../views/pages/colleges.vue").default
        },
        {
            path: '/grades',
            name: '班级信息管理',
            icon: "fa fa-language",
            component: require("../views/pages/grades.vue").default
        },
        {
            path: '/projects',
            name: '课程信息管理',
            icon: "fa fa-map-o",
            component: require("../views/pages/projects.vue").default
        },
        {
            path: '/teachers',
            name: '教师信息管理',
            icon: "fa fa-id-card-o",
            component: require("../views/pages/teachers.vue").default
        },
        {
            path: '/students',
            name: '学生信息管理',
            icon: "fa fa-group",
            component: require("../views/pages/students.vue").default
        },
        {
            path: '/checks',
            name: '学生考勤记录',
            icon: "fa fa-hourglass-half",
            component: require("../views/pages/checks.vue").default
        },
        {
            path: '/leaves',
            name: '学生请假记录',
            icon: "fa fa-calculator",
            component: require("../views/pages/leaves.vue").default
        }
    ]
}

export const teacherMenus = {
    path: '/home',
    name: 'home',
    component: require("../views/home.vue").default,
    children: [
        {
            path: '/welcome',
            name: '系统首页',
            icon: "fa fa-home",
            component: require("../views/pages/welcome.vue").default
        },
        {
            path: '/works',
            name: '我的工作安排',
            icon: "fa fa-desktop",
            component: require("../views/pages/works.vue").default
        },
        {
            path: '/checks',
            name: '学生考勤处理',
            icon: "fa fa-hourglass-half",
            component: require("../views/pages/checks.vue").default
        },
        {
            path: '/leaves',
            name: '学生请假处理',
            icon: "fa fa-calculator",
            component: require("../views/pages/leaves.vue").default
        }
    ]
}

export default function initMenu(router, store){

    let token = null;
	if(store.state.token){

		token = store.state.token;
	}else{

		token = sessionStorage.getItem("token");
		store.state.token = sessionStorage.getItem("token");
	}

	getLoginUser(token).then(resp =>{

		if(resp.data.type == 0){
			router.addRoute(adminMenus);
			store.commit("setMenus", adminMenus);
		}
	
		if(resp.data.type == 1){
			router.addRoute(teacherMenus);
			store.commit("setMenus", teacherMenus);
		}

        router.push('/welcome');
	});
}