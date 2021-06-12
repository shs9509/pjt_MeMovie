<template>
  <div class="container mt-5 p-0 font-neodgm" id="bigbox">
    <div id="topbar" class="mb-3 mx-0 d-flex">
      <p style="color: white" class="text-start ps-2">{{ username }}</p>
      <span><img src="@/assets/profile.png" width="20px" class="ms-2"></span>
    </div>
    <h1 style="color:black; text-align:center;">{{ username }}의 Profile</h1>
    <hr>
    <div class="d-flex flex-column align-items-center">
      <h4 style="">팔로워 : {{ followers }} | 팔로잉 : {{ followings }}</h4>
      <i v-if=" nowUser != username " @click="userFollow" class="fas fa-user-friends fa-2x my-2" :class="{followstatus : follow}"></i>
    </div>
    <hr>
    <div class="d-flex flex-column align-items-center">
      <h2 style="color:black;" class="mt-3">작성한 게시글</h2>
      <div>
        <ul v-for="review in reviews" :key="review.pk" :review="review">
          <ul class="p-0 fs-5 pe-4 mt-1">{{ review.fields.title }}</ul>
        </ul>
      </div>
    </div>
    <hr>
    <div class="d-flex flex-column align-items-center">
      <h2 style="color:black; ">댓글</h2>
      <div>
        <ul v-for="comment in comments" :key="comment.pk" :comment="comment">
          <ul class="p-0 fs-5 pe-4 mt-1">{{ comment.fields.content }}</ul>
        </ul>
      </div>
    </div>
    <hr>
    <div class="d-flex flex-column align-items-center">
      <h2 style="color:black; ">좋아요 누른 영화</h2>
      <div>
        <ul v-for="movie in likemovies" :key="movie.pk" :movie="movie">
          <ul class="p-0 fs-5 pe-4 mt-1">{{ movie.fields.movie_title }}</ul>
        </ul>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'
import jwt_decode from 'jwt-decode'
export default {
  name:'Profile',
  data(){
    return {
      reviews: {},
      comments: {},
      likemovies: {},
      followings: 0,
      followers: 0,
      follow: false,
      username: null,
      nowUser : '',
    }
  },
  props:{
    isLogin:{
      type:Boolean,
    }
  },
  created(){
    axios({
      url:'http://127.0.0.1:8000/memovies/accounts/profile/'+this.$route.params.userid,
      method:'get'
    })
      .then(res=>{
        // console.log(res.data)
        this.reviews = JSON.parse(res.data.review)
        this.comments = JSON.parse(res.data.comment)
        this.likemovies = JSON.parse(res.data.likemovies)
        this.followings = res.data.count_followings
        this.followers = res.data.count_followers
        this.username = res.data.username
        if (this.isLogin) {
          this.nowUser = jwt_decode(localStorage.getItem('jwt')).username
        }
      })
      .catch(err=>{
        console.log(err)
      })
  },
  methods:{
    userFollow () {
      axios({
        url:'http://127.0.0.1:8000/memovies/accounts/follow/'+this.$route.params.userid+'/',
        method: 'post',
        headers: {
          Authorization: `JWT ${localStorage.getItem('jwt')}`
        },
        data:{
          id: 1,
        }
      })
          .then(res => {
            // console.log(res.data)
            this.followers = res.data.count_followers
            this.followings = res.data.count_followings
            this.follow = res.data.follow
          })
          .catch(err => {
            console.log(err)
          })
    },
  }, 
}
</script>

<style>
  .followstatus{
    color: yellow;
  }

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
</style>