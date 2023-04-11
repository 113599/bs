import http from "../utils/http.js";


/** 系统接口 */
export function login(param){
	
	return http.post('/login/', param);
}
export function exit(token){
	
	return http.post('/exit/', {token: token});
}
export function getLoginUser(token){
	
	return http.get('/info/', {params: {token: token}});
}
export function updSessionInfo(param){
	
	return http.post('/info/', param);
}
export function updSessionPwd(param){
	
	return http.post('/pwd/', param);
}

/** 公告信息处理接口 */
export function getPageNotices(pageIndex, pageSize, title){

	return http.get('/notices/page/', 
        {params: {pageIndex: pageIndex, pageSize: pageSize, title: title}});
}
export function addNotices(params){

	return http.post('/notices/add/', params);
}
export function delNotices(id){

	return http.post('/notices/del/', {id: id});
}


/** 学院信息处理接口 */
export function getAllColleges(){

	return http.get('/colleges/all/');
}
export function getPageColleges(pageIndex, pageSize, name){

	return http.get('/colleges/page/', 
        {params: {pageIndex: pageIndex, pageSize: pageSize, name: name}});
}
export function addColleges(params){
	
	return http.post('/colleges/add/', params);
}
export function updColleges(params){
	
	return http.post('/colleges/upd/', params);
}
export function delColleges(id){
	
	return http.post('/colleges/del/', {id: id});
}

/** 班级信息处理接口 */
export function getAllGrades(){

	return http.get('/grades/all/');
}
export function getPageGrades(pageIndex, pageSize, name){

	return http.get('/grades/page/', 
        {params: {pageIndex: pageIndex, pageSize: pageSize, name: name}});
}
export function addGrades(params){
	
	return http.post('/grades/add/', params);
}
export function updGrades(params){
	
	return http.post('/grades/upd/', params);
}
export function delGrades(id){
	
	return http.post('/grades/del/', {id: id});
}

/** 课程信息处理接口 */
export function getAllProjects(){

	return http.get('/projects/all/');
}
export function getPageProjects(pageIndex, pageSize, name){

	return http.get('/projects/page/', 
        {params: {pageIndex: pageIndex, pageSize: pageSize, name: name}});
}
export function addProjects(params){
	
	return http.post('/projects/add/', params);
}
export function updProjects(params){
	
	return http.post('/projects/upd/', params);
}
export function delProjects(id){
	
	return http.post('/projects/del/', {id: id});
}

/** 学生信息处理接口 */
export function getPageStudents(pageIndex, pageSize, stuName, collegeId, gradeId){

	return http.get('/students/page/', 
        {params: {pageIndex: pageIndex, pageSize: pageSize, stuName: stuName, collegeId: collegeId, gradeId: gradeId}});
}
export function addStudents(params){
	
	return http.post('/students/add/', params);
}
export function updStudents(params){
	
	return http.post('/students/upd/', params);
}
export function delStudents(id){
	
	return http.post('/students/del/', {id: id});
}

/** 教师信息处理接口 */
export function getPageTeachers(pageIndex, pageSize, name, record, phone){

	return http.get('/teachers/page/', 
        {params: {pageIndex: pageIndex, pageSize: pageSize, name: name, record: record, phone: phone}});
}
export function addTeachers(params){
	
	return http.post('/teachers/add/', params);
}
export function updTeachers(params){
	
	return http.post('/teachers/upd/', params);
}
export function delTeachers(id){
	
	return http.post('/teachers/del/', {id: id});
}

/** 教师工作处理接口 */
export function getWorks(gradeId){

	return http.get('/works/worklist/', {params: {gradeId: gradeId}});
}
export function getTeacherWork(teacherId){

	return http.get('/works/teaworklist/', {params: {teacherId: teacherId}});
}
export function getSetWorks(gradeId){

	return http.get('/works/setworklist/', {params: {gradeId: gradeId}});
}
export function setWork(param){
	
	return http.post('/works/setwork/', param);
}


/** 学生考勤处理接口 */
export function getPageChecks(pageIndex, pageSize, gradeId, teacherId, teacherName){

	return http.get('/checks/page/', 
        {params: {pageIndex: pageIndex, pageSize: pageSize, 
					gradeId: gradeId, teacherId: teacherId, teacherName: teacherName}});
}
export function addCheck(param){
	
	return http.post('/checks/add/', param);
}
export function updCheck(param){
	
	return http.post('/checks/upd/', param);
}

/** 考勤记录处理接口 */
export function getCheckListByNo(checkNo){

	return http.get('/checklogs/referno/', {params: {checkNo: checkNo}});
}

/** 学生请假处理接口 */
export function getPageLeaves(pageIndex, pageSize, 
	collegeId, gradeId, teacherId, studentId, studentName){

	return http.get('/leaves/page/', 
        {params: {pageIndex: pageIndex, pageSize: pageSize, 
					collegeId: collegeId, gradeId: gradeId, teacherId: teacherId, 
					studentId: studentId, studentName: studentName}});
}
export function updLeave(param){
	
	return http.post('/leaves/upd/', param);
}


