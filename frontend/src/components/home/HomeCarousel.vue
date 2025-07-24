<template>
  <section class="swiper-section">
    <div class="carousel-fullscreen">  
      <Swiper
        :modules="[Autoplay, Pagination, EffectFade]"
        :loop="true"
        :autoplay="{ delay: 5000 }"
        :effect="'fade'"
        @swiper="onSwiper"
        @slideChange="onSlideChange"
        class="my-swiper"
      >
        <SwiperSlide v-for="(img, index) in images" :key="index">
          <div class="slide" :style="{ backgroundImage: `url(${img})` }">
            <div class="overlay">
              <div 
                class="slide-text"
                v-if="currentIndex === 0"
              >
                这是新月，这是满月<br />
                <span style="margin-left: 2em;">——这是周童玥</span>
              </div>
            </div>
          </div>
        </SwiperSlide>
      </Swiper>
      
      <!-- 横线指示器 -->
      <div class="indicator-container">
        <div
          v-for="(img, index) in images"
          :key="'indicator-' + index"
          class="indicator-line"
          :class="{ active: index === currentIndex }"
          @click="goToSlide(index)"
        ></div>
      </div>
      
    </div>
  </section>
</template>

<script setup>
import 'swiper/css'
import 'swiper/css/effect-fade'
import 'swiper/css/pagination'

import { Swiper, SwiperSlide } from 'swiper/vue'
import { Autoplay, Pagination, EffectFade } from 'swiper/modules'
import { ref } from 'vue'

const currentIndex = ref(0)
let swiperInstance = null
const goToSlide = (index) => {
  if (swiperInstance) {
    swiperInstance.slideToLoop(index)
    currentIndex.value = index
  }
}

const onSwiper = (swiper) => {
  swiperInstance = swiper
}

const onSlideChange = () => {
  if (swiperInstance) {
    currentIndex.value = swiperInstance.realIndex
  }
}


const images = [
  'https://wx4.sinaimg.cn/mw1024/008cOgx0ly1hq7lc57l93j349a2e9hdw.jpg',
  'https://wx1.sinaimg.cn/mw1024/008A0wZ6gy1hzq8e8x3q9j34802tcu10.jpg',
  'https://wx2.sinaimg.cn/mw1024/008bletUgy1i30rvidx6vj31900u0do1.jpg',
]
</script>

<style scoped>
.carousel-fullscreen {
  position: relative;
  width: 100vw;     /* 强制使用整屏宽度 */
  height: 100vh;    /* 高度为整屏 */
  margin: 0;
  padding: 0;
}

/* 外部容器占满视口 */
.swiper-section {
  width: 100%;
  height: 100vh;
}

/* Swiper本体必须有高度 */
.my-swiper {
  height: 100%;
}

/* 每一页必须设置高度 */
.swiper-slide {
  height: 100%;
}

/* 每页的背景图 + 居中文本 */
.slide {
  width: 100%;
  height: 100%;
  background-size: cover;
  background-position: center;
  position: relative;
}

/* 中间叠加文字内容 */
.overlay {
  position: absolute;
  top: 0; left: 0;
  width: 100%; height: 100%;
  background: rgba(0, 0, 0, 0.3);
  color: white;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  text-align: center;
  padding: 2rem;
}

.overlay h1 {
  font-size: 2.5rem;
  margin-bottom: 1rem;
}

.overlay p {
  font-size: 1.2rem;
  margin-bottom: 2rem;
}

.overlay button {
  background: #ca4770;
  color: white;
  border: none;
  padding: 0.8rem 1.5rem;
  border-radius: 5px;
  font-size: 1rem;
  cursor: pointer;
}

.indicator-container {
  position: absolute;
  bottom: 20px;
  left: 0;
  right: 0;
  display: flex;
  justify-content: center;
  z-index: 10;
}

.indicator-line {
  width: 30px;
  height: 3px;
  background-color: rgba(255, 255, 255, 0.3); ;
  margin: 0 5px;
  cursor: pointer;
  transition: background-color 0.3s;
  border-radius: 2px;
}

.indicator-line.active {
  background-color: #ffffff;
  height: 3px;
}

.slide-text {
  position: absolute;
  bottom: 30%;
  right: 15%;
  transform: translateX(50%);
  font-size: 28px;
  font-family: serif;
  font-weight: 700;
  line-height: 2;
  text-align: center;
  color: rgba(255, 255, 255, 0.96);
  text-shadow: 0 2px 6px rgba(0, 0, 0, 0.6);
  opacity: 0;
  animation: fadeUp 1.8s ease-out 0.6s forwards;
  pointer-events: none;
  white-space: pre-line;
}




@keyframes fadeUp {
  0% {
    transform: translateY(30px);
    opacity: 0;
  }
  100% {
    transform: translateY(0);
    opacity: 1;
  }
}

</style>
