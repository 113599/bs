<template>
    <Layout>
		<Menus :menuList="this.$store.state.menus.children"></Menus>
		<Layout>
			<Header class="fater-header">
				<Breadcrumb v-if="this.$router.currentRoute.value.path != '/welcome'" class="fater-header-nav">
					<BreadcrumbItem to="/welcome">首页</BreadcrumbItem>
					<BreadcrumbItem>{{ this.$router.currentRoute.value.name }}</BreadcrumbItem>
				</Breadcrumb>
				<Nav></Nav>
			</Header>
			<Content class="fater-layout-body">
				<router-view></router-view>
			</Content>
		</Layout>
	</Layout>
</template>

<style>

</style>

<script>
import Nav from "../components/nav.vue";
import Menus from "../components/menus.vue";

export default {
	components: {
		Nav,
		Menus
	}
}
</script>
