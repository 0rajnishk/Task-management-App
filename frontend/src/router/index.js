import { createRouter, createWebHistory } from 'vue-router'
import HelloWorldVue from '../components/HelloWorld.vue'
import HomeVue from '../components/Home.vue'
import LoginVue from '../components/Login.vue'
import RegisterVue from '../components/Register.vue'

const router = createRouter({
    history: createWebHistory(import.meta.env.BASE_URL),
    routes:[
        {
            path:'/hello',
            name:'hello',
            component: HelloWorldVue
        },
        {
            path: '/',
            name: 'home',
            component: HomeVue
        },
        {
            path: '/login',
            name: 'login',
            component: LoginVue
        },
        {
            path: '/register',
            name: 'register',
            component: RegisterVue
        }
    ]
})

export default router