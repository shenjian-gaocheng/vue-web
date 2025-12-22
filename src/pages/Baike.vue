<script setup>
import OverlayMask from '@/components/OverlayMask.vue'
import Topbar from '@/components/Topbar.vue'
import Sidebar from '@/components/Sidebar.vue'
import Notification from '@/components/Notification.vue'
import { useResponsiveSidebar } from '@/composables/useResponsiveSidebar'

const { isMobile, isSidebarCollapsed } = useResponsiveSidebar()
</script>

<template>
  <div class="layout-page d-flex">
    <!-- 顶部栏：仅移动端显示 -->
    <Topbar
      v-if="isMobile"
      :collapsed="isSidebarCollapsed"
      @update:collapsed="isSidebarCollapsed = $event"
    />

    <!-- 遮罩：必须放在 Sidebar 后面、Main 前面 -->
    <OverlayMask
      v-if="isMobile && !isSidebarCollapsed"
      @click="isSidebarCollapsed = true"
    />

    <!-- 侧边栏 -->
    <Sidebar
      :is-mobile="isMobile"
      v-model:collapsed="isSidebarCollapsed"
    />

    <main 
      :class="[
        'position-relative',
        'flex-grow-1',
        'overflow-auto',
        'px-4',
        !isMobile ? 'main-scrollable' : ''
      ]"
      :style="{ paddingTop: isMobile ? '76px' : '16px' }"
    >

      <Notification />

      <!-- 姓名 & 简介 -->
      <div class="row justify-content-center mb-4">
        <div class="col-md-10 col-xl-8 text-center py-4 bg-light rounded">

          <img
            src="/bg.webp"
            alt=""
            class="mb-4"
            style="width:100%; max-width:600px; height:auto; display:block; margin:0 auto;"
          >

          <h1 class="fw-bold display-5 mb-1">周童玥</h1>
          <h3 class="text-warning fw-bold">Zhou TongYue</h3>
          <p class="text-muted">TEAM SII（SNH48 十八期生）</p>

          <!-- 社交链接 -->
          <div class="mt-3">
            <a href="https://weibo.com/u/7861137548" class="mx-3" target="_blank">
              <i class="fab fa-weibo fa-2x text-danger"></i>
            </a>
            <a href="https://v.douyin.com/R0CZVXm5esU/" class="mx-3" target="_blank">
              <i class="fab fa-tiktok fa-2x text-dark"></i>
            </a>
            <a href="https://space.bilibili.com/3537104390850991" class="mx-3" target="_blank">
              <i class="fab fa-bilibili fa-2x text-primary"></i>
            </a>
          </div>

        </div>
      </div>


      <!-- 基本信息 -->
      <div class="row justify-content-center mt-4 mb-4 g-4">
        <div class="col-md-10 col-xl-8">

          <div class="text-center mb-4">
            <h2 class="fw-bold">基本信息</h2>
          </div>

          <div class="row g-4">

            <!-- 个人信息 -->
            <div class="col-md-6">
              <div class="card shadow-sm h-100">
                <div class="card-body">
                  <h5 class="card-title text-primary mb-3">个人信息</h5>
                  <ul class="list-unstyled mb-0 text-start">
                    <li><strong>昵称：</strong> 小周</li>
                    <li><strong>生日：</strong> 2005-03-22</li>
                    <li><strong>星座：</strong> 白羊座</li>
                    <li><strong>血型：</strong> -</li>
                    <li><strong>身高：</strong> 165 cm</li>
                    <li><strong>出生地：</strong> 中国 江苏</li>
                  </ul>
                </div>
              </div>
            </div>

            <!-- 成员信息 -->
            <div class="col-md-6">
              <div class="card shadow-sm h-100">
                <div class="card-body">
                  <h5 class="card-title text-primary mb-3">成员信息</h5>
                  <ul class="list-unstyled mb-0 text-start">
                    <li><strong>加入时间：</strong> 2023-05-02</li>
                    <li><strong>加入所属：</strong> SNH48 十八期生</li>
                    <li><strong>升格时间：</strong> 2023-08-18（当日S队公演宣布）</li>
                    <li><strong>最终所属：</strong> SNH48 S队（TEAM SII）</li>
                    <li><strong>所属公司：</strong> 上海丝芭文化传媒集团有限公司</li>
                    <li><strong>Catch Phrase：</strong> 这是新月，这是满月，这是——“周童玥”！</li>
                    <li><strong>应援色：</strong> 💛 黄色</li>
                  </ul>
                </div>
              </div>
            </div>

          </div>
        </div>
      </div>


      <!-- 特长 & 兴趣爱好 -->
      <div class="row justify-content-center mt-4 mb-4 g-4">
        <div class="col-md-10 col-xl-8">

          <div class="text-center mb-4">
            <h2 class="fw-bold">个人特长及兴趣爱好</h2>
          </div>

          <div class="row g-4">

            <!-- 个人特长 -->
            <div class="col-md-6">
              <div class="card shadow-sm h-100">
                <div class="card-body">
                  <h5 class="card-title text-primary mb-3">个人特长</h5>
                  <ul class="list-unstyled mb-0">
                    <li><i class="fas fa-check text-success me-2"></i>琵琶</li>
                    <li><i class="fas fa-check text-success me-2"></i>睡觉</li>
                  </ul>
                </div>
              </div>
            </div>

            <!-- 兴趣爱好 -->
            <div class="col-md-6">
              <div class="card shadow-sm h-100">
                <div class="card-body">
                  <h5 class="card-title text-primary mb-3">兴趣爱好</h5>
                  <ul class="list-unstyled mb-0">
                    <li><i class="fas fa-heart text-danger me-2"></i>美女</li>
                    <li><i class="fas fa-paw text-primary me-2"></i>猫猫狗狗</li>
                  </ul>
                </div>
              </div>
            </div>

          </div>
        </div>
      </div>


      <!-- 参加过的公演 -->
      <div class="row justify-content-center mt-4 mb-4 g-4">
        <div class="col-md-10 col-xl-8">

          <div class="text-center mb-4">
            <h2 class="fw-bold">主要参与的公演</h2>
          </div>

          <div class="mb-4 py-4 bg-light rounded">
            <h5 class="mb-3 p-0">
              <i class="fas fa-theater-masks text-primary me-2"></i><b>Team SII《INTO THE LIGHT》公演（2025.08.16 - ）</b>
            </h5>
            <p class="mb-3 p-0">
              <i class="fas fa-theater-masks text-warning me-2"></i>《命运的X号》新生公演（2023.05.02 - 2024.04.24）
            </p>
            <p class="mb-3 p-0">
              <i class="fas fa-theater-masks text-primary me-2"></i>Team SII《幻镜》B版公演（2023.05.26 - 2025.02.16）
            </p>
            <p class="mb-3 p-0">
              <i class="fas fa-theater-masks text-warning me-2"></i>《代号XII 2.0》新生公演（2024.05.05 - 2025.03.12）
            </p>
            <p class="m-0 p-0">
              <i class="fas fa-theater-masks text-primary me-2"></i>Team SII《幻镜》C版公演（2025.02.23 - 2025.07.27）
            </p>
          </div>
        </div>
      </div>

      <!-- 奖项 -->
      <div class="row justify-content-center mt-4 mb-4">
        <div class="col-md-10 col-xl-8">

          <div class="text-center mb-4">
            <h2 class="fw-bold">获奖</h2>
          </div>

          <div class="mb-4 py-4 bg-light rounded">
            <h5 class="mb-3 p-0">
              <i class="fas fa-trophy text-warning me-2"></i>
              <b>2025 SNH48 GROUP 年度青春盛典 No.47（年度梦想成员奖）</b>
            </h5>
            <p class="m-0 p-0">
              <i class="fas fa-trophy text-warning me-2"></i>
              2024 SNH48 GROUP 年度青春盛典 No.53
            </p>
          </div>

        </div>
      </div>

      <!-- 团内人物关系 -->
      <div class="row justify-content-center mt-4 mb-4">
        <div class="col-md-10 col-xl-8">

          <!-- 模块标题（与内容同宽） -->
          <div class="text-center mb-4">
            <h2 class="fw-bold mb-2">团内人物关系</h2>
            <!-- 可选副标题 -->
            <!-- <div class="text-muted small">周童玥的队友与其他活动关系整理</div> -->
          </div>

          <!-- 外层卡片 -->
          <div class="card shadow-sm border-0">
            <div class="card-body p-4 p-md-5">

              <!-- 分区标题 -->
              <div class="mb-4">
                <div class="d-flex align-items-center justify-content-between flex-wrap gap-2">
                  <h5 class="mb-0">周童玥的队友</h5>
                  <span class="badge text-bg-secondary">Team / 新生 / 活动</span>
                </div>
                <hr class="my-3">
              </div>

              <!-- Team SII 现队友 -->
              <section class="border-0 bg-light-subtle mb-4">
                <div class="card-body">
                  <div class="d-flex align-items-center justify-content-between flex-wrap gap-2 mb-2">
                    <h4 class="mb-0">Team SII 现队友</h4>
                    <span class="badge rounded-pill text-bg-primary">现</span>
                  </div>
                  <p class="text-muted mb-3">
                    包括正式成员、兼任成员和已分配到 Team SII 的预备生。
                  </p>

                  <div class="d-flex flex-wrap gap-2 name-wrap">
                    <span class="badge rounded-pill text-bg-light border text-dark">曹可甜</span>
                    <span class="badge rounded-pill text-bg-light border text-dark">陈雨孜</span>
                    <span class="badge rounded-pill text-bg-light border text-dark">蒋夏羽</span>
                    <span class="badge rounded-pill text-bg-light border text-dark">芦馨怡</span>
                    <span class="badge rounded-pill text-bg-light border text-dark">刘诗彤</span>
                    <span class="badge rounded-pill text-bg-light border text-dark">刘增艳</span>
                    <span class="badge rounded-pill text-bg-light border text-dark">柳雨呈</span>
                    <span class="badge rounded-pill text-bg-light border text-dark">宁轲</span>
                    <span class="badge rounded-pill text-bg-light border text-dark">盛乐</span>
                    <span class="badge rounded-pill text-bg-light border text-dark">田姝丽</span>
                    <span class="badge rounded-pill text-bg-light border text-dark">由淼</span>
                    <span class="badge rounded-pill text-bg-light border text-dark">闫明筠</span>
                    <span class="badge rounded-pill text-bg-light border text-dark">杨心渝</span>
                    <span class="badge rounded-pill text-bg-light border text-dark">张雷雷</span>
                    <span class="badge rounded-pill text-bg-light border text-dark">张倩</span>
                    <span class="badge rounded-pill text-bg-light border text-dark">赵天杨</span>

                    <span class="badge rounded-pill text-bg-warning text-dark">武博涵（Team X兼任）</span>
                    <span class="badge rounded-pill text-bg-info text-dark">李婷（预备生）</span>
                    <span class="badge rounded-pill text-bg-info text-dark">刘婧阳（预备生）</span>
                  </div>
                </div>
              </section>

              <!-- Team SII 前队友 -->
              <section class="border-0 bg-light-subtle mb-4">
                <div class="card-body p-4">
                  <div class="d-flex align-items-center justify-content-between flex-wrap gap-2 mb-2">
                    <h4 class="mb-0">Team SII 前队友</h4>
                    <span class="badge rounded-pill text-bg-secondary">前</span>
                  </div>
                  <p class="text-muted mb-3">
                    包括已毕业或退团的正式成员，以及已解除兼任的兼任成员。
                  </p>

                  <div class="d-flex flex-wrap gap-2 name-wrap">
                    <span class="badge rounded-pill text-bg-light border text-dark">李慧</span>
                    <span class="badge rounded-pill text-bg-light border text-dark">马玉灵</span>
                    <span class="badge rounded-pill text-bg-light border text-dark">邵雪聪</span>
                    <span class="badge rounded-pill text-bg-light border text-dark">朱涵佳</span>
                    <span class="badge rounded-pill text-bg-light border text-dark">黄恩茹</span>
                    <span class="badge rounded-pill text-bg-warning text-dark">刘倩倩（原GNZ48 Team NIII兼任）</span>
                    <span class="badge rounded-pill text-bg-light border text-dark">彭嘉敏</span>
                    <span class="badge rounded-pill text-bg-warning text-dark">黄怡慈（原BEJ48 Team B兼任）</span>
                    <span class="badge rounded-pill text-bg-light border text-dark">段艺璇</span>
                    <span class="badge rounded-pill text-bg-light border text-dark">沈小爱</span>


                  </div>
                </div>
              </section>

              <!-- 新生公演 前队友 -->
              <section class="border-0 bg-light-subtle mb-5">
                <div class="card-body p-4">
                  <div class="d-flex align-items-center justify-content-between flex-wrap gap-2 mb-2">
                    <h4 class="mb-0">新生公演 前队友</h4>
                    <span class="badge rounded-pill text-bg-secondary">新生阶段</span>
                  </div>
                  <p class="text-muted mb-3">
                    新生公演（《命运的X号》《代号XII 2.0》）时期队友，不包括 Team SII 成员。
                  </p>

                  <div class="d-flex flex-wrap gap-2 name-wrap">
                    <span class="badge rounded-pill text-bg-light border text-dark">林佳怡</span>
                    <span class="badge rounded-pill text-bg-light border text-dark">禹佳蔚</span>
                    <span class="badge rounded-pill text-bg-light border text-dark">张月铭</span>
                    <span class="badge rounded-pill text-bg-light border text-dark">王依柳</span>
                    <span class="badge rounded-pill text-bg-light border text-dark">熊紫轶</span>
                    <span class="badge rounded-pill text-bg-light border text-dark">刘小涵</span>
                    <span class="badge rounded-pill text-bg-light border text-dark">卢晨昕</span>
                    <span class="badge rounded-pill text-bg-light border text-dark">李虞龙若</span>
                    <span class="badge rounded-pill text-bg-light border text-dark">温若其</span>
                    <span class="badge rounded-pill text-bg-light border text-dark">许佳佳</span>
                    <span class="badge rounded-pill text-bg-light border text-dark">尤可莹</span>
                    <span class="badge rounded-pill text-bg-light border text-dark">张怡婷</span>
                    <span class="badge rounded-pill text-bg-light border text-dark">梁怀方</span>
                    <span class="badge rounded-pill text-bg-light border text-dark">唐程成</span>
                    <span class="badge rounded-pill text-bg-light border text-dark">王悦垚</span>
                    <span class="badge rounded-pill text-bg-light border text-dark">王紫澍</span>
                    <span class="badge rounded-pill text-bg-light border text-dark">叶凡</span>
                    <span class="badge rounded-pill text-bg-light border text-dark">张瀚引</span>
                    <span class="badge rounded-pill text-bg-light border text-dark">陈真允一</span>
                    <span class="badge rounded-pill text-bg-light border text-dark">罗颍宸</span>
                    <span class="badge rounded-pill text-bg-light border text-dark">温冰冰</span>
                    <span class="badge rounded-pill text-bg-light border text-dark">吴欣怡</span>
                    <span class="badge rounded-pill text-bg-light border text-dark">夏奕欣</span>
                    <span class="badge rounded-pill text-bg-light border text-dark">张曼妮</span>
                    <span class="badge rounded-pill text-bg-light border text-dark">陈芷晴</span>
                    <span class="badge rounded-pill text-bg-light border text-dark">潘力帼</span>
                    <span class="badge rounded-pill text-bg-light border text-dark">陈俞希</span>
                    <span class="badge rounded-pill text-bg-light border text-dark">金泓言</span>
                    <span class="badge rounded-pill text-bg-light border text-dark">李妍</span>
                    <span class="badge rounded-pill text-bg-light border text-dark">李子忻</span>
                    <span class="badge rounded-pill text-bg-light border text-dark">杨秋野（原名孙莉）</span>
                    <span class="badge rounded-pill text-bg-light border text-dark">肖彦竹</span>

                  </div>
                </div>
              </section>

              <!-- 其他关系 -->
              <section class="border-0 bg-white">
                <div class="card-body p-4">
                  <h4 class="mb-2">其他关系</h4>
                  <p class="text-muted mb-3">
                    周童玥在 SNH48 GROUP 其他活动中的队友。
                  </p>

                  <div class="vstack gap-3">
                    <div class="p-3 bg-light-subtle rounded">
                      <div class="fw-semibold mb-1">《最佳拍档》第四季 拍档</div>
                      <div class="text-muted">庄雅雯（前 BEJ48 Team E 成员）</div>
                    </div>

                    <div class="p-3 bg-light-subtle rounded">
                      <div class="fw-semibold mb-1">《燃烧吧，团魂》第二季「我说的都队」社团</div>
                      <div class="text-muted">
                        刘增艳、叶凡（SNH48 Team NII 成员）、张倩、唐程成（SNH48 Team NII 成员）
                        <span class="ms-2 badge text-bg-primary">周童玥：队长</span>
                      </div>
                    </div>
                  </div>
                </div>
              </section>

            </div>
          </div>

        </div>
      </div>


    </main>
  </div>
</template>

<style scoped>
.card {
  border: none;
  background-color: #f8f9fa;
}
hr {
  border-top: 1px solid #dee2e6;
}

.name-wrap{
  max-width: 720px;   /* 关键：控制一行大约 6 个 */
  margin: 0 auto;     /* 居中 */
}
</style>