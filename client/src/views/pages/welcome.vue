<template>
	<div class="fater-body-show">
        <Row :gutter="15">
            <Col span="8">
                 <div class="fater-calendar-panel">
                    <Calendar cell-height="40"/>
                </div>
            </Col>
            <Col span="16">
                <Card>
                    <template #title>
                        系统信息
                    </template>
                    <div>
                        <div class="fater-sysinfo-panle">
                            <table>
                                <tr>
                                    <td>系统名称</td>
                                    <td>学生考勤管理系统 V1.0.0</td>
                                </tr>
                                <tr>
                                    <td>运行环境</td>
                                    <td>Python3.9.9 + NodeJS 16.13.0 + MySQL 8.0</td>
                                </tr>
                                <tr>
                                    <td>客户端开发</td>
                                    <td>Vue3.0 + Vue-Router + Vuex + IView</td>
                                </tr>
                                <tr>
                                    <td>服务端开发</td>
                                    <td>Django</td>
                                </tr>
                                <tr>
                                    <td>开发时间</td>
                                    <td>2023-02-15</td>
                                </tr>
                                <tr>
                                    <td>开发团队</td>
                                    <td>爱编程的小肥仔</td>
                                </tr>
                                <tr>
                                    <td>资源获取</td>
                                    <td>
                                        微信搜索 
                                        <span style="font-size: 18px;font-weight:bold;color:#2d8cf0;">编程苑</span> 
                                        小程序私聊
                                    </td>
                                </tr>
                            </table>
                        </div>
                    </div>
                </Card>
            </Col>
        </Row>

        <div class="fater-welcome-panle"></div>  
    </div>
</template>

<script>
</script>