<template>
    <h1>Register</h1>
        <form @submit.prevent="register">
        <div>
            <label for="username">Username</label>
            <input type="text" id="username" v-model="username" required />
        </div>
        <div>
            <label for="email">Email</label>
            <input type="email" id="email" v-model="email" required />
        </div>
        <div>
            <label for="password">Password</label>
            <input type="password" id="password" v-model="password" required />
        </div>
        <button type="submit">Register</button>
    </form>
    <div>
        <RouterLink to="/">Home</RouterLink>
    </div>
    <div>
        <RouterLink to="/login">Login</RouterLink>
    </div>
</template>

<script>
export default {
    data() {
        return {
            username:"",
            email:"",
            password:""
        }
    },
    methods: {
        async register() {
            const data = {
                username:this.username,
                email:this.email,
                password:this.password
            }
            try {
              const response = await fetch('http://127.0.0.1:5050/register', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify(data)
                });

                if (!response.ok) {
                    throw new Error('Sign Up failed!');
                }

                const responseData = await response.json();
                alert(responseData.message);

                this.$router.push('/login');
            } catch (error) {
                alert(error.message || 'Register failed!');
            }
        }
    }
}
</script>