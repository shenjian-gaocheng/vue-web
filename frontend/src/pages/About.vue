<script setup>
import LayoutDefault from '@/layouts/LayoutDefault.vue'
</script>

<template>
  <div class="layout-page d-flex">
    <LayoutDefault>
      <div
        :class="[
          'flex-fill',
          'd-flex',
          'flex-column',
          'bg-white',
          'text-center',
          'px-4',
          !isMobile ? 'main-scrollable' : ''
        ]"
        :style="{
          flex: 1,
          minWidth: 0,
          paddingTop: isMobile ? '76px' : '16px'
        }"
      >

        <div style="max-width: 900px; margin: 0 auto; padding-left: 16px; padding-right: 16px;">
          <div class="mt-4 mx-auto">
            <h1>关于周童玥应援站</h1>
          </div>

          <div class="mt-5 mx-auto">
            <h2 class="mb-3">本站主题</h2>
            <p>周童玥应援站是SNH48-周童玥应援会建立的，以介绍、宣传周童玥为主的网站。</p>
            <p>包括了介绍周童玥的百科、社交平台链接、以及所有周童玥参加过的公演及团内活动的列表。</p>
          </div>

          <div class="mt-5 mx-auto">
            <h2 class="mb-3">本站声明</h2>
            <p>本站为周童玥应援会建立并管理，非周童玥个人官方网站。</p>
            <p>本站仅提供周童玥及其应援会相关的信息，不提供任何站内互动渠道。</p>
            <p>若需要与应援会交流，或对本站有任何意见或建议，请加应援会QQ群：158139179。</p>
            <p>若要与周童玥互动，请前往口袋48app，在周童玥的口袋房间和她互动。</p>
          </div>
        </div>
      </div>
    </LayoutDefault>
  </div>
</template>