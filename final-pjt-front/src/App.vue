<template>
  <div id="app" class="font-neodgm">
    <div class="account">
      <span v-if="isLogin" id="topnav">
        <router-link to="#" @click.native="logout">로그아웃</router-link>
      </span>
      <span v-else>
        <router-link :to="{ name:'Login' }">로그인</router-link> |
        <router-link :to="{ name:'Signup' }">회원 가입</router-link>
      </span>
    </div>
    <div id="nav">
      <router-link :to="{ name:'Home' }">미-무비</router-link> |
      <router-link :to="{ name:'Community'}">커뮤니티</router-link>|
      <router-link v-if="isLogin" :to="{ name: 'Profile', params: { userid: userid }}">프로필</router-link>|
      <router-link v-if="isLogin" :to="{ name: 'UserRecommend', params: { userid: userid }}">추천 영화</router-link>|
      <router-link :to="{ name: 'Recommend'}">그떄 그영화</router-link>
    </div>
    <div>
    </div>
    <router-view @login="login" :isLogin="isLogin" />
  </div>
</template>
<script>
import jwt_decode from "jwt-decode"

export default {
  name: 'App',
  data: function () {
    return {
      isLogin: false,
      userid:'',
    }
  },
  methods: {
    logout () {
      this.isLogin = false
      this.userid = ''
      localStorage.removeItem('jwt')
      this.$router.push({ name:'Home' })
    },
    login () {
      const token = localStorage.getItem('jwt')
      if (token) {
        this.isLogin = true
        this.userid = jwt_decode(token).user_id
      }
    },
  },
  created: function () {
    const token = localStorage.getItem('jwt')
    if (token) {
      this.isLogin = true
      this.userid = jwt_decode(token).user_id
    }
  },
}
</script>
<style>
@import url('https://fonts.googleapis.com/css2?family=Jua&family=Noto+Sans+KR&display=swap');
@import url('//cdn.jsdelivr.net/gh/Dalgona/neodgm-webfont@1.521/neodgm/style.css');
<link rel="stylesheet" href="//cdn.jsdelivr.net/gh/Dalgona/neodgm-webfont@1.521/neodgm/style.css">

#app {
  font-family: Avenir, Helvetica, Arial, sans-serif, Noto Sans K;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}

#nav {
  padding: 10px;
  text-align : start;
  background-color: navy;
  border-color: black 3px;
}

#nav a {
  font-weight: bold;
  color: white;
  text-decoration: none;
}

#nav a.router-link-exact-active {
  color: lightgray;
}

.font{
  font-family: 'Noto Sans KR', sans-serif;
}

.account {
  text-align: end;
  background-color: lightgray;
  border: 1px solid black;
}

#topnav a {
  text-decoration: none;
  color:black;
  padding-right:10px;
}

.font-neodgm { 
  font-family: 'NeoDunggeunmo'; 
}

#index{
  background-color: black;
}
</style>
