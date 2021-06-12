<template>
  <div class="font-neodgm">
    <div class="container mt-4 d-flex flex-column px-0" id="bigbox">
      <div id="topbar" class="mb-3 mx-0 d-flex">
        <p style="color: white" class="text-start ps-2">상세 보기</p>
        <span><img src="@/assets/find.png" width="30px"></span>
      </div>
      <div>
        <div class="d-flex px-3 mb-3">
          <img :src="imgUrl" height="600px">
          <div class="d-flex flex-column align-items-center">
            <h1 style="color: black;"> {{ movie.movie_title }}</h1>
            <!-- <button class="btn"><i :class="{likeStatus:like}" class="far fa-heart fa-2x" @click="likeMovie"></i></button> -->
            <button class="btn"><img v-show="like" src="@/assets/full_folder.png" style="width:50px;height:50px" @click="likeMovie"></button>
            <button class="btn"><img v-show="!like" src="@/assets/empty_folder.png" style="width:40px;height:40px" @click="likeMovie"></button>
            <!-- <button class="btn"><img :src="like ? likeIcon : UnlikeIcon" @click="likeMovie"></button> -->
            <div class="m-3" id="overview" >
              <h4 style="color:black; text-align:center;">줄거리</h4>
              <p>{{ movie.overview }}</p>
            </div>
            <p>개봉일 : {{ movie.release_date }}</p>
            <p> 사이트 평점: {{ movie.vote_average }}</p>
          </div>
        </div>
      </div>
    </div> 
    <div class="mt-4 container py-2 d-flex justify-content-center" id="comment">
      <form @submit.prevent="movieComment">
        <label for="rate">평점: </label>
        <select v-model="rate"  @change="getRate">
          <option value="default">평점 선택</option>
          <option v-for="n in raterange" :key="n.id">{{ n }}</option>
        </select>
        <label for="content" class="ms-2">한줄평: </label>
        <input type="text" v-model="comment" style="width:700px">
        <button class="mx-2" style="background-color:navy; color:white;">평점등록</button>
      </form>
    </div>
    <div class="container mt-4 d-flex flex-column align-items-center">
      <h4 style="color:white" class="my-3">관객 한 줄평</h4>
      <table style="text-align:center;" class="fs-6">
        <thead>
          <tr>
            <th>평점</th>
            <th>후기</th>
            <th>수정</th>
            <th>삭제</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="comment in comments" :key="comment.id" :comment="comment">
            <td>{{ comment.rate }} </td>
            <td>{{ comment.content }}</td>
            <td>
              <b-button v-b-modal.modal-1 variant="none"><img src="@/assets/update.png" width="30px" v-if="comment.user === userid"></b-button>
              <b-modal id="modal-1" title="댓글수정">
                <form @submit.prevent="UpdateComment(comment)">
                  <label for="rate">평점:</label>
                  <select @change="getNewRate" :newRate="newRate">
                    <option value="default" selected>{{comment.rate}}</option>
                    <option v-for="n in raterange" :key="n.id">{{ n }}</option>
                  </select>
                  <input type="text" v-model="newComment" :placeholder="comment.content">
                  <button class="btn btn-primary btn-sm">수정하기</button>
                </form>
              </b-modal>
            </td>
            <td>
              <button class="btn btn-none" @click="commentDelete(comment.id)" v-if="comment.user === userid"><img src="@/assets/delete.png" width="30px"></button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
      <!-- 댓글 만들기 -->
  </div>
</template>

<script>
import jwt_decode from 'jwt-decode'
import axios from 'axios'
export default {
  name:'MovieDetail',
  data(){
    return {
      movie :[],
      comment:'',
      rate:5,
      comments:[],
      like:false,
      newComment:'',
      newRate:5,
      userid : '',
      raterange:[1,2,3,4,5,6,7,8,9,10],
    }
  },
  props:{
    isLogin:{
      type:Boolean,
    }
  },
  created(){
    axios({
      url:'http://127.0.0.1:8000/memovies/movies/'+this.$route.params.movieid,
      method:'get',
    })
      .then(res=>{
        console.log(res)
        this.movie = res.data.movie
        this.comments = res.data.comments
        this.like = res.data.like
        if (this.isLogin) {
          this.userid = jwt_decode(localStorage.getItem('jwt')).user_id
        }
      })
  },
  methods:{
    getMovie(){
      axios({
        url:'http://127.0.0.1:8000/memovies/movies/'+this.$route.params.movieid,
        method:'get',
      })
        .then(res=>{
          // console.log(res)
          // this.movie = res.data.movie
          this.comments = res.data.comments
        })
    },
    movieComment(){
      axios({
        url:'http://127.0.0.1:8000/memovies/movies/'+this.$route.params.movieid+'/comments/',
        method:'post',
        data:{
          content: this.comment,
          rate: this.rate,
          user: this.userid,
        },
        headers:{
          Authorization: `JWT ${localStorage.getItem('jwt')}`
        }
      })
        .then(res=>{
          console.log(res, '들어오는 데이터 제발 좀 보여라...')
          this.comment = ''
          this.getMovie()
        })
        .catch(err=>{
          console.log(err.response.data)
          alert('Login이 필요합니다!')
          this.$router.push({name:'Login'})
        })
    },
    commentDelete(commentId){
      axios({
        url:'http://127.0.0.1:8000/memovies/movies/comments/'+commentId,
        method:'delete',
        headers:{
          Authorization: `JWT ${localStorage.getItem('jwt')}`
        }
      })
        .then(res=>{
          console.log(res)
          this.getMovie()
        })
        .catch(err=>{
          console.log(err)
        })
    },
    UpdateComment(comment){
      axios({
        url:`http://127.0.0.1:8000/memovies/movies/comments/`+comment.id+'/',
        method:'put',
        data:{
          user:this.userid,
          content:this.newComment,
          rate: this.newRate
        }
      })
        .then(res=>{
          console.log(res)
          this.newComment =''
          this.getMovie()
        })
        .catch(err=>{
          console.log(err)
        })
    },
    likeMovie(){
      axios({
        url:'http://127.0.0.1:8000/memovies/movies/'+this.$route.params.movieid+'/like/',
        method:'post',
        data:{
          like : this.like
        },
        headers:{
          Authorization: `JWT ${localStorage.getItem('jwt')}`
        }
      })
        .then(res=>{
          // console.log(res.data.like)
          this.like = res.data.like
          this.getMovie
        })
        .catch(err=>{
          console.log(err.response.data)
          alert('Login이 필요합니다!')
          this.$router.push({name:'Login'})
        })

    },
    getRate(event){
      console.log(event.target)
      this.rate = event.target.value
    },
    getNewRate(event){
      console.log(event.target)
      this.newRate = event.target.value
    },

  },
  computed:{
    imgUrl(){
      const tmdb_url = 'https://image.tmdb.org/t/p/w500/'
      return tmdb_url + this.movie.poster_path
    },
  }
}
</script>
<style>
  .likeStatus {
    color: palevioletred;
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

  #comment{
    background-color:lightgrey;
    border: 3px solid black;
    color:black;
  }

  /* #overview {
    width:90%;
    padding-left:13%;
  } */
</style>