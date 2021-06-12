<template>
  <div class="container font-neodgm mt-5 p-0" id="bigbox">
    <div id="topbar" class="mb-3 mx-0 d-flex">
      <p style="color: white" class="text-start ps-2">MEMOVIES Sign Up</p>
      <span><img src="@/assets/signup.png" width="30px" class="ms-2"></span>
    </div>
    <div class="d-flex flex-column align-items-center">
      <h1 style="color:black;">회원 가입</h1>
      <form @submit.prevent="signup">
        <div class="m-3">
          <label for="username" style="color:black;">ID: </label>
          <input type="text" id="username" v-model="username" class="ms-2" style="width:440px;">
        </div>
        <div class="m-3">
          <label for="password" style="color:black;">비밀번호: </label>
          <input type="password" id="password" v-model="password" class="ms-2" style="width:400px;">
        </div>
        <div class="m-3">
          <label for="passwordConfirmation" style="color:black;">비밀번호 확인: </label>
          <input type="password" id="passwordConfirmation" v-model="passwordConfirmation" class="ms-2" style="width:370px;">
        </div>
        <button class="mb-2" style="margin-left:200px;">회원 가입</button>
      </form>
    </div>
  </div>
</template>

<script>
import axios from 'axios'
export default {
  name:'Signup',
  data(){
    return{
      username:'',
      password:'',
      passwordConfirmation:'',
    }
  },
  methods:{
    signup(){
      axios({
        url:'http://127.0.0.1:8000/memovies/accounts/signup/',
        method:'post',
        data:{
          username:this.username,
          password: this.password,
          passwordConfirmation: this.passwordConfirmation,
        }
      })
        .then(res=>{
          console.log(res)
          this.$router.push({ name:'Login' })
        })
        .catch(err=>{
          console.log(err)
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
</style>