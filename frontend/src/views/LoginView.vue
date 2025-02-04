<template>
    <h2>login page</h2>

    <form @submit.prevent="login">
        <div>
            <label for="email">Email</label>
            <input type="email" id="email" v-model="email" required />
        </div>
        <div>
            <label for="password">Password</label>
            <input type="password" id="password" v-model="password" required />
        </div>
        <button type="submit">login</button>
    </form>


    <div>
        <RouterLink to="/">home</RouterLink>
    </div>

    <div>
        <RouterLink to="/signup">signup</RouterLink>
    </div>


</template>


<script>
export default {
    data() {
        return {
            email: "",
            password: "",
        };
    },

    methods: {

        async login(){
            if (!this.email || !this.password) {
                alert("All fields are required!");
                return;
            }

            const data = {
                email: this.email,
                password: this.password
            };

            const response = await fetch("http://localhost:5000/login", {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(data)
                
            });
            const res = await response.json();

            localStorage.setItem("token", res.token)
            console.log(res)
            alert(res.token)

        }
    }

}
</script>