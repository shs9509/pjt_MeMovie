import Vue from 'vue'
import VueRouter from 'vue-router'
import Login from '@/views/accounts/Login'
import Signup from '@/views/accounts/Signup'
import Home from '@/views/Home'
import BootstrapVue from 'bootstrap-vue'
import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap-vue/dist/bootstrap-vue.css'
import Community from '@/views/community/Community'
import ReviewCreate from '@/views/community/ReviewCreate'
import ReviewDetail from '@/views/community/ReviewDetail'
import MovieDetail from '@/views/movies/MovieDetail'
import NaverMovieDetail from '@/views/movies/NaverMovieDetail'
import BoxofficeMovieDetail from '@/views/movies/BoxofficeMovieDetail'
import Profile from '@/views/accounts/Profile'
import UserRecommend from '@/views/movies/UserRecommend'
import Recommend from '@/views/movies/Recommend'
import ReviewUpdate from '@/views/community/ReviewUpdate'


Vue.use(BootstrapVue);
Vue.use(VueRouter)

const routes = [
  {
    path:'/memovies/movies/UserRecommend/:userid',
    name:'UserRecommend',
    component: UserRecommend,
  },
  {
    path:'/memovies/',
    name:'Home',
    component:Home,
  },
  {
    path: '/memovies/accounts/login',
    name: 'Login',
    component: Login
  },
  {
    path: '/memovies/accounts/signup',
    name: 'Signup',
    component: Signup
  }, 
  {
    path:'/memovies/community/',
    name:'Community',
    component: Community,
  },
  {
    path:'/memovies/community/reviewcreate',
    name:'ReviewCreate',
    component: ReviewCreate,
  },
  {
    path:'/memovies/community/review/:reviewId',
    name:'ReviewDetail',
    component: ReviewDetail,
    props: true,
  },
  {
    path:'/memovies/:movieid',
    name:'MovieDetail',
    component: MovieDetail,
    props: true,
  },
  {
    path:'/memovies/naver/:movieid',
    name:'NaverMovieDetail',
    component: NaverMovieDetail,
    props: true,
  },
  {
    path:'/memovies/naver/:movieid',
    name:'BoxofficeMovieDetail',
    component: BoxofficeMovieDetail,
    props: true,
  },
  {
    path:'/memovies/accounts/profile/:userid',
    name: 'Profile',
    component: Profile,
    props: true,
  },
  {
    path:'/memovies/UserRecommend/:userid',
    name:'UserRecommend',
    component: UserRecommend,
  },
  {
    path:'/memovies/Recommend/',
    name:'Recommend',
    component: Recommend,
  },
  {
    path:'/memovies/community/update/:reviewid',
    name: 'ReviewUpdate',
    component: ReviewUpdate,
    props: true,
  },
]
const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
})




export default router
