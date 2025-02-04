<template>
    <h1>Log In</h1>
        <form @submit.prevent="login">
        <div>
            <label for="credentials">Username or Email</label>
            <input type="text" id="credentials" v-model="credentials" required />
        </div>
        <div>
            <label for="password">Password</label>
            <input type="password" id="password" v-model="password" required />
        </div>
        <button type="submit">Login</button>
    </form>
    <div>
        <RouterLink to="/">Home</RouterLink>
    </div>
    <div>
        <RouterLink to="/register">Register</RouterLink>
    </div>
</template>

<script>
export default {
    data() {
        return {
            credentials:"",
            email:""
        }
    },
    methods: {
        async login() {
            const data = {
                credentials:this.credentials,
                password:this.password
            }
            try {
              const response = await fetch('http://127.0.0.1:5050/login', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify(data)
                });

                if (!response.ok) {
                    throw new Error('Log in failed!');
                }

                const responseData = await response.json();
                alert(responseData.message);

                this.$router.push('/home');
            } catch (error) {
                alert(error.message || 'Login failed!');
            }
        }
    }
}
</script>