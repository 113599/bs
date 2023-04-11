import axios from 'axios'
import qs from 'qs'

import { Notice } from "view-ui-plus";

const service = axios.create({
	baseURL: 'http://localhost:8000/api',
	timeout: 15000 
})

service.interceptors.request.use(config => {
	
	if(config.method === "post"){
		
		config.data = qs.stringify(config.data,  { indices: false });
	}
	
	return config;
}, error => {
	Promise.reject(error)
})

// respone拦截器
service.interceptors.response.use(
	success => {

		if (success.data.code == 0) {

			return success.data;

		}else if (success.data.code == 1){

			return success.data;
		} else {

			Notice.error({
				duration: 3,
				title: success.data.msg
			});
			return Promise.reject(success.data);
		}
	},
	error => {
		
		Notice.error({
			duration: 3,
			title: '系统异常，请求中断'
		});
		return Promise.reject(error);
	}
)

export default service