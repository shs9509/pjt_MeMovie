<template>
  <div class="container font-neodgm mt-5 p-0" id="bigbox">
    <div id="topbar" class="mb-3 mx-0 d-flex">
      <p style="color: white" class="text-start ps-2">MEMOVIES Login</p>
      <span><img src="@/assets/login.png" width="30px"></span>
    </div>
    <div class="d-flex flex-column align-items-center">
      <h1 style="color:black;">로그인</h1>
      <form @submit.prevent ="login">
        <div class="my-3 black">
          <label for="username" class="black">ID:  </label>
          <input type="text" v-model="username" id="username" class="ms-2" style="width:440px;">
        </div>
        <div>
          <label for="password" class="black">비밀번호:  </label>
          <input type="password" v-model="password" id="password" class="ms-1" style="width:400px;">
        </div>
        <br>
        <button class="mb-2" style="margin-left:200px;">Login</button>
      </form>
    </div>
  </div>
</template>


<script>
import axios from 'axios'

export default {
  name:'Login',
  data(){
    return {
      username:'',
      password:'',
    }
  },
  methods:{
    login(){
      axios({
        url:'http://127.0.0.1:8000/memovies/accounts/login/',
        method:'post',
        data:{
          username:this.username,
          password:this.password,
        },
      })
        .then(res=>{
          localStorage.setItem('jwt', res.data.token)
          // console.log('login', localStorage)
          this.$emit('login',this.username)
          this.$router.push({ name:'Home' })
        })
        .catch(err=>{
          alert(JSON.stringify(err.data))
        })
    },
  },

}
</script>

<style>
#bigbox {
    background-color: lightgrey;
    border: 3px solid black;
  }

  #topbar{
    background-color:navy;
    height:30px
  }
.font{
    font-family: 'Noto Sans KR', sans-serif;
  }
.black{
  color:black;
}
</style>