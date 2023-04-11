<template>
	<div class="fater-layout-left">
		<div class="fater-header-logo">学生考勤系统</div>
		<Sider>
			<Menu theme="light" active-name="系统首页">
				<MenuItem v-for="(item, index) in menuList" :key="index" :name="item.name" :to="item.path">
					<span :class="item.icon"></span>
					{{ item.name }}
				</MenuItem>
			</Menu>
		</Sider>
	</div>

</template>

<script>
export default{
    props: {
        menuList: []
    },
        
}
</script>

<style>
</style>
