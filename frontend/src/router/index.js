import { createRouter, createWebHistory } from 'vue-router'
import HelloWorldVue from '../components/HelloWorld.vue'
import Home from '../views/HomeView.vue'
import Login from '../views/LoginView.vue'
import Signup from '../views/SignupView.vue'



const router = createRouter({
    history: createWebHistory(import.meta.env.BASE_URL),
    routes: [
        {
            path: '/',
            name: 'home',
            component: Home
        },
        // {
        //     path: '/home',
        //     name: 'home',
        //     component: Home
        // },
        {
            path: '/hello',
            name: 'hello',
            component: HelloWorldVue
        },
        {
            path: '/signup',
            name: 'signup',
            component: Signup
        },
        {
            path: '/Login',
            name: 'login',
            component: Login
        }

    ]
})

export default router